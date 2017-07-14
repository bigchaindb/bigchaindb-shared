build-image:
	docker build --rm=false -t bigchaindb-shared .

build:
	docker run -v `pwd`:/src bigchaindb-shared bash -c 'make so-alt'
	rm -rf dist-so
	cp -r ext/bigchaindb-hs/build/dist-so .
	ln -s dist-so/libHS*.so dist-so/bigchaindb.so
	python -m bigchaindb_shared dumpErrors bigchaindb_shared/errors.py

test:
	docker run -v `pwd`:/src -w /src bigchaindb-shared bash -c 'pip install -r requirements-dev.txt; pytest test.py -s -v'
