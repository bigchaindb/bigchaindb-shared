try:
    import rapidjson as json
except ImportError:
    import json
import ctypes as ct

from bigchaindb_shared import errors


class API(object):
    def __init__(self, path):
        self.shared_object = ct.cdll.LoadLibrary(path)

    def call_json_rpc(self, method, params):
        request = {'method': method, 'params': params}
        out = self.call_so('jsonRPC', json.dumps(request))
        out = json.loads(out)
        if 'error' in out:
            raise getattr(errors, out['error']['class'])(out['error']['msg'])
        return out['result']

    def call_so(self, name, req):
        _res = [None]
        def cb(data):
            _res[0] = data
        ftype = ct.CFUNCTYPE(None, ct.c_char_p)
        getattr(self.shared_object, name)(req.encode(), ftype(cb))
        return _res[0].decode()

    def __getattr__(self, name):
        return lambda val: self.call_json_rpc(name, val)
