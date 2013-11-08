from pprint import pprint
from unittest import TestCase

from pyrouge import rouge
from pyrouge.tests import rouge_home, sl2003_summary

ROUGE_PATH = rouge_home()
class TestRougeCompat(TestCase):

    def test_invalid_rouge(self):
        with self.assertRaises(Exception):
            rouge.Rouge155(ROUGE_PATH + "invalid")

    def test_valid_rouge(self):
        try:
            rouge.Rouge155(ROUGE_PATH)
        except Exception:
            self.fail("Rouge155() raised Exception unexpectedly!")


    def test_run_rouge(self):
        r = rouge.Rouge155(ROUGE_PATH)

        # [11,12,13,14,21,22,23,24]

        system = sl2003_summary("systems", "SL.P.10.R.11.SL062003-01.html")
        models = [sl2003_summary("models", "SL.P.10.R.{}.SL062003-01.html".format(c))
                  for c in "ABCD"]

        results = r.score_summary(system, models)
        expected_columns = ['rouge_su4_precision', 'rouge_3_f_score_cb', 'rouge_3_f_score_ce', 'rouge_1_precision', 'rouge_su4_f_score', 'rouge_3_recall', 'rouge_3_precision_ce', 'rouge_2_precision_ce', 'rouge_2_precision_cb', 'rouge_2_recall', 'rouge_3_precision_cb', 'rouge_4_f_score_ce', 'rouge_2_precision', 'rouge_1_recall_cb', 'rouge_1_recall_ce', 'rouge_4_f_score_cb', 'rouge_2_recall_cb', 'rouge_su4_f_score_ce', 'rouge_su4_f_score_cb', 'rouge_2_recall_ce', 'rouge_4_precision_cb', 'rouge_4_precision_ce', 'rouge_1_f_score', 'rouge_4_recall_ce', 'rouge_su4_precision_ce', 'rouge_1_recall', 'rouge_4_recall_cb', 'rouge_4_recall', 'rouge_3_recall_cb', 'rouge_3_recall_ce', 'rouge_4_precision', 'rouge_4_f_score', 'rouge_3_f_score', 'rouge_2_f_score_cb', 'rouge_3_precision', 'rouge_2_f_score_ce', 'rouge_su4_recall_cb', 'rouge_su4_precision_cb', 'rouge_su4_recall_ce', 'rouge_1_precision_cb', 'rouge_su4_recall', 'rouge_1_precision_ce', 'rouge_2_f_score', 'rouge_1_f_score_ce', 'rouge_1_f_score_cb']
        self.assertListEqual(results.keys(), expected_columns)
        self.assertAlmostEqual(results['rouge_1_f_score'], 0.02857)
