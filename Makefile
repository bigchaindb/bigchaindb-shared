build:
	docker build --rm=false -t bigchaindb-shared .
	make rebuild

rebuild:
	docker run -v `pwd`:/src bigchaindb-shared bash -c 'make so-alt'
	rm -rf dist-so
	cp -r ext/bigchaindb-hs/build/dist-so .
