pyrouge
=======

A Python interface to the ROUGE package. A working installation of ROUGE 1.5.5 is required to run the package.

Right now, only the basic functionality is in place. You can score one summary at a time with respect to multiple reference summaries.
Down the road, the plan is to reimplement (parts of) ROUGE in pure Python.
The motivation is that the ROUGE package, while standard in evaluation of extractive summaries,
can be a challenge to obtain and install, and also does not fit well in a Python workflow.

Contributions and suggestions are very welcome.

## Usage example

```
from pyrouge import Rouge155, Doc, Sent
from pprint import pprint

ref_texts = ["Poor nations pressurise developed countries into granting trade subsidies.",
             "Developed countries should be pressurized. Business exemptions to poor nations.",
             "World's poor decide to urge developed nations for business concessions."]
summary_text = "Poor nations demand trade subsidies from developed nations."

# Substitute path to rouge home directory
ROUGE_HOME="/Users/anders/code/diogenes/tools/rouge-1.5.5-dist/ROUGE-1.5.5"
rouge = Rouge155(ROUGE_HOME)

# Wrap the summary and references in pyrouge.Doc and pyrouge.Sent objects
summary = Doc(id="summary", sents=[Sent(1, summary_text)])
refs = [Doc(id=chr(65+i), sents=[Sent(1, ref_text)]) for i, ref_text in enumerate(ref_texts)]

score = rouge.score_summary(summary, refs)
pprint(score)
```

The output will be something like this:

```
{'rouge_1_f_score': 0.40741,
 'rouge_1_f_score_cb': 0.40741,
 'rouge_1_f_score_ce': 0.40741,
 'rouge_1_precision': 0.45833,
 'rouge_1_precision_cb': 0.45833,
 'rouge_1_precision_ce': 0.45833,
 'rouge_1_recall': 0.36667,
 'rouge_1_recall_cb': 0.36667,
 'rouge_1_recall_ce': 0.36667,
 'rouge_2_f_score': 0.16667,
 'rouge_2_f_score_cb': 0.16667,
 'rouge_2_f_score_ce': 0.16667,
 'rouge_2_precision': 0.19048,
 'rouge_2_precision_cb': 0.19048,
 'rouge_2_precision_ce': 0.19048,
 'rouge_2_recall': 0.14815,
 'rouge_2_recall_cb': 0.14815,
 'rouge_2_recall_ce': 0.14815,
 'rouge_3_f_score': 0.0,
 'rouge_3_f_score_cb': 0.0,
 'rouge_3_f_score_ce': 0.0,
 'rouge_3_precision': 0.0,
 'rouge_3_precision_cb': 0.0,
 'rouge_3_precision_ce': 0.0,
 'rouge_3_recall': 0.0,
 'rouge_3_recall_cb': 0.0,
 'rouge_3_recall_ce': 0.0,
 'rouge_4_f_score': 0.0,
 'rouge_4_f_score_cb': 0.0,
 'rouge_4_f_score_ce': 0.0,
 'rouge_4_precision': 0.0,
 'rouge_4_precision_cb': 0.0,
 'rouge_4_precision_ce': 0.0,
 'rouge_4_recall': 0.0,
 'rouge_4_recall_cb': 0.0,
 'rouge_4_recall_ce': 0.0,
 'rouge_su4_f_score': 0.13158,
 'rouge_su4_f_score_cb': 0.13158,
 'rouge_su4_f_score_ce': 0.13158,
 'rouge_su4_precision': 0.15625,
 'rouge_su4_precision_cb': 0.15625,
 'rouge_su4_precision_ce': 0.15625,
 'rouge_su4_recall': 0.11364,
 'rouge_su4_recall_cb': 0.11364,
 'rouge_su4_recall_ce': 0.11364}
```
## Run tests

The unit tests can be run be issuing ``nosetests´´ from the root directory of the package.
