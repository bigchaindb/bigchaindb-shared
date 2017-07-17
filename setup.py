#!/usr/bin/env python

from setuptools import setup


setup(name='bigchaindb-shared',
      author='BigchainDB Developers',
      author_email='dev@bigchaindb.com',
      version='0.1.0a1',
      description=
        ('Prebuilt shared object contaning functions to read and '
         'create BigchainDB transactions'),
      packages=['bigchaindb_shared'],
      py_modules=['bigchaindb_shared'],
      package_data={'bigchaindb_shared': ['lib/*/*.so', 'lib/*/libs/*.so']},
      url='https://github.com/libscott/bigchaindb-shared/',
)
