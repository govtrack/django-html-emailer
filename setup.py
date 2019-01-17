# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages
from codecs import open

setup(
  name='django-html-emailer',
  version='0.0.8',
  
  description='Utility for sending HTML emails from Django.',
  long_description=open("README.md", encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/if-then-fund/django-html-emailer',
  keywords="Django email HTML",
  classifiers=[ # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],

  author='Joshua Tauberer',
  author_email='jt@occams.info',
  license='MIT',

  install_requires=[
  	'pynliner',
  	"commonmark>=0.8.0",
    "commonmarkextensions>=0.0.1",
  ],
  packages=find_packages(),
  package_data={'htmlemailer': ['templates/htmlemailer/*']},
)
