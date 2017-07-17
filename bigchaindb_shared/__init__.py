import os.path
import os

from bigchaindb_shared import api, errors


default_sopath = os.path.dirname(__file__) + \
        '/lib/x86_64/libbigchaindb_shared.so'
sopath = os.environ.get('BIGCHAINDB_SHARED_PATH') or default_sopath
api = api.API(sopath)
