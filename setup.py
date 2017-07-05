#!/usr/bin/env python

from distutils.core import setup

import os.path
cabalfile = os.path.join(os.path.dirname(__file__),
        'ext/bigchaindb-hs/bigchaindb.cabal')
ver = [l.split()[1] for l in open(cabalfile) if l.startswith('version:')][0]

setup(name='bigchaindb-shared',
      version=ver,
      description='Prebuilt shared object contaning functions to read and create BigchainDB transactions',
      author='BigchainDB Developers',
      author_email='scott@bigchaindb.com',
      url='https://github.com/libscott/bigchaindb-shared/',
      py_modules=['bigchaindb_shared'],
      packages=['dist-so'],
      package_data={'dist-so': ['*.so', 'libs/*.so', 'bigchaindb.cabal']},
)
