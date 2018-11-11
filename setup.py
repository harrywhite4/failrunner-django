#!/usr/bin/env python

from distutils.core import setup

setup(
    name='failrunner-django',
    version='0.1',
    packages=['failrunner'],
    description='',
    author='Harry White',
    url='https://github.com/harrywhite4/failrunner-django',
    entry_points={
        'console_scripts': ['failrunner=failrunner.runner:main'],
    },
    install_requires=[
        'requests'
    ]
)