FROM python:3.6
LABEL maintainer "dev@bigchaindb.com"
RUN apt-get update && apt-get install -y libgmp-dev chrpath
# TODO: Fix stack version
RUN curl -sSL https://get.haskellstack.org/ | sh
COPY . /src/
WORKDIR /src/ext/bigchaindb-hs
RUN make so

