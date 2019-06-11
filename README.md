# OPTiMaDe

The aim of OPTiMaDe is to make materials databases
interoperational. This repository contains the specification of a
general common API for retrieving data from materials databases.

* [optimade.md](optimade.md): The API specification.
* [AUTHORS](AUTHORS): List of contributors.

## For developers

The latest "stable" version of the specification is found in the [master](https://github.com/Materials-Consortia/OPTiMaDe/tree/master) branch.  
The latest "in development" version is found in the [develop](https://github.com/Materials-Consortia/OPTiMaDe/tree/develop) branch.

If you are a **server** developer, it is _mandated_ to always implement the latest stable version, while it is _recommended_ to implement the latest version in development.
This may be achieved by having a _master_ and _develop_ structure for your implementation, similar to the one used here.

If you are a **client** developer, you are _encouraged_ to support at least the latest stable version, while it is _recommended_ to support the latest version in development.
This may be achieved by having a _master_ and _develop_ structure for your client code, similar to the one used here.
