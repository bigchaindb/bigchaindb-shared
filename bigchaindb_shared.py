try:
    import rapidjson as json
except ImportError:
    import json
import ctypes as ct
import os.path
import glob
import sys
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


def call_json_rpc(method, params):
    request = {'method': method, 'params': params}
    out = call_so('jsonRPC', json.dumps(request))
    out = json.loads(out)
    if 'error' in out:
        raise ERRORS[out['error']['class']](out['error']['msg'])
    return out['result']


class BDBSharedException(Exception):
    pass


ERRORS = {}

for name in call_json_rpc('showErrors', {})['errors']:
    globals()[name] = ERRORS[name] = type(name, (BDBSharedException,), {})


if __name__ == '__main__':
    print(json.dumps(call_json_rpc(sys.argv[1], json.loads(sys.argv[2]))))
