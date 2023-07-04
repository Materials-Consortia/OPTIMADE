# OPTIMADE Property Definitions

## What is an OPTIMADE property definition?

The section `Property Definitions` of the OPTIMADE specification defines an output format-agnostic way to declare properties that can be communicated via OPTIMADE to describe physical quantities and related data.
The format uses a subset of JSON Schema extended with OPTIMADE-specific identifiers, as allowed by the JSON Schema standard with identifiers prefixed with `x-optimade-`.
Hence, they can be used as schemas to validate data items using standard tools for JSON Schema.
Property Definitions are used in the OPTIMADE API to describe precisely what data a database makes available.
However, they can also be used in other contexts since they can be used to assign stable URI identifiers to such definitions, which can then be used anywhere where there is a need to refer to a specific definition of a data property unambiguously.

As described in more detail below, the OPTIMADE consortium publishes the current and past standardized sets of Property Definitions in subdirectories of the following URL:

  - https://schemas.optimade.org/properties/

Anyone can, of course, publish their own sets of Property Definitions under any URL they like.
See [Editing and contributing Property Definitions](#editing_and_contributing_property_definitions) below for more information.

## Property Definitions in the OPTIMADE repository

The OPTIMADE repository:

- https://github.com/Materials-Consortia/OPTIMADE

contains a subdirectory `schemas/src/properties`, followed by a version number directory, with source files from which the Property Definitions for the standard OPTIMADE properties are generated.
They are organized with one subdirectory per category, of which we presently use:
- `core` for the most core Property Definitions of the OPTIMADE API protocol.
- `optimade` for property definitions integral to the OPTIMADE standard.

The `optimade` category is further partitioned using subdirectories according to OPTIMADE endpoints.
In addition, common definitions reused across the definition source files are sorted in a special subdirectory, `common`.

These directories contain human-readable YAML-formatted property definition source files with `.yaml` extensions.
The source files are processed with the tool `tests/scripts/process_propdefs.py` into standards-conformant JSON files where inline copies of the corresponding definitions replace references to other files to adhere to the OPTIMADE standard format for Property Definitions.

The following makefile target processes all Property Definitions (and other schema definitions, see below) into the output directory `schemas/output`:
```
make schemas
```
The make command also generates documentation in markdown and HTML meant to be keept alongside the JSON definition files.

## Stable Property Definition URIs

Properties standardized by OPTIMADE are given stable URIs that are URLs with the following format:
```
  https://schemas.optimade.org/properties/<version>/<namespace>/<entrytype>/<name>
```
where:

- `<version>` is the property definition version prefixed with a `v`, which is the minor OPTIMADE version in which the property definition was last changed on format "vMAJOR.MINOR", e.g. "v1.2".
- `<namespace>` is a particular namespace for the Property Definitions.
  The namespace `optimade` is used for property definitions that are integral to the OPTIMADE standard.
- `<entrytype>` is the OPTIMADE entry type that the property belongs to in OPTIMADE.
- `<name>` is an identifier of lowercase Latin characters and the underscore character identifying the property.

## Entry type definitions

In OPTIMADE, a set of property definitions defines an entry type.
Machine-readable definition of these entry types are provided similarly to the property definitions with stable URIs that are URLs with the following format:
```
  https://schemas.optimade.org/entrytypes/<version>/<namespace>/<entrytype>
```

## Standards definitions

In OPTIMADE, a set of entry types define a standard.
There presently is only a single standard published by OPTIMADE, which is provided with a stable URI using the following URL:
```
  https://schemas.optimade.org/standards/<version>/<namespace>/optimade
```
(In the future, OPTIMADE may define other standards to differentiate support for different sets of entry types.)

## Unit, constant, and prefix definitions

The OPTIMADE Property Definitions require a careful definition of the physical units of measurement used for properties using references to unit, constant, and prefix definitions.
The format for these definitions is described in the subsection `Physical Units in Property Definitions` of `Property Definitions` in the OPTIMADE specification.

These are also given stable URIs using the following URLs:
```
  https://schemas.optimade.org/units/<version>/<defining organization>/<year>/<category>/<name>
  https://schemas.optimade.org/constants/<version>/<defining organization>/<year>/<category>/<name>
  https://schemas.optimade.org/prefixes/<version>/<defining organization>/<name>
```
They are distinguished according to the following conventions:

- A unit defines a reference for expressing the magnitude of a quantity.
- A constant defines a known measurement, i.e., a specific dimensioned or dimensionless quantity, possibly along with a specified standard uncertainty.
- A prefix defines a dimensionless constant whose symbols are commonly prepended to unit symbols to express a correspondingly rescaled unit.

For example, the Bohr magneton *unit* (defined, e.g., in Rev. Mod. Phys 41, 375 (1969)) is the reference used when expressing a magnetic moment in multiples of the magnetic dipole moment of an electron which orbits an atom in the orbit of lowest energy in the Bohr model.
Various experimentally determined relations of this magnetic moment to the SI base units are represented as constants in OPTIMADE.
For example, one such Bohr magneton constant is the "2018 CODATA recommended value" published in Rev. Mod. Phys. 93, 025010 (2021), which is 9.2740100783(28) x 10^(-24) J/T.
Another is the "1973 CODATA recommended value" published in J. Phys. Chem. Ref. Data 2, 663 (1973), which is 9.274078(36) x 10^(-24) J/T.
It is useful in the Bohr magneton unit definition to use a Bohr magneton constant to express an approximate relationship to the SI base units.

## Other useful URLs

The URIs are URLs that can be retrieved to fetch a human-readable description of the definition in HTML format.
Every URI can also be suffixed with the extension ".json" to obtain the machine-readable JSON definition file.

The URIs with the version number in the format "vMAJOR.MINOR" are stable in the sense that they will always refer to a single specific definition.
However, the definition file may be amended and clarified in ways that do not functionally alter the definition.
When this happens, the version number in the definition file (`x-optimade-definition -> version`) will be updated to match the corresponding release of OPTIMADE.
However, the URI (`$id`) will be retained as long as the definition functionally remains the same.

Historical versions of the definitions are retained unmodified in URLs where the version number takes the format "vMAJOR.MINOR.PATCH", e.g., "v1.2.0", referring to the full version number of the definition.
These are not meant to be used as URIs, since multiple such URLs will refer to what is functionally the same definition.

For simplicity in locating the most recent definitions, the URLs are also available with the version number using the format "vMAJOR", e.g., "v1", as well as just the string "current".
However, these URLs MUST NOT be used as URIs to reference Property Definitions since the definitions they reference may change over time.

Finally, browsable indices of definitions are provided via URLs using the format:
```
https://schemas.optimade.org/<kind>/<version>/index.html
```

## Versioning of definitions

The property definition URIs are meant to be kept as static as possible to improve interoperability.
The properties standardized by OPTIMADE use OPTIMADE version numbers.
The URIs omit the PATCH version number since it is not possible for a definition to functionally change between patch releases.

The exact Property Definition files released as part of a specific version of OPTIMADE are found using the URLs with the version number on the format "vMAJOR.MINOR.PATCH".

For example, a full list of the Property Definitions (including their version numbers) that are part of OPTIMADE release v1.2.0 is found at:
```
  https://schemas.optimade.org/properties/v1.2.0/index.html
```

## Creating database-specific definitions

Database providers may want to use the OPTIMADE repository framework to generate definition files for database-specific properties.
The repository provides a directory `schemas/src/example` to help with this.

The recommended workflow is to copy this directory into a working directory of your own, e.g., `schemas/src/my-database`.
(Note that if you want to change the domain name used for the static URIs "https://example.org/schemas" you need to update the corresponding variable in the Makefile.)

When the content under `schemas/src/example/src` has been edited, executing `make` processes the files into `schemas/src/example/output`.

If you want to host your Property Definitions, use your web server to publish the content under `output` at the appropriate base URL, e.g., `https://example.com/schemas/`.
Note:

- You can give the parameter `schema_html_pretty=true` to the make command to style them.
- You can give the parameter `schema_html_ext=true` to give html extensions also for the HTML files that are meant to be served without extensions.
  Files with extensions are useful for some hosting solutions (e.g., GitHub pages) that automatically forwards URLs without extensions.

## Contributing definitions to OPTIMADE

To propose new definitions, or modifications to existing definitions:

- Clone the OPTIMADE repository from GitHub.

- Compose or edit the YAML files for the definitions under `schemas/src`.
  The format is described in the OPTIMADE standard.
  You can also look at the files in `schemas/example` as examples.

- Execute `make schemas` to process them info `schemas/output`.

If you want to integrate these definitions into the OPTIMADE standard:

- Decide what namespace to use and ensure your definition files are placed in appropriate directories, e.g., `schemas/src/<namespace>/<entrytype>/`.
  Use `optimade` for `<namespace>` to get them included in the central part of the OPTIMADE standard.

- Edit the `$id` fields to use the corresponding locations under `https://schemas.optimade.org/`.

- If you know which future version of the OPTIMADE standard will contain these properties (e.g., because a new release is being worked on in which they will be included), put that version in `$id` (as, e.g., `v1.2`) and `x-optimade-property/version` (as, e.g., `1.2.0`).
  If you do not know, use the placeholder `$${OPTIMADE_VERSION}` in both places; set e.g.: `$id: "https://schemas.optimade.org/properties/v$${OPTIMADE_VERSION}/optimade/example/property"` and `version: "$${OPTIMADE_VERSION}"` in `x-optimade-property`.
  When running `make properties`, this placeholder is substituted with the OPTIMADE version number as written at the top of the specification document, which renders Property Definition output files useful for testing.
  When a new version of the OPTIMADE standard is released, the maintainers are meant to replace these placeholders with the relevant version, which then becomes the permanent version for those definitions.

- Make a GitHub pull request from your repository to the `develop` OPTIMADE repository branch.

When the pull request is merged, the properties will become part of the next release of the OPTIMADE standard and published under `https://schemas.optimade.org/properties/`
