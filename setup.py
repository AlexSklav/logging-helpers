#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup
import versioneer

setup(name='logging-helpers',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Helper functions, etc. for the Python `logging` module.',
      keywords='',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='https://github.com/wheeler-microfluidics/logging-helpers',
      license='BSD',
      packages=['logging_helpers'],
      # Install data listed in `MANIFEST.in`
      include_package_data=True)
