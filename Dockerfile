FROM python:3.6
LABEL maintainer "dev@bigchaindb.com"
RUN apt-get update && apt-get install -y libgmp-dev
RUN curl -sSL https://get.haskellstack.org/ | sh
RUN mkdir -p /src/
COPY . /src
WORKDIR /src
RUN cd ext/bigchaindb-hs && stack setup --install-ghc && stack build
