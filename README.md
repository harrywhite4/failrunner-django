[![Build Status](https://travis-ci.com/harrywhite4/failrunner-django.svg?branch=master)](https://travis-ci.com/harrywhite4/failrunner-django)
[![PyPI version shields.io](https://img.shields.io/pypi/v/failrunner-django.svg)](https://pypi.python.org/pypi/failrunner-django/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/failrunner-django.svg)](https://pypi.python.org/pypi/failrunner-django/)

# failrunner-django
A command line tool to run django tests that failed during a travis job

# Installation

- Install with pip `pip install failrunner-django`
- You should now have the `failrunner` command

# Basic Usage
- To run a job `failrunner -j jobnumber` (The job number is shown in the url when viewing a job)
- To run a job on travis-ci.org `failrunner -j jobnumber --org`
- To specify manage.py path `failrunner -j jobmnumber -p /path/to/manage/`
- For all cli options `failrunner --help`

# Testing
Use `python -m unittest` to run tests.
