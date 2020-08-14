#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name         = 'medleysolver',
    version      = '0.1',
    description  = 'Algorithm Selection for SMT Solver',
    author       = 'Nikhil Pimpalkhare',
    author_email = 'nikhil.pimpalkhare@berkeley.edu',
    url          = 'https://github.com/nikhilpim/medley-solver/',
    scripts      = [
        'bin/medley',
    ],
    packages     = find_packages(),
    install_requires = [
        'numpy',
        'z3',
        'tqdm',
        'dill'
    ],
)