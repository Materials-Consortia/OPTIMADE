<div align="center" style="padding-bottom: 1em;">
<img width="100px" align="center" src="https://matsci.org/uploads/default/original/2X/b/bd2f59b3bf14fb046b74538750699d7da4c19ac1.svg">
</div>

<h1 align="center">
The OPTIMADE Specification
</h1>


The Open Databases Integration for Materials Design (OPTIMADE) consortium aims to make materials databases interoperational by developing a common REST API.

This repository contains the specification of the OPTIMADE API.

* [optimade.rst](optimade.rst): The API specification.
* [AUTHORS](AUTHORS): List of contributors.
* [CHANGELOG](CHANGELOG.md): The release notes for each version of the specification.
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

## Licensing of the unit definitions database `definitions.units`

The OPTIMADE standard refers to a specific version of the `definitions.units` database included with the source distribution of GNU Units.
This file is included in the OPTIMADE repository under the subdirectory [standards/GNU_Units](standards/GNU_Units).
The file is licensed separately from other files in the repository: it is available under the GNU General Public License (GPL).
Full information on how the file is licensed is available in the [header of the file](standards/GNU_Units/definitions.units) and the license file included in that directory, [COPYING](standards/GNU_Units/COPYING).

The following does not constitute legal advice; however, we believe implementations under other licenses can use this file if:

- The file is distributed separated from other source files in a way that makes it clear that it is part of the GNU Units software and is licensed under the GPL.
  (For example, as done in this repository: in a separate subdirectory with its own readme and license files.)

- The software reads the file during program execution, e.g., at startup (as opposed to, e.g., having the file compiled or linked into a binary program distributed to end users).

Alternatively, the software using the file could itself be licensed in a way compatible with the GNU GPL.

## How to cite

If you use OPTIMADE to access or host data, we kindly ask that you cite our paper:

- Andersen *et al*, OPTIMADE, an API for exchanging materials data, *Sci. Data* **8**, 217 (2021) [10.1038/s41597-021-00974-z](https://doi.org/10.1038/s41597-021-00974-z)

To cite an individual version of the specification, please use the versioned records on Zenodo:

- Andersen *et al*, The OPTIMADE Specification, *Zenodo*, [10.5281/zenodo.4195050](https://doi.org/10.5281/zenodo.4195050)
