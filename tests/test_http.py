import random
import pytest
import requests

from bigchaindb_shared import errors, api

SERVER = 'http://localhost:9984'
pub = 'DD8qvyA6rXSTG4P1ojuFYvXUJ8UHnCy8srWE13xkZdvg'
sec = '4U6vaeue9wtBzkG1ybkShUyMDRgZKEjtQ2CAQQ5PFz67'


def test_get_path():
    assert 'api' in api.httpGetPath({
        'server': SERVER,
        'path': '/',
    })


def test_404():
    with pytest.raises(errors.Http404NotFound):
        api.httpGetPath({
            'server': SERVER,
            'path': '/a',
        })


def test_connection_fail():
    with pytest.raises(errors.HttpConnectionError):
        api.httpGetPath({
            'server': 'http://127.11.11.11:9999',
            'path': '/',
        })


def test_post_transaction():
    tx = api.createTx({
        'creator': pub,
        'outputs': [["1", pub]],
        'asset': {'r': str(random.random())}
    })
    tx_signed = api.signTx({'tx': tx, 'keys': [sec]})
    res = api.httpPostTx({'server': SERVER, 'tx': tx_signed})
    assert res == tx_signed
