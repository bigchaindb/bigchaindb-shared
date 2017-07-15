# bigchaindb-shared-java

Java frontend for BigchainDB Shared

This code is in an early stage, so it may be a little rough around the edges.

Contributions welcome!

## Getting Started

To use this code in your project, you need to make the `libbigchaindb_shared.so`
file findable by JNA, for example, by passing `-Djna.library.path=lib/x86_x64` to
`java`.

See: https://github.com/java-native-access/jna/blob/master/www/GettingStarted.md

To run the tests in Eclipse, you can configure it via **Run -> Run Configurations...**
as such:

![configuration](https://user-images.githubusercontent.com/125019/28241750-95289254-699a-11e7-8797-f4338d9058da.png)

## API

See [bigchaindb-shared](http://github.com/libscott/bigchaindb-shared).
