from setuptools import setup
import os

from pyrouge.utils.file_utils import list_files


data_files = list_files('pyrouge/test/data')
data_files = [p.replace('pyrouge/test/', '') for p in data_files]

setup(
    name='pyrouge',
    version='0.1.0',
    author='Benjamin Heinzerling, Anders Johannsen',
    author_email='benjamin.heinzerling@h-its.org',
    packages=['pyrouge', 'pyrouge.utils', 'pyrouge.test'],
    scripts=[
        'bin/pyrouge_set_rouge_path.py',
        'bin/pyrouge_convert_plain_text_to_rouge_format.py',
        'bin/pyrouge_evaluate_plain_text_files.py',
        'bin/pyrouge_convert_rouge_format_to_plain_text.py',
        'bin/pyrouge_evaluate_rouge_format_files.py',
        'bin/pyrouge_write_config_file.py'
        ],
    #test_suite='pyrouge.test.suite',
    package_data={'pyrouge.test': data_files},
    url='http://pypi.python.org/pypi/pyrouge/',
    license='LICENSE.txt',
    description='A Python wrapper for the ROUGE summarization evaluation'
        ' package.',
    long_description=open('README.md').read(),
    )
