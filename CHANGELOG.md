# Changelog

## v1.1.0 (08/07/2021)

This is release v1.1.0 of the OPTIMADE API specification.

This is a minor release that primarily clarifies the specification, with only two additions.

### Changes

- The `mass` field of the `species` attribute for the `structures` type has been updated from a float to a list of floats ([#344](https://github.com/Materials-Consortia/OPTIMADE/pull/344)). This is a breaking change for any implementations that serve this optional field.
- The `implementation` field of the general `meta` response has been updated to include an `issue_tracker` field ([#339](https://github.com/Materials-Consortia/OPTIMADE/pull/339)).

### Fixes

- The specification text has been clarified in several places.
- Multiple typos, grammatical errors, and incorrect API examples have been fixed.
- The OpenAPI schemas are now fully compliant with the Swagger validator.


## v1.0.0 (01/07/2020)

This is release v1.0.0 of the OPTIMADE API specification.

The specification has undergone a few changes since v1.0.0-rc.2, some not backward compatible.

A few highlighted changes directly affecting the API:
- Several changes related to version negotiation for future releases of the API have been added.
- The API may now be served on both the unversioned and versioned URLs.
- The top-level `meta` field has undergone major revision:
   - It is now mandatory, with a few mandatory subfields (e.g., `api_version`), and most other fields made optional.
   - A link to a schema may be provided.
   - It no longer contains an `index_base_url`, since this functionality is covered by `root` links in the `/links` endpoint.

- The `unit` field for describing properties in the `/info` endpoints is now standardized to use the Unified Code for Units of Measure.
