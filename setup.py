#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='waldo-match',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'opencv-contrib-python==3.4.1.15',
        'imutils==0.4.6',
        'numpy==1.14.5'
    ],
    scripts=['waldo-match/match.py'],
)
