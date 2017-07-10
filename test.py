import pytest

from bigchaindb.common.transaction import Transaction
from bigchaindb_shared import errors, api

"""
The scope of these tests is not to check the functionality in detail,
but to check that basic API contract appears to be in place and does not
randomly break.
"""

pub = 'DD8qvyA6rXSTG4P1ojuFYvXUJ8UHnCy8srWE13xkZdvg'
sec = '4U6vaeue9wtBzkG1ybkShUyMDRgZKEjtQ2CAQQ5PFz67'


def create_tx(msg='hello', outputs=1):
    outputs = [([pub], i+1) for i in range(outputs)]
    return Transaction.create([pub], outputs, asset={'msg': msg}).to_dict()


def test_generate_key_pair():
    gen = lambda: api.generateKeyPair({})
    assert {'public_key', 'secret_key'} == set(gen())
    assert gen() != gen(), 'same pair generated twice'


def test_create_tx():
    res = api.createTx({
        'creator': pub,
        'outputs': [['1', pub]],
        'asset': {'msg': 'hello'}
    })
    assert res == create_tx()


def test_transfer_tx():
    ctx = Transaction.from_dict(create_tx())
    ttx = Transaction.transfer(ctx.to_inputs(), [([pub], 1)], asset_id=ctx.id)
    res = api.transferTx({
        'spends': [ctx.to_dict()],
        'outputs': [['1', pub]],
    })
    assert res == ttx.to_dict()


def test_transfer_with_links():
    ctx = Transaction.from_dict(create_tx(outputs=2))
    ttx = Transaction.transfer(ctx.to_inputs()[1:], [([pub], 2)], asset_id=ctx.id)
    res = api.transferTx({
        'spends': [ctx.to_dict()],
        'links': [{'transaction_id': ctx.id, 'output_index': 1}],
        'outputs': [['2', pub]],
    })
    assert res == ttx.to_dict()


def test_transfer_different_asset_ids_fails():
    with pytest.raises(errors.TxTransferError):
        res = api.transferTx({
            'spends': [create_tx(), create_tx('a')],
            'outputs': [['2', pub]],
        })


def test_transfer_wrong_amount():
    with pytest.raises(errors.TxTransferError):
        res = api.transferTx({
            'spends': [create_tx(), create_tx()],
            'outputs': [['2', pub]],
        })


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
    with pytest.raises(errors.TxInvalid):
        api.validateTx({'tx': tx_bad})

    tx_bad = create_tx()
    tx_bad['id'] += 'a'
    with pytest.raises(errors.TxInvalid):
        api.validateTx({'tx': tx_bad})

    api.validateTx({'tx': create_tx()})


def test_parse_condition_dsl():
    res = api.parseConditionDSL({
        'expr': pub,
    })
    assert res == {
        'details': {
            'type': 'ed25519-sha-256',
            'public_key': pub,
        },
        'uri': 'ni:///sha-256;DNG_jyuIfk5d58p_QXW-suIrpLPshloag4MGABQEovo?fpt=ed25519-sha-256&cost=131072',
    }
    res = api.parseConditionDSL({
        'expr': ('(1 of ' + pub + ')'),
    })
    assert res == {
        'details': {
            'type': 'threshold-sha-256',
            'threshold': 1,
            'subconditions': [{
                'type': 'ed25519-sha-256',
                'public_key': pub 
            }],
        },
        'uri': 'ni:///sha-256;Mhu9nCYOZ2Nd6CagNAaTpF0wy6u1VfrRXaypbNs8WI4?fpt=threshold-sha-256&cost=132096&subtypes=ed25519-sha-256',
    }


def test_parse_condition_dsl_fail():
    with pytest.raises(errors.TxConditionParseError):
        api.parseConditionDSL({
            'expr': 'fds',
        })


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


# TODO: test verify CC uris, public keys
