# OPTiMaDe

The Open Databases Integration for Materials Design (OPTiMaDe) consortium aims to make materials databases interoperational by developing a common REST API.

This repository contains the specification of the OPTiMaDe API.

* [optimade.rst](optimade.rst): The API specification.
* [AUTHORS](AUTHORS): List of contributors.
* [optimade.org](https://www.optimade.org): Public OPTiMaDe web site
* [OPTiMaDe wiki](https://github.com/Materials-Consortia/OPTiMaDe/wiki): Information for developers

The subdirectory `schemas/` contains OpenAPI schemas for the main OPTiMaDe API and index meta-database as implemented by the [optimade-python-tools repository](https://github.com/Materials-Consortia/optimade-python-tools).
_Note_: These schemas are an approximation of the full human-readable specification and may be missing certain constraints.
Furthermore, they may not be up to date in the develop branch of this repository.

## For developers

The [master branch of the repository](https://github.com/Materials-Consortia/OPTiMaDe/tree/master) is at the latest release or pre-release version of the specification.
Versions without a version number suffix (alpha, beta, release candidates and similar) indicate a stable release.

The [develop branch of the repository](https://github.com/Materials-Consortia/OPTiMaDe/tree/develop) contains the present in-development version of the specification.

API and client implementations are encouraged to support the latest release or pre-release of the specification.
If this is a pre-release, implementations are also encouraged to support the latest stable release.
