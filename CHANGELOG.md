# Changelog

## v1.3.0-rc.1 (November 2025)

This release extends the OPTIMADE specification with new entry types and properties with an emphasis on applying the partial data protocol from v1.2 to the new trajectories endpoint, for which each resource is likely to be too large to be served in a single response.

As part of this release, the OPTIMADE consortium also adopts the Contributor Covenant (3.0) Code of Conduct for all community interactions.
Please see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details of the contributor expectations, as well as reporting and enforcement procedures.

Minor OPTIMADE releases are always intended to be backwards-compatible for clients, meaning that any client code written for v1.x should continue to work, and any breaking changes should be reported as bugs to be fixed in a patch v1.3.x release.

## New features

- **Trajectories endpoint** ([#377](https://github.com/Materials-Consortia/OPTIMADE/pull/377), [#481](https://github.com/Materials-Consortia/OPTIMADE/pull/481))
): A new trajectories entry type has been added to the specification to share data belonging to ordered sequences of structures, such as those arising from molecular dynamics simulations or geometry optimizations.
    In order to handle large individual entries, this endpoint makes use of the partial data protocol introduced in v1.2, with additional specialisations for slicing (e.g., the `dimension_slices` URL parameter) and representing dimensions that remain constant throughout a trajectory, whilst retaining the ability to filter using the normal OPTIMADE syntax via the `reference_frame` field.
- **Provider-specific data types** ([#560](https://github.com/Materials-Consortia/OPTIMADE/pull/560)): Providers and namespaces can now define custom data types for their properties that let them use specific query semantics that differ from the standard OPTIMADE data types.
  For example, a provider could define a field that uses a string format for a field, but a custom data type that allows for e.g., `CONTAINS` queries to do something other than pure substring matching.
- **New fields for structures entries (`fractional_site_positions`, `site_coordinate_span`, `site_coordinate_span_description`, `optimization_type`, `wyckoff_positions`)**
  ([#539](https://github.com/Materials-Consortia/OPTIMADE/pull/539), [#562](https://github.com/Materials-Consortia/OPTIMADE/pull/562), [#570](https://github.com/Materials-Consortia/OPTIMADE/pull/570)): Several new fields have been added to the structures entry type to improve symmetry representation and to provide information about the provenance of the structure:
  - `fractional_site_positions`, `site_coordinate_span`, `site_coordinate_span_description`: New fields that can be used to describe positions of atoms as an alternative to `cartesian_site_positions`, to be used in conjunction with `space_group_symmetry_operations_xyz` when providing only the asymmetric unit of a structure.
    The additional `site_coordinate_span` and `site_coordinate_span_description` fields can be used to describe the extent of the atoms that have been provided as fractional coordinates and can take values such as `asymmetric_unit`, `unit_cell`, `molecular_entities`, etc.
  - `wyckoff_positions`: This field can be used to provide the Wyckoff positions of each site in the structure, if known, following the IUCr definitions of labelling.
  - `optimization_type`: This field can be used to describer the type of optimization that has been performed on a structure, if any.
    For example, the optimization could be relative to experimental evidence (`experimental`) (e.g., minimising discrepancy with a diffraction pattern), relative to some kind of Hamiltonian (e.g., density-funtional theory or a force-field), and whether the optimisation scope was `local` or in some sense `global` (minimised relative to a global energy surface of possible decompositions and other structural configurations).
- **JSONLines standardization for serializing OPTIMADE APIs to disk** ([#531](https://github.com/Materials-Consortia/OPTIMADE/pull/531)): An appendix has been added to the specification with a suggestion for how to serialize OPTIMADE entries, or full APIs (including e.g., info endpoints) to a single file using the [JSONLines format](https://jsonlines.org/).
  This format is already in-use by several tools in the ecosystem and is RECOMMENDED for interoperability.
- **Extended filtering on relationships** ([#524](https://github.com/Materials-Consortia/OPTIMADE/pulls/524), [#523](https://github.com/Materials-Consortia/OPTIMADE/pull/523)):
  Additional metadata fields describing relationships between entries (`description` and `role`) have been added between all entry types.
  An additional dummy field `target` has been added to enable direct querying (i.e., without requiring a join) on properties of the target of a relationship, for example: `/structures?filter=references.target.doi="10.1234/56789"`.
  In addition, relationships specifically between `files` and `calculations` entries can now specify a `role` that describes whether the file is an `input`, `output`.


## v1.2.0 (June 2024)


This release adds significant but optional new functionality to the specification; it also provides several clarifications to existing behaviour.

Minor OPTIMADE releases are always intended to be backwards-compatible for clients, meaning that any client code written for v1.1 should continue to work.
Although the majority of features added in this release are optional for servers, there are a couple of mandatory format additions that are discussed below in the notes for implementations.
We have clarified our approach to versioning explicitly in the specification under [Versioning of this standard](https://github.com/Materials-Consortia/OPTIMADE/blob/v1.2.0/optimade.rst#versioning-of-this-standard).

For a more academic summary of the changes, please see our paper: [10.1039/D4DD00039K](https://doi.org/10.1039/D4DD00039K).

In addition to the specification document itself, machine-readable schemas from this repository can now be found hosted at [schemas.optimade.org](https:///schemas.optimade.org), and HTML builds of the specification can be found at [specification.optimade.org](https://specification.optimade.org).

### New features

- **Property definitions** ([#376](https://github.com/Materials-Consortia/OPTIMADE/pull/376)): A new section titled [Property Definitions](https://github.com/Materials-Consortia/OPTIMADE/blob/v1.2.0/optimade.rst#property-definitions) has been added to the specification which significantly extends the way in which implementations can define and describe the custom properties they serve, including URIs, unit definitions, API support levels (for querying and sorting) as well as full support for JSON Schema constructs for describing the JSON representation of the property. These definitions form the basis of a new machine-readable form of the OPTIMADE specification found in the main repository and served at [schemas.optimade.org](https://schemas.optimade.org).
- **Namespace prefixes for definitions** ([#473](https://github.com/Materials-Consortia/OPTIMADE/pull/473)): The mechanism for providers to define custom properties under their own namespace/prefix has been extended to allow implementations to share common definitions. These so-called definition namespaces can be registered as providers in their own right and can serve property definitions in the new format.
- **Partial data** ([#467](https://github.com/Materials-Consortia/OPTIMADE/pull/467)): Adds a mechanism and format for streaming, paginating or slicing individual properties within entries.
- **Per entry/property metadata** ([#463](https://github.com/Materials-Consortia/OPTIMADE/pull/463)): Added a mechanism for providing metadata specific to a given entry or property.
- **Files endpoint** ([#360](https://github.com/Materials-Consortia/OPTIMADE/pull/360)): The [`files` entry type](https://github.com/Materials-Consortia/OPTIMADE/blob/v1.2.0/optimade.rst#files-entries) has been added to provide a robust way of linking entries to arbitrary file-based data relevant to the entry, such as alternative crystal structure representation formats, input or output files from computational procedures, or experimental data files.
- **Symmetry operation specification and space group fields** ([#480](https://github.com/Materials-Consortia/OPTIMADE/pull/480), [#405](https://github.com/Materials-Consortia/OPTIMADE/pull/405), [#464](https://github.com/Materials-Consortia/OPTIMADE/pull/464)): Several fields have been added to the `structures` entry type to fully describe symmetry. Symmetry operations can be provided explicitly in `space_group_symmetry_operations_xyz`, as well as space group specifications in various forms: `space_group_symbol_hall`, `space_group_symbol_hermann_mauguin`, `space_group_symbol_hermann_mauguin_extended`, `space_group_it_number`.
- **Database licenses** ([#414](https://github.com/Materials-Consortia/OPTIMADE/pull/414),[#497](https://github.com/Materials-Consortia/OPTIMADE/pull/497)): Several fields have been added to programmatically describe the licensing status of data served by OPTIMADE APIs. A database-wide license can be provided as a set of [SPDX identifiers](https://spdx.org/licenses/) in `available_licenses`, with a related field `available_licenses_for_entries` specifying specifically which licenses apply to individual entries and other non-substantial extracts from the database for cases where these differ from the database-wide licenses. The global field `license` can be used point to a human-readable license page (external or otherwise) that explains any caveats to the licensing arrangement.
- **Database metadata field** ([#424](https://github.com/Materials-Consortia/OPTIMADE/pull/424)): Added an additional metadata field `database` for providing a human-readable description of a given database.
- **Backoff time** ([#411](https://github.com/Materials-Consortia/OPTIMADE/pull/411)): Databases can now request ahead of time that clients apply a particular rate limit or back-off time via the `request_delay` metadata field.

### Patches

- **Fuzzy comparisons on lists** ([#415](https://github.com/Materials-Consortia/OPTIMADE/pull/415)):
String comparisons like `CONTAINS`, `STARTS WITH` and `ENDS WITH` are now compatible with list filter operations like `HAS`, `HAS ALL` etc.
- **Boolean values** ([#348](https://github.com/Materials-Consortia/OPTIMADE/pull/348)):
[Boolean values](https://github.com/Materials-Consortia/OPTIMADE/blob/v1.2.0/optimade.rst#comparisons-of-boolean-values) were overlooked in the first version of the filter grammar as no OPTIMADE fields required them.
This functionality has been introduced for boolean fields using the syntax `TRUE` and `FALSE`.
Only strict equality (`=`) and inequality (`!=`) comparisons on individual fields are supported.
- **Compatibility with JSON:API v1.1** ([#461](https://github.com/Materials-Consortia/OPTIMADE/pull/461)): References to JSON:API v1.0 have been updated to v1.1.
- Typo, formatting and code snippet fixes.

### Notes for implementations

As discussed above, the majority of this release involves the addition of more expressive metadata fields for property definitions, definition namespaces shared across providers, and licensing information, as well as mechanisms for serving files and partial data responses (for large entries, e.g., giant structures).
We hope that the machine-readable schemas and property definitions now available at [schemas.optimade.org](https://schemas.optimade.org) will make implementing the specification much easier.

The mandatory format changes required to support v1.2 are limited to the following:

- `/info/<entry_type>` endpoints MUST now have a top-level `id` and `type` field, e.g., the `/info/structures` MUST now serve `{"id": "structures", "type": "info"}`. This is for compliance with JSON:API and their previous omission should be treated as a specification bug.
- In cases where a server implementation treats filters on non-prefixed but unknown OPTIMADE fields as errors, implementations MUST update their known property list to handle new fields added to OPTIMADE in this version, such that they can continue to follow the expected behaviour for [Handling unknown property names](https://github.com/Materials-Consortia/OPTIMADE/blob/v1.2.0/optimade.rst#handling-unknown-property-names).


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
