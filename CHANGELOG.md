# Changelog

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


## v1.0.0 (July 1, 2020)

This is release v1.0.0 of the OPTIMADE API specification.
