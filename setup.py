#!/usr/bin/env python

from distutils.core import setup

import os.path
cabalfile = os.path.join(os.path.dirname(__file__),
        'ext/bigchaindb-hs/bigchaindb.cabal')
ver = [l.split()[1] for l in open(cabalfile) if l.startswith('version:')][0]


if __name__ == '__main__':
    setup(name='bigchaindb-shared',
          author='BigchainDB Developers',
          author_email='dev@bigchaindb.com',
          version=ver,
          description=
            ('Prebuilt shared object contaning functions to read and '
             'create BigchainDB transactions'),
          packages=['dist-so', 'bigchaindb_shared'],
          py_modules=['bigchaindb_shared'],
          package_data={'dist-so': ['*.so', 'libs/*.so', 'bigchaindb.cabal']},
          url='https://github.com/libscott/bigchaindb-shared/',
    )
