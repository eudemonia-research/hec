#!/usr/bin/env python

from distutils.core import setup

setup(name='hec',
      version='0.0.5',
      description='Encrypt text using bitcoin addresses',
      author='Kitten Tofu',
      author_email='kitten@eudemonia.io',
      url='http://eudemonia.io/',
      packages=['hec'],
      requires=['PyQt5','pycoin', 'pycrypto'],
      scripts=['scripts/hecs.py']
     )
