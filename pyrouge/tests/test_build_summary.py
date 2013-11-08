import os
from unittest import TestCase

from pyrouge import rouge
from pyrouge.base import Doc
from pyrouge.tests import rouge_home

ROUGE_PATH = rouge_home()
DATA_DIR = "/users/anders/code/pyrouge/data/SL2003"

class TestRougeCompat(TestCase):

    def test_read_summary(self):
        #<html>
        #<head>
        #<title>SL.P.10.R.A.SL062003-01</title>
        #</head>
        #<body bgcolor="white">
        #<a name="1">[1]</a> <a href="#1" id=1>Poor nations demand trade subsidies from developed nations.</a>
        #</body>
        #</html>
        summary_fname = os.path.join(DATA_DIR, "models/SL.P.10.R.A.SL062003-01.html")
        summary = Doc.from_see(open(summary_fname).read())
        self.assertEqual(summary.id, "SL.P.10.R.A.SL062003-01")
        self.assertEqual(len(summary.sents), 1)

        first_sent = summary.sents[0]
        self.assertEqual(first_sent.text, "Poor nations demand trade subsidies from developed nations.")




    
            
    
    #def test_eval(self):
    #    r = rouge.Rouge155(ROUGE_PATH)
    #    r.eval()


