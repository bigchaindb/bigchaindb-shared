import pytest

from bigchaindb.common.transaction import Transaction
from bigchaindb_shared import call_json_rpc, BDBError


"""
The scope of these tests is not to check the functionality in detail,
but to check that basic API contract appears to be in place and does not
randomly break.
"""


pub = 'DD8qvyA6rXSTG4P1ojuFYvXUJ8UHnCy8srWE13xkZdvg'
sec = '4U6vaeue9wtBzkG1ybkShUyMDRgZKEjtQ2CAQQ5PFz67'


def create_tx():
    return Transaction.create([pub], [([pub], 1)], asset={'msg': 'hello'}).to_dict()


def test_generate_key_pair():
    assert {'public_key', 'secret_key'} == set(api.generateKeyPair({}))


def test_create_tx():
    res = api.createTx({
        'creator': pub,
        'outputs': [['1', pub]],
        'asset': {'msg': 'hello'}
    })
    assert res == create_tx()


def test_sign_tx():
    tx = create_tx()
    signed = api.signTx({
        'tx': tx,
        'key': sec,
    })
    assert signed == Transaction.from_dict(tx).sign([sec]).to_dict()


def test_validate_tx():
    tx_bad = create_tx()
    del tx_bad['asset']
    try:
        api.validateTx({'tx': tx_bad})
        assert False
    except BDBError as e:
        assert e.args[0] == 100


    tx_bad = create_tx()
    tx_bad['id'] += 'a'
    try:
        api.validateTx({'tx': tx_bad})
        assert False
    except BDBError as e:
        assert e.args[0] == 100

    api.validateTx({'tx': create_tx()})


def test_parse_condition_dsl():
    res = api.parseConditionDSL({
        'expr': 'DD8qvyA6rXSTG4P1ojuFYvXUJ8UHnCy8srWE13xkZdvg',
    })
    assert res == {
        'details': {
            'type': 'ed25519-sha-256',
            'public_key': 'DD8qvyA6rXSTG4P1ojuFYvXUJ8UHnCy8srWE13xkZdvg',
        },
        'uri': 'ni:///sha-256;DNG_jyuIfk5d58p_QXW-suIrpLPshloag4MGABQEovo?fpt=ed25519-sha-256&cost=131072',
    }
    res = api.parseConditionDSL({
        'expr': ('(1 of DD8qvyA6rXSTG4P1ojuFYvXUJ8UHnCy8srWE13xkZdvg)'),
    })
    assert res == {
        'details': {
            'type': 'threshold-sha-256',
            'threshold': 1,
            'subconditions': [{
                'type': 'ed25519-sha-256',
                'public_key': 'DD8qvyA6rXSTG4P1ojuFYvXUJ8UHnCy8srWE13xkZdvg'
            }],
        },
        'uri': 'ni:///sha-256;Mhu9nCYOZ2Nd6CagNAaTpF0wy6u1VfrRXaypbNs8WI4?fpt=threshold-sha-256&cost=132096&subtypes=ed25519-sha-256',
    }


def test_parse_condition_dsl_fail():
    try:
        api.parseConditionDSL({
            'expr': 'fds',
        })
        assert False
    except BDBError as e:
        assert e.args[0] == 101


def test_verify_fulfillment():
    tx = create_tx()
    ffill = api.signCondition({
        'keys': [sec],
        'condition': tx['outputs'][0]['condition'],
        'msg': 'hello',
    })
    res = api.verifyFulfillment({
        'fulfillment': ffill,
        'msg': 'hello',
        'condition': tx['outputs'][0]['condition'],
    })
    assert res == {'valid': True}
        
    res = api.verifyFulfillment({
        'fulfillment': ffill,
        'msg': 'wat',
        'condition': tx['outputs'][0]['condition'],
    })
    assert res == {'valid': False}


class API(object):
    def __getattr__(self, name):
        return lambda val: API.call(name, val)
    
    @staticmethod
    def call(name, val):
        return call_json_rpc(name, val)

api = API()
