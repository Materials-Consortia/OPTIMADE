# OPTIMADE

The Open Databases Integration for Materials Design (OPTIMADE) consortium aims to make materials databases interoperational by developing a common REST API.

This repository contains the specification of the OPTIMADE API.

* [optimade.rst](optimade.rst): The API specification.
* [AUTHORS](AUTHORS): List of contributors.
* [optimade.org](https://www.optimade.org): Public OPTIMADE web site
* [OPTIMADE wiki](https://github.com/Materials-Consortia/OPTIMADE/wiki): Information for developers

The subdirectory `schemas/` contains OpenAPI schemas for the main OPTIMADE API and index meta-database as implemented by the [optimade-python-tools repository](https://github.com/Materials-Consortia/optimade-python-tools).
_Note_: These schemas are an approximation of the full human-readable specification and may be missing certain constraints.
Furthermore, they may not be up to date in the develop branch of this repository.

## For developers

The [master branch of the repository](https://github.com/Materials-Consortia/OPTIMADE/tree/master) is at the latest release or pre-release version of the specification.
Versions without a version number suffix (alpha, beta, release candidates and similar) indicate a stable release.

The [develop branch of the repository](https://github.com/Materials-Consortia/OPTIMADE/tree/develop) contains the present in-development version of the specification.

API and client implementations are encouraged to support the latest release or pre-release of the specification.
If this is a pre-release, implementations are also encouraged to support the latest stable release.

## How to cite

Pending the publication of an OPTIMADE paper, we kindly ask that you cite the preprint and Zenodo archive for this repository:

- Andersen *et al*, OPTIMADE: an API for exchanging materials data, arXiv:2103.02068 https://arxiv.org/abs/2103.02068
- Andersen *et al*, The OPTIMADE Specification, https://doi.org/10.5281/zenodo.4195050
