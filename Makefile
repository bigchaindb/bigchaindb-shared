so:
	cd ext/bigchaindb-hs; stack init --install-ghc; make so

build:
	docker build --rm=false -t bigchaindb-shared .
	make rebuild

rebuild:
	docker rm -f build-bigchaindb-shared || true
	docker run -v `pwd`:/src --name build-bigchaindb-shared -d bigchaindb-shared sleep infinity
	docker exec build-bigchaindb-shared bash -c 'make so-alt'
	rm -rf dist-so
	docker cp build-bigchaindb-shared:/root/src/ext/bigchaindb-hs/build/dist-so .
