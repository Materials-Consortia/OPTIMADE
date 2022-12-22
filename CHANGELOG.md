# Changelog

## v1.2.0-rc.1 (December 2022)

This is the first release candidate of v1.2.0 of the OPTIMADE API specification.
It should contain all of the new features in the specification, but their implementation may be modified in the final release.

Note: The OpenAPI schemas distributed in `./schemas` have not yet been modified with the new features 1.2.0.

This minor release adds significant but optional new functionality to the specification, as well as providing several clarifications to existing behaviour.

### New features

- **Property definitions** ([#376](https://github.com/Materials-Consortia/OPTIMADE/pull/376)).
A new section titled [Property Defintions](https://github.com/Materials-Consortia/OPTIMADE/blob/develop/optimade.rst#property-definitions) has been added to the specification which significantly extends the way in which implementations can define and describe the custom properties they serve, including URIs, unit definitions, API support levels (for querying and sorting) as well as full support for JSON Schema constructs for describing the JSON representation of the property.
- **Files endpoint** ([#360](https://github.com/Materials-Consortia/OPTIMADE/pull/360)).
The `/files` endpoint and corresponding [`files` entry
type](https://github.com/Materials-Consortia/OPTIMADE/blob/develop/optimade.rst#files-entries) has been added to provide a robust way of linking entries to arbitrary file-based data relevant to the entry, such as alternative crystal structure representation formats, input or output files from computational procedures, or experimental data files.
- **Boolean values** ([#348](https://github.com/Materials-Consortia/OPTIMADE/pull/348)).
[Boolean values](https://github.com/Materials-Consortia/OPTIMADE/blob/develop/optimade.rst#comparisons-of-boolean-values) were overlooked in the first version of the filter grammar as no OPTIMADE fields required them.
This functionality has been introduced for boolean fields using the syntax `TRUE` and `FALSE`.
Only strict equality (`=`) and inequality (`!=`) comparisons on individual fields are supported.
- **Fuzzy comparisons on lists** ([#415](https://github.com/Materials-Consortia/OPTIMADE/pull/415))
String comparisons like `CONTAINS`, `STARTS WITH` and `ENDS WITH` are now compatible with list filter operations like `HAS`, `HAS ALL` etc.
- **Backoff time** ([#411](https://github.com/Materials-Consortia/OPTIMADE/pull/411)):
- **Database licenses** ([#414](https://github.com/Materials-Consortia/OPTIMADE/pull/414)):
- **Symmetry data** ([#405](https://github.com/Materials-Consortia/OPTIMADE/pull/405)):


## v1.1.0 (July 8, 2021)

This is release v1.1.0 of the OPTIMADE API specification.

This is a minor release that primarily patches minor specification errors and introduces one new feature.

### New features

- The `implementation` field of the general `meta` response has been updated to include an `issue_tracker` field ([#339](https://github.com/Materials-Consortia/OPTIMADE/pull/339)).

### Patches

- The `mass` field of the `species` attribute for the `structures` entry type has been updated from a float to a list of floats ([#344](https://github.com/Materials-Consortia/OPTIMADE/pull/344)).
    - This was deemed a specification bug that now is fixed in both the specification text and the schemas.
    - Note: this could constitute a breaking change for software implemented to strictly adhere to the v1.0.0 specification.
- The specification text has been clarified in several places without change of intended meaning.
- Multiple typos, grammatical errors, and incorrect API examples have been fixed.
- The OpenAPI schemas are now fully compliant with the Swagger validator.

## v1.0.1 (July 28, 2021)

This is release v1.0.1 of the OPTIMADE API specification.

This release contains all of the patches from [v1.1.0](https://github.com/Materials-Consortia/OPTIMADE/releases/tag/v1.1.0), whilst maintaining compatibility with v1.0.0.

## v1.0.0 (July 1, 2020)

This is release v1.0.0 of the OPTIMADE API specification.
