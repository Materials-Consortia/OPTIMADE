# OPTIMADE Property Definitions

## What is an OPTIMADE property definition?

The OPTIMADE standard specifies an output format-agnostic way to declare data properties, with particular support for describing physical quantities and related data.
The format uses a subset of JSON Schema extended with additional OPTIMADE-specific identifiers, as allowed by the JSON Schema standard with identifiers prefixed with `x-optimade`.
Hence, they can be used as schemas to validate data items using standard tools for JSON Schema.
Property Definitions are used in the OPTIMADE API to describe precisely what data a database makes available.
However, they can also be used in other contexts since they allow assigning stable URI identifiers to such definitions, which can be used anywhere there is a need to refer to a specific definition of a data property unambiguously.

As described in more detail below, the OPTIMADE consortium publishes the current and past standardized sets of Property Definitions in subdirectories of the following URL:

  - https://schemas.optimade.org/properties/

You can, of course, publish your own sets of Property Definitions under any URL you like.
See [Editing and contributing Property Definitions](#editing_and_contributing_property_definitions) below for more information.


## Property Definitions in the OPTIMADE repository

The OPTIMADE repository:

- https://github.com/Materials-Consortia/OPTIMADE

contains a subdirectory `properties/src` that contains source files from which to generate Property Definitions for the standard OPTIMADE properties.
They are organized with one subdirectory per namespace, of which we currently only use:
- `core` for the most core Property Definitions of the OPTIMADE API protocol.
- `optimade` for property definitions that are integral to the OPTIMADE standard.

Each namespace, except `core`, has "endpoint" subdirectories to sort the Property Definitions into the endpoints in the OPTIMADE protocol to which they belong.
In addition, common definition references from other definition source files may be sorted in a special subdirectory, `common`.

The endpoint subdirectories contain human-readable YAML-formatted property definition source files.
The source files use JSON Schema pointers to reference other source files to avoid duplication of information.
They are processed with the tool `tests/scripts/process_propdefs.py` into standards-conformant JSON files where JSON Schema pointers are replaced by inline copies of the corresponding definitions to adhere to the OPTIMADE standard format for Property Definitions.

All Property Definitions can be processed in one go into the output directory `properties/output` by using the following makefile target:
```
make properties
```


## Stable Property Definition URIs

Properties standardized by OPTIMADE are given stable URIs that are URLs with the following format:
```
  https://schemas.optimade.org/properties/<version>/<namespace>/<endpoint>/<property id>
```
where:

- `<version>` is the property definition version prefixed with a `v`, which per definition coincides with the full OPTIMADE version in which the property definition was last changed (see below), e.g., `v1.2.0`.
- `<namespace>` is a particular namespace for the Property Definitions.
  The namespace `optimade` is used for property definitions that are integral to the OPTIMADE standard.
- `<endpoint>` is the endpoint to which the property is designated in OPTIMADE.
- `<property id>` is a lowercase identifier that identifies the property.

The following URL references a compound JSON document collecting all Property Definitions that belong to the same endpoint:
```
  https://schemas.optimade.org/properties/<version>/<namespace>/<endpoint>
```
The following URL references a compound JSON document collecting all definitions that belong to all endpoints in a namespace:
```
  https://schemas.optimade.org/properties/<version>/<namespace>
```
A URI used to reference property definitions MUST always use the URL with the full version number, including the major, minor, and patch version segments.


## Other useful URLs

To simplify access to the Property Definitions, all the URLs in the previous section are also available via URLs with less precise version numbers than the stable URIs described in the previous section.
In this case, `<version>` references either a `<major>.<minor>` or just a `<major>` OPTIMADE version number, e.g., `v1.2` or `v1`.
However, these URLs MUST NOT be used as URIs to reference Property Definitions since they will be changed over time to reference the latest respective version.

Note that the `$id` fields in the properties found via these URLs always point to the correct stable URI (i.e., with a `<major>.<minor>.<patch>` version).
Hence, these URLs can be reliably used to locate the correct `$id` for the latest relevant version of a property definition.


## Versioning of Property Definitions

The property definition URIs are meant to be kept as static as possible to improve interoperability.

The properties standardized by OPTIMADE use OPTIMADE version numbers.
However, even in further releases of OPTIMADE, they stay at the precise OPTIMADE patch release in which they were last modified.

Exactly which Property Definitions are part of a specific version of OPTIMADE can be located using the URLs in the preceding section or in the files generated by `make properties`.

For example, a full list of the Property Definitions (including their version numbers) that are part of OPTIMADE release v1.2.0 is found at:
```
  https://schemas.optimade.org/properties/v1.2.0/optimade
```
The same information is also found in the path: `properties/v1.2.0/optimade.json` after executing `make properties` in the OPTIMADE repository.


## Editing and Contributing Property Definitions

To create a new property definition or to propose a modification to an existing definition:

- Compose or edit YAML files for the Property Definitions.
  The definition of the format is published in the OPTIMADE standard.
  You can also look at the files in `properties/src` as examples.
  Make sure to give the Property Definitions appropriate `$id` values as URLs where you plan to host them (see below).

- Place them under appropriate directories in the OPTIMADE repository: `properties/src/<namespace>/<endpoint>/`.

- Execute `make properties`

Your new/changed properties will appear under `properties/output`.
If you want to host your Property Definitions, use your web server to publish the content under `properties/output` under the appropriate base URL, e.g., `https://example.com/properties/`.

If you want to integrate your Property Definitions in the OPTIMADE standard:

- Decide what namespace to use and ensure your definition files are placed in appropriate directories `properties/src/<namespace>/<endpoint>/` in your clone of the OPTIMADE repository.
  Use `optimade` for `<namespace>` to get them included in the central part of the OPTIMADE standard.

- Edit the `$id` fields to use the corresponding locations under `https://schemas.optimade.org/properties/`.

- Use the string `${{version}}` in place of the property definition version.
  When the OPTIMADE standard is released, this will be replaced with the release version number.

- Make a GitHub pull request from your repository to the `develop` OPTIMADE repository branch.

When the pull request is merged, the properties will become part of the next release of the OPTIMADE standard and published under `https://schemas.optimade.org/properties/`
