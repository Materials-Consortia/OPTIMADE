# OPTIMADE Property Definitions and other schemas

## OPTIMADE Property Definitions

The section `Property Definitions` of the OPTIMADE specification defines an output format-agnostic way to declare properties that can be communicated via OPTIMADE to describe physical quantities and related data.
The format uses a subset of JSON Schema extended with OPTIMADE-specific identifiers, as allowed by the JSON Schema standard with identifiers prefixed with `x-optimade-`.
Hence, they can be used as schemas to validate data items using standard tools for JSON Schema.

As described in more detail below, the OPTIMADE consortium publishes the current and past standardized sets of Property Definitions, with an index available at the following URL:

  - https://schemas.optimade.org/defs/

Anyone can, of course, publish their own sets of Property Definitions under any URL they like.
See [Creating database-specific definitions](#creating-database-specific-definitions) and [Contributing standard definitions to OPTIMADE](#contributing-standard-definitions-to-optimade) below for more information.


### Using the definitions

The primary purpose of Property Definitions is to include them in the info endpoint responses in an implementation of the OPTIMADE API to describe precisely what data a database makes available.
For example, the URI IDs in the definitions may tell a client interacting with two databases that these databases communicate the same property in the same way.

However, they can also be used in other contexts since they provide stable URI IDs that unambiguously define both a data format and the meaning of the data represented using that format.
These URIs are user-friendly in the sense they are resolvable URLs that give a human-readable definition of the defined entity.

A researcher who uploads research data in, say, CSV format, to an online data repository (e.g., figshare) can use the Property Definition URIs and/or the JSON definition files to unambiguously communicate the format and content of the cells in the CSV file.
The definitions can be referenced, for example, by using the stable URIs as column headers in the CSV file or by using the definition names as column headers and giving the full URIs in accompanying information (e.g., an attached README file).
The full JSON-formatted definition files can also be included in the upload to make the upload completely self-contained.

Instead of using individual URIs or definition files for each property, it is also possible to instead give the URI to an OPTIMADE entry type or standard definition, which groups multiple Property Definitions.
Since the JSON representations of the definitions always are non-referential (i.e., they contain all the information inline with no references to external definitions), it is safe to include a single JSON file for each entity being referenced (i.e., each property, entry type, or just the one file to reference any set of properties part of the OPTIMADE standard).


### Physical unit definitions

As part of standardizing property definitions, OPTIMADE also includes stable URIs for physical units (see below).
Similarly to the possible use of Property Definitions outside of the OPTIMADE API, the unit definitions may be useful for referring to specific units in other contexts unambiguously.
For example, the stable URIs and/or the JSON definition files can be used in software to carefully communicate exactly the definition of the units of the values being returned.


## Property Definitions in the OPTIMADE repository

The OPTIMADE repository:

- https://github.com/Materials-Consortia/OPTIMADE

contains a subdirectory `schemas/src/defs/`, followed by version number directories, under which source files from which the Property Definitions for the standard OPTIMADE properties are generated.
The primary source files for properties reside under `properties`.
They are organized with one subdirectory per category, of which we presently use:

- `core` for the most core Property Definitions of the OPTIMADE API protocol.
- `optimade` for property definitions integral to the OPTIMADE standard.

The `optimade` category is further partitioned using subdirectories according to OPTIMADE entry types (which correspond to endpoints in the REST API).
In addition, common definitions reused across the definition source files are sorted in a special subdirectory, `common`.

These directories contain YAML-formatted property definition source files with `.yaml` extensions.
The source files are processed with the tool `tests/scripts/process_propdefs.py` into standards-conformant JSON files where inline copies of the corresponding definitions replace references to other files to adhere to the OPTIMADE standard format for Property Definitions.

The following makefile target processes all Property Definitions (and other schema definitions, see below) into the output directory `schemas/output`:
```
make schemas
```
This command also generates documentation in markdown and HTML meant to be keept alongside the JSON definition files.
Once the generation is complete, the property definitions are found under `schemas/output/defs/` using the same directory structure as under `schemas/src`.

You can browse the definitions by starting a browser with the generated index page, e.g.:
```
  firefox schemas/output/defs/index.html
```
The generation places extension-less HTML files alongside the JSON definition files, which this index page links to.
This should work with most browsers.

The `make schemas` commands take two optional parameters:

- `schemas_html_pretty=true` creates html output that is arguably styled more nicely.
- `schemas_html_ext=true` creates files with `.html` extensions also for the HTML files that are meant to be served without extensions.
  To generate the files with these extensions may be useful for some hosting solutions (e.g., GitHub pages) that automatically forward URLs without extensions.
  Unless the files are served using such a solution, links to the definitions (e.g., from the index page) will be broken.


### Stable Property Definition URIs

Properties standardized by OPTIMADE are given stable URIs that are URLs with the following format:
```
  https://schemas.optimade.org/defs/<version>/properties/<namespace>/<entrytype>/<name>
```
where:

- `<version>` is the minor version of the property on format "vMAJOR.MINOR", e.g. "v1.2", which is the minor OPTIMADE version in which the property was created or functionally changed.
  Functionally changed means that the definition of the property is not just amended or clarified, but altered in a way that changes its interpretation.
  In accordance with [semantic versioning](https://semver.org/), if only the minor version number is increased, the change MUST be backward compatible (e.g., the changed definition may add a non-mandatory field to a dictionary.)
- `<namespace>` is a particular namespace for the Property Definitions.
  The namespace `optimade` is used for property definitions integral to the OPTIMADE standard.
- `<entrytype>` is the OPTIMADE entry type that the property belongs to in OPTIMADE.
- `<name>` is an identifier of lowercase Latin characters and the underscore character identifying the property.

The URIs are URLs that can be retrieved to fetch a human-readable description of the definition in HTML format.
Every URI can also be suffixed with the extension ".json" to obtain the machine-readable JSON definition file.
These URIs are stable in the sense that they will always refer to a single specific definition.
However, the definition description that the URL resolves to may be amended and clarified in ways that do not functionally alter the definition.
When this happens, the version number in the definition file (in the field `x-optimade-definition -> version`) will be updated to match the corresponding release of OPTIMADE.
The URI (and thus the `$id` in the JSON definition) will be retained as long as the definition functionally remains the same.

Historical versions of the definitions are retained unmodified under URLs using the following format:
```
  https://schemas.optimade.org/releases/<full version>/<version>/properties/<namespace>/<entrytype>/<name>
```
where `<full_version>` refers to a version string on the format "vMAJOR.MINOR.PATCH", e.g., "v1.2.0" referring to the full version number of the definition and `<version>` still refers to the format "vMAJOR.MINOR".
These URLs collect all historical versions corresponding to the OPTIMADE release with the same version.
The double URL segments for versions may look redundant.
However, they take this form to keep a complete historical record that preserves any amendments and clarifications of the older definition files.


### Entry type definitions

In OPTIMADE, an entry type consists of a set of property definitions.
Machine-readable definition of these entry types are provided analgous to the property definitions with stable URIs that are URLs and historical URLs with the following formats:
```
  https://schemas.optimade.org/defs/<version>/entrytypes/<namespace>/<entrytype>
  https://schemas.optimade.org/releases/<full version>/entrytypes/<namespace>/<entrytype>
```
The corresponding source files are found in the OPTIMADE repository in `schemas/output/defs/<version>/entrytypes`.


### Standards definitions

A set of entry types can be bundled to define a standard.
There is presently only a single standard published by OPTIMADE, which is provided with a stable URI and historical URL with the following formats:
```
  https://schemas.optimade.org/defs/<version>/standards/optimade
  https://schemas.optimade.org/releases/<full version>/standards/optimade
```
(In the future, OPTIMADE may use this feature for implementations to be able to indicate the support of data beyond what is included in the core optimade standard.)


### Unit, constant, and prefix definitions

To support the definition of properties, OPTIMADE also provide definition files for units, constants, and prefixes under the corresponding subdirectories of `schemas/src/defs/<version>`.
The format for these definitions is described in the subsection `Physical Units in Property Definitions` of `Property Definitions` in the OPTIMADE specification.

These are also given stable URIs using the following URLs:
```
  https://schemas.optimade.org/defs/<version>/units/<defining organization>/<year>/<category>/<name>
  https://schemas.optimade.org/defs/<version>/constants/<defining organization>/<year>/<category>/<name>
  https://schemas.optimade.org/defs/<version>/prefixes/<defining organization>/<name>
```
They are distinguished according to the following conventions:

- A unit defines a reference for expressing the magnitude of a quantity.
- A constant defines a known measurement, i.e., a specific dimensioned or dimensionless quantity, possibly along with a specified standard uncertainty.
- A prefix defines a dimensionless constant whose symbols are commonly used prepended to unit symbols to express a correspondingly rescaled unit.

For example, the Bohr magneton *unit* (defined, e.g., in Rev. Mod. Phys 41, 375 (1969)) refers to the reference magnetic moment used to express a measure in multiples of the magnetic dipole moment of an electron which orbits an atom in the orbit of lowest energy in the Bohr model.
Various experimentally determined relations of this magnetic moment to the SI base units are represented as constants in OPTIMADE.
For example, one such Bohr magneton constant is the "2018 CODATA recommended value" published in Rev. Mod. Phys. 93, 025010 (2021), which is 9.2740100783(28) x 10^(-24) J/T.
Another is the "1973 CODATA recommended value" published in J. Phys. Chem. Ref. Data 2, 663 (1973), which is 9.274078(36) x 10^(-24) J/T.
The Bohr magneton constants can be used to express an approximate relationship between the Bohr magneton unit and the SI base units.

Analogous to how property definitions are grouped into entry types and standards, unit, constant and prefix definitions are grouped into unit systems.
Unit systems are accssible using URIs and historical URLs with the following formats:
```
  https://schemas.optimade.org/defs/<version>/unitsystems/<defining organization>/<name>
  https://schemas.optimade.org/releases/<full version>/unitsystems/<defining organization>/<name>
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


## JSON-Schema for OPTIMADE response validation

The definition files under `schemas/src/defs` are used in combination with supplied [JSON Schema](https://json-schema.org/) schemas for [JSON:API](https://jsonapi.org/) to generate JSON Schema files that can validate OPTIMADE responses.
The corresponding source file is found in `schemas/src/json-schema/<version>/optimade.yaml`.
After generating the schemas with `make schemas`, the generated JSON Schema is found in `schemas/output/json-schema/<version>/optimade.json`.


## JSON-LD definitions

The definition files under `schemas/src/defs` are also used to generate definition files for [JSON-LD](https://json-ld.org/) that can be used to annotate JSON:API-formatted responses from OPTIMADE so that the containing data is compatible with JSON-LD.
The corresponding source file is found under `schemas/src/json-ld/<version>`.
After generating the schemas with `make schemas` the generated JSON-LD context and supporting files are found under `schemas/output/json-schema/<version>`.

The JSON-LD context is hosted at:
```
https://schemas.optimade.org/json-ld/<version>/optimade.json
```
For example, if a standard JSON:API-formatted OPTIMADE v1.2 response includes a top-level field `"@context": "https://schemas.optimade.org/json-ld/v1.2/optimade.json"`, the resulting response will be parsable using standard JSON-LD tools.
To generate JSON-LD contexts that include database-specific properties, see [Creating database-specific definitions](#creating_database_specific_definitions) below.


## Creating database-specific definitions

Database providers may want to use the OPTIMADE repository framework for property definitions to generate their own definition files for database-specific properties.
There is a repository provided via OPTIMADE that contains example files for this:

- https://github.com/Materials-Consortia/optimade-property-tools

Please see the instructions provided in the README.md file of that repository.


## Contributing standard definitions to OPTIMADE

To propose new definitions, or modifications to existing definitions:

- Clone the OPTIMADE repository from GitHub.

- Compose or edit the YAML files for the definitions under `schemas/src`.
  The format is described in the OPTIMADE standard.
  You can also look at the files in `schemas/example` as examples.

- Execute `make schemas` to process them info `schemas/output`.

If you want to integrate these definitions into the OPTIMADE standard:

- Decide what namespace to use and ensure your definition files are placed in appropriate directories under `schemas/src/defs/<version>`.
  For proporties to be included in the central part of the OPTIMADE standard, use `optimade` for `<namespace>`.

- Edit the `$id` fields to use the corresponding locations under `https://schemas.optimade.org/`.

- Make a GitHub pull request from your repository to the `develop` OPTIMADE repository branch.

When the pull request is merged, the properties will become part of the next release of the OPTIMADE standard and published under `https://schemas.optimade.org/properties/`


## Updating schemas.optimade.org (for OPTIMADE maintainers)

This is the workflow to update the schemas at `https://schemas.optimade.org/`:

- Make sure to have cloned the OPTIMADE main and schema repositories.

- Execute in the main OPTIMADE repository:
  ```
  make clean
  make schemas schemas_html_pretty=true schemas_html_ext=true
  ```

- From the OPTIMADE repository execute the following command to see what files are about to be uploaded and modified in the schemas repository:
  ```
  rsync -ia --no-t --checksum --dry-run schemas/output/ /path/to/repo/for/schemas/ | tests/scripts/filter_rsync_itemize_output.sh
  ```
  Be careful to include the trailing slash on `schemas/output/`.
  The arguments `--no-t --checksum` makes sure to only update files only if the contents differ (not if only the modification time is different because the files have been regenerated).
  You should see a new release directory being uploaded and only modified files under `defs` for the definitions we have amended or clarified since the previous release, and the occasional update of a version symlink.
  Check that the output matches your expectations.

- If all looks well:
  ```
  rsync -av --no-t --checksum schemas/output/ /path/to/repo/for/schemas/
  ```

- Check that the changes look resonable also from the perspective of git:
  ```
  cd /path/to/repo/for/schemas/
  git status
  ```

- Stage, commit and push the changes to the schema repo:
  ```
  git add .
  git commit -m "Update schemas for <version> release"
  git push
  ```
