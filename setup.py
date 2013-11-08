from setuptools import setup

setup(name='pyrouge',
      version='0.1',
      description='An interface to the ROUGE package for evaluating summarization',
      url='http://github.com/storborg/funniest',
      author='Anders Johannsen',
      author_email='anders@johannsen.com',
      license='https://github.com/andersjo/pyrouge',
      packages=['pyrouge'],
      install_requires=["beautifulsoup4", "pandas"],
      zip_safe=False)
