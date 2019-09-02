# from setup_reqs import use_setuptools
# use_setuptools()
import os
from setuptools import setup, find_packages
from distutils.core import setup
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyminesweeper",
    version = "0.9",
    author = "JustaGist",
    author_email = "saifksidhik@gmail.com",
    description = ("minesweeper game written in python 3"),
    license = "BSD",
    keywords = "minesweeer, game",
    # url = "https://bitbucket.org/justagist/reinfor_learn",
    packages=find_packages(),
    scripts=['pyminesweeper/commandlinescripts/pyminesweeper'],
    install_requires=[
          'pygame', 'numpy'
      ],
    long_description=read('README.md'),
    classifiers=[],
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: BSD License",
    # ],
)