# bigchaindb-shared

BigchainDB Shared is a client library for creating and signing BigchainDB transactions.

It is disributed as a pre-built set of `.so` shared objects targeting Ubuntu 16.04 x64. It may work on other platforms that also have a compatable version of libc installed (try it out and let us know).

## Quickstart

```shell
git clone --recursive https://github.com/libscott/bigchaindb-shared/
cd bigchaindb-shared
python -m bigchaindb_shared generateKeyPair '{}'
```

## Building

```shell
make build-image
make build
```

## Features

* Easier to use JSON api
* Simple FFI interface - easy to integrate with your language
* High performance binary (x86/64, Debian 8, Ubuntu 16.04 etc)

## FFI

See `bigchaindb_shared/__init__.py` for an example.

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
