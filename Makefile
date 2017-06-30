
test:
	test-python

test-python:
	pytest -s -x python/tests

so:
	cd ext/bigchaindb-hs && make so

build-container:
	docker build --rm=false .
