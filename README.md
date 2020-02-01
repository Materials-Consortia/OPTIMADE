# OPTiMaDe

The Open Databases Integration for Materials Design (OPTiMaDe) consortium aims to make materials databases interoperational by developing a common REST API.

This repository contains the specification of the OPTiMaDe API.

* [optimade.rst](optimade.rst): The API specification.
* [AUTHORS](AUTHORS): List of contributors.
* [optimade.org](https://www.optimade.org): Public OPTiMaDe web site
* [OPTiMaDe wiki](https://github.com/Materials-Consortia/OPTiMaDe/wiki): Information for developers

## For developers

The [master branch of the repository](https://github.com/Materials-Consortia/OPTiMaDe/tree/master) is supposed to be at the latest named release of the specification.
A commit tagged with a version number without a suffix indicates a stable release.
A commit tagged with the suffix `-rc<number>` indicates a release candidate version. 

The [develop branch of the repository](https://github.com/Materials-Consortia/OPTiMaDe/tree/develop) contains the present in-development version of the specification.

API and client implementations are RECOMMENDED to implement the lastest named release.
If the latest named release is a release candidate, it is also RECOMMENDED that they implement the latest stable release.
