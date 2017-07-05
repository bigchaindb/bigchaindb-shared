try:
    import rapidjson as json
except ImportError:
    import json
import ctypes as ct
import os.path
import glob
import os


sobase = os.environ.get('BIGCHAINDB_SHARED_PATH') or 'dist-so'
sopath = os.path.join(os.path.dirname(__file__),
                      glob.glob(sobase + '/*.so')[0])

SHARED_OBJECT = ct.cdll.LoadLibrary(sopath)

FTYPE = ct.CFUNCTYPE(None, ct.c_char_p)

def call_so(name, req):
    _res = [None]
    def cb(data):
        _res[0] = data
    getattr(SHARED_OBJECT, name)(req.encode(), FTYPE(cb))
    return _res[0].decode()


class BDBError(Exception):
    pass


def call_json_rpc(method, params):
    request = {'method': method, 'params': params}
    out = call_so('jsonRPC', json.dumps(request))
    out = json.loads(out)
    if 'error' in out:
        raise BDBError(out['error']['code'], out['error']['message'], out['error']['data'])
    return out['result']

