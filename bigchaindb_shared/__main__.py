from __future__ import print_function
import argparse
import os.path
import json
import sys

from bigchaindb_shared import api, errors


parser = argparse.ArgumentParser(
        description='BigchainDB Shared command line interface',
        usage='python -m bigchaindb_shared {method} {json}')

subparsers = parser.add_subparsers(dest="method", metavar='')
methods = api.call_json_rpc('showMethods', {})


for (name, description) in methods['methods']:
    subparser = subparsers.add_parser(name, help=description)
    if name not in {'generateKeyPair'}:
        subparser.add_argument('json', type=json.loads)

dumpErrors = subparsers.add_parser('dumpErrors', help="Write Python exception classes")
dumpErrors.add_argument('path', help="Path to write to")


args = parser.parse_args()

if args.method == 'dumpErrors':
    errors = api.showErrorClasses({})['errors']
    tpl = '\nclass BDBSharedError(Exception):\n    pass'
    for error in errors:
        tpl += '\n\nclass %s(BDBSharedError):\n    pass' % error
    errspath = os.path.dirname(__file__) + '/errors.py'
    open(errspath, 'w').write(tpl)
    print("Wrote", errspath)
else:
    try:
        out = api.call_json_rpc(args.method, getattr(args, 'json', {}))
        print(json.dumps(out))
    except errors.BDBSharedError as e:
        print('%s: %s' % (e.__class__.__name__, e), file=sys.stderr)
        sys.exit(1)
