build-image:
	docker build --rm=false -t bigchaindb-shared .

build:
	docker run -v `pwd`:/src bigchaindb-shared bash -c 'make so-alt'
	rm -rf dist-so
	cp -r ext/bigchaindb-hs/build/dist-so .
	python -m bigchaindb_shared writeErrors '{}'

test:
	docker run -v `pwd`:/src -w /src bigchaindb-shared bash -c 'pip install -r requirements-dev.txt; pytest test.py -s -v'
