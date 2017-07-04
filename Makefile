
test:
	test-python

test-python:
	pytest -s -x python/tests

so:
	cd ext/bigchaindb-hs; stack init --install-ghc; make so

build-container:
	docker build --rm=false .
	docker run -v `pwd`:/src --name shared -d f31fbb09d32e sleep infinity
	docker exec shared bash -c 'rm -rf /root/src; cp -r /src/ /root/src; cd /root/src; make so'
