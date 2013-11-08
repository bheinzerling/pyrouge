import os
from pyrouge.base import Doc

__author__ = 'anders'

def rouge_home():
    return os.getenv("ROUGE_EVAL_HOME", "/Users/anders/code/diogenes/tools/rouge-1.5.5-dist/ROUGE-1.5.5")


SL2003_DIR = "/users/anders/code/pyrouge/data/SL2003"
SL2003_MODELS_DIR = os.path.join(SL2003_DIR, "models")
SL2003_SYSTEMS_DIR = os.path.join(SL2003_DIR, "systems")

def sl2003_summary(kind, filename):
    summary_dir = os.path.join(SL2003_DIR, kind)
    summary_contents = open(os.path.join(summary_dir, filename)).read()
    return Doc.from_see(summary_contents)


