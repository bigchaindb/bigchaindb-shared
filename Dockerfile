FROM python:3.6
LABEL maintainer "dev@bigchaindb.com"

# System dependencies
# chrpath is for preparing the .so files for distribution and
# libgmp-dev is required by ghc
RUN apt-get update && apt-get install -y libgmp-dev chrpath
RUN curl -sSL https://get.haskellstack.org/ | sh
# TODO: Fix stack version

# Copy the current code. If stack resolver or project layout is changed, the image
# will need to be re-built.
COPY . /src/

# Run stack setup, and install project dependencies. This does not build the project,
# but does cache the majority of dependencies in /root/.stack, so that building is much
# faster.
WORKDIR /src/ext/bigchaindb-hs
RUN stack setup
RUN stack install --only-dependencies

