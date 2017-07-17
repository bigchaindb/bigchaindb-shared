#!/usr/bin/env python

from setuptools import setup


setup(name='bigchaindb-shared',
      author='BigchainDB',
      author_email='dev@bigchaindb.com',
      version='0.1.0a1',
      description=
        ('Prebuilt shared object contaning functions to read and '
         'create BigchainDB transactions'),
      url='https://github.com/bigchaindb/bigchaindb-shared/',
      license="Apache Software License 2.0",
      packages=['bigchaindb_shared'],
      package_data={'bigchaindb_shared': ['lib/*/*.so', 'lib/*/libs/*.so']},
      test_suite='tests',
)
