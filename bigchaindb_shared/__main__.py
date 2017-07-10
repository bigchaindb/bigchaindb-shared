import os.path
import json
import sys

from bigchaindb_shared import api


method = sys.argv[1]
if method == 'writeErrors':
    errors = api.showErrors({})['errors']
    tpl = '\nclass BDBSharedError(Exception):\n    pass'
    for error in errors:
        tpl += '\n\nclass %s(BDBSharedError):\n    pass' % error
    open(os.path.dirname(__file__) + '/errors.py', 'w').write(tpl)
else:
    print(json.dumps(api.call_json_rpc(method, json.loads(sys.argv[2]))))
