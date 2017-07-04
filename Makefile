
test:
	test-python

test-python:
	pytest -s -x python/tests

so:
	cd ext/bigchaindb-hs; stack init --install-ghc; make so

docker-build:
	docker build --rm=false -t bigchaindb-shared .
	docker rm -f build-bigchaindb-shared || true
	docker run -v `pwd`:/src --name build-bigchaindb-shared -d bigchaindb-shared sleep infinity
	docker exec shared bash -c 'rm -rf /root/src; cp -r /src/ /root/src; cd /root/src; make so'
	docker cp build-bigchaindb-shared:/root/src/ext/bigchaindb-hs/build/dist-so .
