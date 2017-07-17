build-image:
	docker build --rm=false -t bigchaindb-shared .

build:
	docker run -v `pwd`:/src bigchaindb-shared bash -c 'make so-alt'
	rm -rf lib/x86_x64
	cp -r ext/bigchaindb-hs/build/dist-so lib/x86_x64
	cd lib/x86_x64 && ln -s libHS*.so libbigchaindb_shared.so
	python -m bigchaindb_shared dumpErrors bigchaindb_shared/errors.py

test:
	docker run -v `pwd`:/src -w /src bigchaindb-shared bash -c 'pip install -r requirements-dev.txt; pytest -s -v'
