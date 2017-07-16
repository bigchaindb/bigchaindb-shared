# bigchaindb-shared

BigchainDB Shared is a client library for creating and signing BigchainDB transactions.

It is disributed as a pre-built set of **.so** shared objects built on Ubuntu 16.04 x64. It may work on other platforms that also have a compatable version of libc installed (try it out and let us know).

Already provided language frontends are **Python**, **Java**, plus a **CLI**.

## Quickstart

```shell
git clone --recursive https://github.com/libscott/bigchaindb-shared/
cd bigchaindb-shared
python -m bigchaindb_shared createTx '
{
    "creator":"5UY9Ev2BT2yvSxzuwCrEouqpB1F7ofjhevbTujVaSk2w",
    "outputs":[["1","(1 of 5UY9Ev2BT2yvSxzuwCrEouqpB1F7ofjhevbTujVaSk2w, 3339Ev2BT2yvSxzuwCrEouqpB1F7ofjhevbTujVaSk2w)"]]
}
'
```

## Building

```shell
make build-image
make build
```

## Features

* Easy to use JSON api
* Simple FFI interface - easy to integrate with your language
* High performance binary (x86/64, Debian 8, Ubuntu 16.04 etc)

## FFI

BigchainDB Shared is designed to be trivial to interoperate with other langauges that provide an FFI interface to call `.so` methods. All methods are exposed via a single function called 'jsonRPC'. See `bigchaindb_shared/__init__.py` for an example. Once this interface is implemented, all functions are exposed via a simple JSON protocol.

## CLI

BigchainDB Shared also has a CLI interface, depending only on Python and no additional libraries.

## Methods

### genKeyPair

Generates a key pair using system entropy.

Example: 

```python:
alice = api.generateKeyPair({})
bob = api.generateKeyPair({})
```

### createTx

Make a transaction to create an asset.

Arguments:

* **asset** (optional): JSON payload of asset
* **creator**: Ed25519 public key
* **outputs**: List of amounts and condition specifications
* **metadata** (optional): JSON payload of metadata

Example:

```python
tx_create = api.createTx({
    "asset": {"data": "my first asset"}
    "creator": alice.public_key,
    "outputs": [["30", bob.public_key],["20", alice.public_key]],
    "metadata": {"msg": "hello world"},
})
```

### transferTx

Make a transaction to transfer an asset.

Arguments:

* **spends**: List of transactions to use as inputs
* **links** (optional): List of outputs to use
* **outputs**: List of amounts and condition specifications
* **metadata** (optional): JSON payload of metadata

Example:

```python
tx_transfer = api.transferTx({
    "spends": [tx_create],
    "links": [{"transaction_id": "<ID of tx in `spends`>", "output_index": 1}],
    "outputs": [["11", alice.public_key]],
    "metadata": {"msg": "thanks"}
})
```

### signTx

Sign a transaction

Arguments:

* **tx**: Transaction to be signed
* **key**: Private key

Example:

```python
tx_create_signed = api.signTx({
    "tx": create_tx,
    "key": alice.secret_key
})
```

### validateTx

Validate that a transaction is structurally correct

Arguments:

* **tx**: Transaction to check

Example:

```python
api.validateTx({
    "tx": create_tx_signed
})
```

### parseConditionDSL

Parse a condition signing spec (DSL) into an `output.condition`.

A signing spec can represent a simple ed25519 condition or a complex multi-party condition, eg:

`(1 of <key1>, (2 of <key2, <key3>))`.

Arguments:

* **expr**: Expression to parse

Example:
```python
api.parseConditionDSL({
    "expr": alice.public_key
})

spec = "(2 of " + alice.public_key + ", " + bob.public_key)"
api.parseConditionDSL({
    "expr": spec
})
```

### httpGetTransaction

GET a transaction from bigchaindb server.

Arguments:

* **server**: Base URL of server http interface.
* **txid**: 64 character ID of the transaction to fetch.

Example:
```python
tx = api.httpGetTransaction({
    "server": "http://localhost:9984/",
    "txid": tx_create.id
})
```

### httpGetPath

GET any path from bigchaindb server.

Arguments:

* **server**: Base URL of server http interface.
* **path**: Path of the resource to fetch.

Example:
```python
index = api.httpGetPath({
    "server": "http://localhost:9984/",
    "path": "/"
})
```

### httpPostTransaction

POST a transaction to the server.

Arguments:

* **server**: Base URL of server http interface.
* **tx**: Signed transaction to send.

Example:
```python
api.httpPostTransaction({
    "server": "http://localhost:9984/",
    "tx": tx_create_signed
})
```
