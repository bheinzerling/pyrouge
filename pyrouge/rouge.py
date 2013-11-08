import codecs
from collections import defaultdict
import shutil
import pandas as pd
import logging
from os import mkdir
import os
import re
from subprocess import check_output
from tempfile import mkdtemp

class Rouge155(object):
    def __init__(self, rouge_home, n_words=None, stem=False, keep_files=False):
        self._stem = stem
        self._n_words = n_words
        self._discover_rouge(rouge_home)
        self._keep_files = keep_files

    def _discover_rouge(self, rouge_home):
        self._rouge_home = rouge_home
        self._rouge_bin = os.path.join(rouge_home, 'ROUGE-1.5.5.pl')
        if not os.path.exists(self._rouge_bin):
            raise "Rouge binary not found at {}".format(self._rouge_bin)
        self._rouge_data = os.path.join(rouge_home, 'data')
        if not os.path.exists(self._rouge_data):
            raise "Rouge data dir not found at {}".format(self._rouge_data)

    def _write_summary(self, summary, models_dir):
        summary_filename = os.path.join(models_dir, summary.id + ".html")
        with codecs.open(summary_filename, 'w', encoding='utf-8') as f:
            f.write(rouge_summary_content(summary.id, summary.sents))

        return summary.id + ".html"

    def _write_references(self, references, peers_dir):
        reference_basenames = []
        for reference in references:
            reference_filename = os.path.join(peers_dir, reference.id + ".html")
            reference_basenames.append(reference.id + ".html")
            with codecs.open(reference_filename, 'w', encoding='utf-8') as f:
                f.write(rouge_summary_content(reference.id, reference.sents))

        return reference_basenames

    def _write_config(self, references, summary):
        temp_dir = mkdtemp()
        self._config_dir = temp_dir
        summary_dir = os.path.join(temp_dir, 'models')
        reference_dir = os.path.join(temp_dir, 'peers')
        mkdir(summary_dir)
        mkdir(reference_dir)
        summary_file = self._write_summary(summary, summary_dir)
        reference_files = self._write_references(references, reference_dir)
        settings_file = os.path.join(temp_dir, "settings.xml")
        with codecs.open(settings_file, 'w', encoding='utf-8') as f:
            settings_xml = rouge_settings_content("task", reference_dir, reference_files, summary_dir, [summary_file])
            f.write(settings_xml)

        logging.info("Writing ROUGE configuration to {}".format(temp_dir))

    def score_summary(self, summary, references):
        """``summary'' is a system-generated summary.
        ``references'' is a list of human-made reference summaries"""
        try:
            self._write_config(references, summary)
            output = self._run_rouge()
            return self._parse_output(output)
        finally:
            self._cleanup()

    def score_summaries(self, summaries, references_list):
        """``summaries'' is a dictionary of system-name, summary pairs.
        ``references_list'' is a list of lists, each containing human-made reference summaries"""
        #assert len(summaries) == len(references_list)
        scores = []
        for system_name, references in zip(summaries.keys(), references_list):

            scores.append(self.score_summary(summary, references))
        pass

    #def score_system(self, system):
    #    pass

    def _run_rouge(self):
        options = [
            '-e', self._rouge_data,
            '-a', # evaluate all systems
            '-n', 4,  # max-ngram
            '-x', # do not calculate ROUGE-L
            '-2', 4, # max-gap-length
            '-u', # include unigram in skip-bigram
            '-c', 95, # confidence interval
            '-r', 1000, # number-of-samples (for resampling)
            '-f', 'A', # scoring formula
            '-p', 0.5, # 0 <= alpha <=1
            '-t', 0, # count by token instead of sentence
            '-d', # print per evaluation scores
        ]

        if self._n_words:
            options.extend(["-l", self._n_words])
        if self._stem:
            options.append("-m")

        options.append(os.path.join(self._config_dir, "settings.xml"))

        options = map(str, options)
        logging.info("Running ROUGE with options {}".format(" ".join(options)))

        return check_output([self._rouge_bin] + options)

    def _parse_output(self, output):
        #0 ROUGE-1 Average_R: 0.02632 (95%-conf.int. 0.02632 - 0.02632)
        pattern = re.compile(r"(\d+) (ROUGE-\S+) (Average_\w): (\d.\d+) \(95%-conf.int. (\d.\d+) - (\d.\d+)\)")
        results = {}
        for line in output.split("\n"):
            match = pattern.match(line)
            if match:
                sys_id, rouge_type, measure, result, conf_begin, conf_end = match.groups()
                measure = {'Average_R': 'recall', 'Average_P': 'precision', 'Average_F': 'f_score'}[measure]
                rouge_type = rouge_type.lower().replace("-", '_')
                key = "{}_{}".format(rouge_type, measure)


                results[key] = float(result)
                results["{}_cb".format(key)] = float(conf_begin)
                results["{}_ce".format(key)] = float(conf_end)

        return results

    def _cleanup(self):
        if not self._keep_files:
            shutil.rmtree(self._config_dir)


def rouge_summary_content(title, sents):
    sent_elems = []
    for sent_i, sent in enumerate(sents, 1):
        # $line=~/^<a name=\"[0-9]+\">\[([0-9]+)\]<\/a>\s+<a href=\"\#[0-9]+\" id=[0-9]+>([^<]+)/o) {

        elem = u"<a name=\"{i}\">[{i}]</a> <a href=\"#{i}\" id={i}>{text}</a>".format(i=sent_i, text=sent.text)
        sent_elems.append(elem)

    doc = u"""<html>
  <head>
    <title>{title}</title>
  </head>
  <body>
{elems}
  </body>
</html>""".format(title=title, elems="\n".join(sent_elems))

    return doc



def rouge_settings_content(task_id, model_root, model_filenames, peer_root, peer_filenames):
    model_elems = ["<M ID=\"{id}\">{name}</M>".format(id=chr(65 + i), name=name)
                   for i, name in enumerate(model_filenames)]
    model_elems = "        \n".join(model_elems)
    peer_elems = ["<P ID=\"{id}\">{name}</P>".format(id=i, name=name)
                  for i, name in enumerate(peer_filenames)]
    peer_elems = "        \n".join(peer_elems)

    settings = """
<ROUGE_EVAL version="1.55">
    <EVAL ID="{task_id}">
        <MODEL-ROOT>{model_root}</MODEL-ROOT>
        <PEER-ROOT>{peer_root}</PEER-ROOT>
        <INPUT-FORMAT TYPE="SEE">  </INPUT-FORMAT>
        <PEERS>
            {peer_elems}
        </PEERS>
        <MODELS>
            {model_elems}
        </MODELS>
    </EVAL>
</ROUGE_EVAL>""".format(task_id=task_id, model_root=model_root, model_elems=model_elems,
                        peer_root=peer_root, peer_elems=peer_elems)

    return settings

#if __name__ == '__main__':
    #filename = '/Users/anders/code/diogenes/data/nu-er-tillidsfolkene-ikke-blot-til-pynt.tok'
    #sents = read_dk_tagged_sents(filename)
    #print rouge_summary_content("myfile", sents)
    #
    #ROUGE_BIN = "/Users/anders/code/diogenes/tools/rouge-1.5.5-dist/ROUGE-1.5.5/ROUGE-1.5.5.pl"
    #r = Rouge(rouge_path=ROUGE_BIN)
    #r.eval(Document(id="alpha", sents=sents), [Document(id="alpha", sents=sents)])
    #r.


# command = '%s -e %s -l %d -n 4 -x -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -d %s 1' %(executable, rouge_data, length, config_file)
