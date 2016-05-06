#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    'pynliner', 'commonmark'
]

setup(name='django-html-emailer',
      version='0.0.2',
      description='Utility for sending HTML emails from Django.',
      author='Joshua Tauberer',
      author_email='jt@occams.info',
      install_requires=install_requires,
      packages=['htmlemailer'],
      provides=['htmlemailer'],
      package_data={'htmlemailer': ['templates/htmlemailer/*']},
)
