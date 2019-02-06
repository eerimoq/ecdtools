#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
import re


def find_version():
    return re.search(r"^__version__ = '(.*)'$",
                     open('ecdtools/version.py', 'r').read(),
                     re.MULTILINE).group(1)


setup(name='ecdtools',
      version=find_version(),
      description='Electronic circuit design tools.',
      long_description=open('README.rst', 'r').read(),
      author='Erik Moqvist',
      author_email='erik.moqvist@gmail.com',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'textparser>=0.18.0'
      ],
      test_suite="tests")
