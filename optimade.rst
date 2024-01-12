=========================================
OPTIMADE API specification v1.2.0~develop
=========================================

.. comment

   This document uses RST text roles on (almost) all literals to specify the context to which each literal belongs.
   This markup enables nicer formatting (e.g., HTML output can be formatted using CSS), as well as automated spell checks and testing.
   Below follows the definitions of the text roles used:

     # Filtering

     filter : full OPTIMADE filter strings
     filter-fragment : segments of filter strings, or filter strings that uses, e.g., "..."
                       so they would not pass a validation.
     filter-op : operators and keywords in the filtering language
     ere : regex on ere form
     pcre : regex on pcre form

     # OPTIMADE concepts

     entry : names of type of resources, served via OPTIMADE, pertaining to data in a database.
     property : data item that belongs to an entry.
     val : value examples that properties can be.
           :val: is ONLY used when referencing values of actual properties, i.e., information that belongs to the database.
     type : data type of values.
            MUST equal a valid OPTIMADE data type as listed and defined under `Data types`_.

     # URL queries

     endpoint : specification of endpoints and endpoint names.
     query-param : URL query parameter names.
     query-string : strings that represent segments of URL query strings, with query parameters and values.
     query-url : full URLs, or relative starting with a '/' of URL queries.

     # HTTP

     http-header : an HTTP header name, or header + value.
     http-error : an HTTP error on form <number> <English text>.

     # Responses

     json : examples of JSON output.
     field : keys in key-value dictionaries in responses.
     field-val : value examples that fields can be set to.
                 Note that `null` sometimes refer to the OPTIMADE concept of :val:`null`, and sometimes to the javascript constant :field-val:`null`, and the markup distinguishes these two cases.
     object : names of more complex response objects.

     # Validation

     <anything>-fail : means this is a counter-example of something
                       that is meant to be on form <anything> but is not valid.

.. role:: filter(code)
   :language: filter

.. role:: filter-fragment(literal)

.. role:: filter-op(literal)

.. role:: ere(literal)

.. role:: pcre(literal)


.. role:: entry(literal)

.. role:: property(literal)

.. role:: val(literal)

.. role:: type(literal)

.. role:: property-fail(literal)



.. role:: endpoint(literal)

.. role:: query-param(literal)

.. role:: query-val(literal)

.. role:: query-string(literal)

.. role:: query-url(literal)


.. role:: http-header(literal)

.. role:: http-error(literal)


.. role:: json(code)
   :language: json

.. role:: field(literal)

.. role:: field-val(literal)

.. role:: object(literal)


.. sectnum::

.. contents::



Introduction
============

As researchers create independent materials databases, much can be gained from retrieving data from multiple databases.
However, automating the retrieval of data is difficult if each database has a different application programming interface (API).
This document specifies a standard API for retrieving data from materials databases.
This API specification has been developed over a series of workshops entitled "Open Databases Integration for Materials Design", held at the Lorentz Center in Leiden, Netherlands and the CECAM headquarters in Lausanne, Switzerland.

The API specification described in this document builds on top of the `JSON:API v1.1 specification <https://jsonapi.org/format/1.1/>`__.
More specifically, it defines specific `implementation semantics <https://jsonapi.org/format/1.1/#semantics>`__ allowed by the JSON:API standard, but which go beyond the restrictions imposed on `JSON:API profiles <https://jsonapi.org/format/1.1/#profile-rules>`__ and `extensions <https://jsonapi.org/format/1.1/#extension-rules>`__.
The JSON:API specification is assumed to apply wherever it is stricter than what is formulated in this document.
Exceptions to this rule are stated explicitly (e.g. non-compliant responses are tolerated if a non-standard response format is explicitly requested).

Definition of Terms
===================

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in :RFC:`2119`.

**Database provider**
    A service that provides one or more databases with data desired to be made available using the OPTIMADE API.

**Database-provider-specific prefix**
    Every database provider is designated a unique prefix.
    The prefix is used to separate the namespaces used by provider-specific extensions.
    The list of presently defined prefixes is maintained externally from this specification.
    For more information, see section `Database-Provider-Specific Namespace Prefixes`_.

**API implementation**
    A realization of the OPTIMADE API that a database provider uses to serve data from one or more databases.

**Identifier**
    Names that MUST start with a lowercase letter ([a-z]) or an underscore ("\_") followed by any number of lowercase alphanumerics ([a-z0-9]) and underscores ("\_").

**Base URL**
    The topmost URL under which the API is served. See section `Base URL`_.

**Versioned base URL**
   A URL formed by the base URL plus a path segment indicating a version of the API. See section `Base URL`_.

**Entry**
    A single instance of a specific type of resource served by the API implementation.
    For example, a :entry:`structures` entry is comprised by data that belong to a single structure.

**Entry type**
    Entries are categorized into types, e.g., :entry:`structures`, :entry:`calculations`, :entry:`references`.
    Entry types MUST be named according to the rules for identifiers.

**Entry property**
    One data item which belongs to an entry, e.g., the chemical formula of a structure.

**Entry property name**
    The name of an entry property.
    Entry property names MUST follow the rules for identifiers and MUST NOT have the same name as any of the entry types.

**Relationship**
    Any entry can have one or more relationships with other entries.
    These are described in section `Relationships`_.
    Relationships describe links between entries rather than data that belong to a single entry, and are thus regarded as distinct from the entry properties.

**Query filter**
    An expression used to influence the entries returned in the response to a URL query.
    The filter is specified using the URL query parameter :query-param:`filter`
    using a format described in the section `API Filtering Format Specification`_.

**Queryable property**
    An entry property that can be referred to in the filtering of results.
    See section `API Filtering Format Specification`_ for more information on formulating filters on properties.
    The section `Entry List`_ specifies the REQUIRED level of query support for different properties.
    If nothing is specified, any support for queries is OPTIONAL.

**ID**
    The ID entry property is a unique string referencing a specific entry in the database.
    The following constraints and conventions apply to IDs:

    - Taken together, the ID and entry type MUST uniquely identify the entry.
    - Reasonably short IDs are encouraged and SHOULD NOT be longer than 255 characters.
    - IDs MAY change over time.

**Immutable ID**
    A unique string that specifies a specific resource in a database.
    The string MUST NOT change over time.

**Response format**
    The data format for the HTTP response, which can be selected using the :query-param:`response_format` URL query parameter.
    For more info, see section `Response Format`_.

**Field**
    The key used in response formats that return data in associative-array-type data structures.
    This is particularly relevant for the default JSON-based response format.
    In this case, **field** refers to the name part of the name-value pairs of JSON objects.

Data types
----------

An API implementation handles data types and their representations in three different contexts:

- In the HTTP URL query filter, see section `API Filtering Format Specification`_.
- In the HTTP response. The default response format is JSON-based and thus uses JSON data types.
  However, other response formats can use different data types.
  For more info, see section `Responses`_.
- The underlying database backend(s) from which the implementation serves data.

Hence, entry properties are described in this proposal using
context-independent types that are assumed to have some form of
representation in all contexts. They are as follows:

- Basic types: **string**, **integer**, **float**, **boolean**, **timestamp**.
- **list**: an ordered collection of items, where all items are of the same type, unless they are unknown.
  A list can be empty, i.e., contain no items.
- **dictionary**: an associative array of **keys** and **values**, where **keys** are pre-determined strings, i.e., for the same entry property, the **keys** remain the same among different entries whereas the **values** change.
  The **values** of a dictionary can be any basic type, list, dictionary, or unknown.

An entry property value that is not present in the database is **unknown**.
This is equivalently expressed by the statement that the value of that entry property is :val:`null`.
For more information see section `Properties with an unknown value`_

The definition of a property of an entry type specifies a type. The value of that property MUST either have a value of that type, or be unknown.

General API Requirements and Conventions
========================================

Versioning of this standard
---------------------------
This standard describes a communication protocol that, when implemented by a server, provides clients with an API for data access.

Released versions of the standard are versioned using `semantic versioning v2 <https://semver.org/spec/v2.0.0.html>`__ in reference to changes in *that API* (i.e., not in the server-side implementation of the protocol).

To clarify: semantic versioning mandates version numbers of the form MAJOR.MINOR.PATCH, where a "backwards incompatible API change" requires incrementing the MAJOR version number.
A future version of the OPTIMADE standard can mandate servers to change their behavior to be compliant with the newer version.
However, such changes are only considered "backwards incompatible API changes" if they have the potential to break clients that correctly use the API according to the earlier version.

Furthermore, the addition of new keys in key-value-formatted responses of the OPTIMADE API are not regarded as "backwards incompatible API changes."
Hence, a client MUST disregard unrecognized keys when interpreting responses (but MAY issue warnings about them).
On the other hand, a change of the OPTIMADE standard that fundamentally alters the interpretation of a response due to the presence of a new key will be regarded as a "backwards incompatible API change" since a client interpreting the response according to a prior version of the standard would misinterpret that response.

Working copies distributed as part of the development of the standard are marked with the version number for the release they are based on with an additional "~develop" suffix.
These "versions" do not refer to a single specific instance of the text (i.e., the same "~develop" version string is retained until a release), nor is it clear to what degree they contain backwards incompatible API changes.
Hence, the suffix is intentionally designed to make these version strings not to conform with semantic versioning to prevent incorrect comparisons to released versions using the scheme prescribed by semantic versioning.
Version strings with a "~develop" suffix MAY be used by implementations during testing.
However, a client that encounters them unexpectedly SHOULD NOT make any assumptions about the level of API compatibility.

In conclusion, the versioning policy of this standard is designed to allow clients using the OPTIMADE API according to a specific version of the standard to assume compatibility with servers implementing any future (non-development) version of the standard sharing the same MAJOR version number.

Base URL
--------

Each database provider will publish one or more **base URLs** that serve the API, for example: http://example.com/optimade/.
Every URL path segment that follows the base URL MUST behave as standardized in this API specification.

Versioned base URLs
~~~~~~~~~~~~~~~~~~~

Access to the API is primarily provided under **versioned base URLs**.
An implementation MUST provide access to the API under a URL where the first path segment appended to the base URL is :query-url:`/vMAJOR`, where :val:`MAJOR` is one of the major version numbers of the API that the implementation supports.
This URL MUST serve the *latest* minor/patch version supported by the implementation.
For example, the latest minor and patch version of major version 1 of the API is served under :query-url:`/v1`.

An implementation MAY also provide versioned base URLs on the forms :query-url:`/vMAJOR.MINOR` and :query-url:`/vMAJOR.MINOR.PATCH`.
Here, :val:`MINOR` is the minor version number and :val:`PATCH` is the patch version number of the API.
A URL on the form  :query-url:`/vMAJOR.MINOR` MUST serve the *latest* patch version supported by the implementation of this minor version.

API versions that are published with a suffix, e.g., :val:`-rc<number>` to indicate a release candidate version, SHOULD be served on versioned base URLs without this suffix.

If a request is made to a versioned base URL that begins with :query-url:`/v` and an integer followed by any other characters, indicating a version that the implementation does not recognize or support, the implementation SHOULD respond with the custom HTTP server error status code :http-error:`553 Version Not Supported`, preferably along with a user-friendly error message that directs the client to adapt the request to a version it provides.

It is the intent that future versions of this standard will not assign different meanings to URLs that begin with :query-url:`/v` and an integer followed by other characters.
Hence, a client can safely attempt to access a specific version of the API via the corresponding versioned base URL.
For other forms of version negotiation, see section `Version Negotiation`_.

Examples of valid versioned base URLs:

- http://example.com/optimade/v0/
- http://example.com/v0.9.1/
- http://example.com/v1/

Examples of invalid versioned base URLs:

- http://example.com/optimade/0.9/
- http://example.com/optimade/

Database providers SHOULD strive to implement the latest released version of this standard, as well as the latest patch version of any major and minor version they support.

Note: The base URLs and versioned base URLs themselves are not considered part of the API, and the standard does not specify the response for a request to them.
However, it is RECOMMENDED that implementations serve a human-readable HTML document on base URLs and versioned base URLs, which explains that the URL is an OPTIMADE URL meant to be queried by an OPTIMADE client.

Unversioned base URL
~~~~~~~~~~~~~~~~~~~~

Implementations MAY also provide access to the API on the **unversioned base URL** as described in this subsection.

Access via the unversioned URL is primarily intended for (i) convenience when manually interacting with the API, and (ii) to provide version agnostic permanent links to resource objects.
Clients that perform automated processing of responses SHOULD access the API via versioned base URLs.

Implementations serving the API on the unversioned base URL have a few alternative options:

1. Direct access MAY be provided to the full API.
2. Requests to endpoints under the unversioned base URL MAY be redirected using an HTTP 307 temporary redirect to the corresponding endpoints under a versioned base URL.
3. Direct access MAY be limited to only single entry endpoints (see section `Single Entry Endpoints`_), i.e., so that this form of access is only available for permanent links to resource objects.

Implementations MAY combine direct access to single entry endpoints with redirects for other API queries.

The client MAY provide a query parameter :query-param:`api_hint` to hint the server about a preferred API version.
When this parameter is provided, the request is to be handled as described in section `Version Negotiation`_, which allows a "best suitable" version of the API to be selected to serve the request (or forward the request to).
However, if :query-param:`api_hint` is not provided, the implementation SHOULD serve (or redirect to) its preferred version of the API (i.e., the latest, most mature, and stable version).
In this case, that version MUST also be the first version in the response of the :endpoint:`versions` endpoint (see section `Versions Endpoint`_).

    **For implementers**: Before enabling access to the API on unversioned base URLs, implementers are advised to consider that an upgrade of the major version of the API served this way can change the behaviors of associated endpoints in ways that are not backward compatible.

Version Negotiation
-------------------
The OPTIMADE API provides three concurrent mechanisms for version negotiation between client and server.

1. The :endpoint:`versions` endpoint served directly under the unversioned base URL allows a client to discover all major API versions supported by a server in the order of preference (see section `Versions Endpoint`_).

2. A client can access the API under versioned base URLs.
   In this case, the server MUST respond according to the specified version or return an error if the version is not supported (see section `Versioned Base URLs`_).

3. When accessing the API under the unversioned base URL, clients are encouraged to append the OPTIONAL query parameter :query-param:`api_hint` to hint the server about a preferred API version for the request.
   This parameter is described in more detail below.

The :query-param:`api_hint` query parameter MUST be accepted by all API endpoints.
However, for endpoints under a versioned base URL the request MUST be served as usual according to the version specified in the URL path segment regardless of the value of :query-param:`api_hint`.
In this case, the server MAY issue a warning if the value of :query-param:`api_hint` suggests that the query may not be properly supported.
If the client provides the parameter, the value SHOULD have the format :val:`vMAJOR` or :val:`vMAJOR.MINOR`, where MAJOR is a major version and MINOR is a minor version of the API.
For example, if a client appends :query-string:`api_hint=v1.0` to the query string, the hint provided is for major version 1 and minor version 0.

If the server supports the major version indicated by the :query-param:`api_hint` parameter at the same or a higher minor version (if provided), it SHOULD serve the request using this version.
If the server does not support the major version hinted, or if it supports the major version but only at a minor version below the one hinted, it MAY use the provided values to make a best-effort attempt at still serving the request, e.g., by invoking the closest supported version of the API.
If the hinted version is not supported by the server and the request is not served using an alternative version, the server SHOULD respond with the custom HTTP server error status code :http-error:`553 Version Not Supported`.
Note that the above protocol means that clients MUST NOT expect that a returned response is served according to the version that is hinted.

    **For end users**: Users are strongly encouraged to include the :query-param:`api_hint` query parameter for URLs in, e.g., journal publications for queries on endpoints under the unversioned base URL.
    The version hint will make it possible to serve such queries in a reasonable way even after the server changes the major API version used for requests without version hints.

Index Meta-Database
-------------------

A database provider MAY publish a special Index Meta-Database base URL. The main purpose of this base URL is to allow for automatic discoverability of all databases of the provider. Thus, it acts as a meta-database for the database provider's implementation(s).

The index meta-database MUST only provide the :endpoint:`info` and :endpoint:`links` endpoints, see sections `Info Endpoints`_ and `Links Endpoint`_.
It MUST NOT expose any entry listing endpoints (e.g., :endpoint:`structures`).

These endpoints do not need to be queryable, i.e., they MAY be provided as static JSON files.
However, they MUST return the correct and updated information on all currently provided implementations.

The :field:`is_index` field under :field:`attributes` as well as the :field:`relationships` field, MUST be included in the :endpoint:`info` endpoint for the index meta-database (see section `Base Info Endpoint`_).
The value for :field:`is_index` MUST be :field-val:`true`.

A few suggestions and mandatory requirements of the OPTIMADE specification are specifically relaxed **only for index meta-databases** to make it possible to serve them in the form of static files on restricted third-party hosting platforms:

- When serving an index meta-database in the form of static files, it is RECOMMENDED that the response excludes the subfields in the top-level :field:`meta` field that would need to be dynamically generated (as described in the section `JSON Response Schema: Common Fields`_.)
  The motivation is that static files cannot keep dynamic fields such as :field:`time_stamp` updated.

- The `JSON:API specification <http://jsonapi.org/format/1.1>`__ requirements on content negotiation using the HTTP headers :http-header:`Content-Type` and :http-header:`Accept` are NOT mandatory for index meta-databases.
  Hence, API Implementations MAY ignore the content of these headers and respond to all requests.
  The motivation is that static file hosting is typically not flexible enough to support these requirements on HTTP headers.

- API implementations SHOULD serve JSON content with either the JSON:API mandated HTTP header :http-header:`Content-Type: application/vnd.api+json` or :http-header:`Content-Type: application/json`. However, if the hosting platform does not allow this, JSON content MAY be served with :http-header:`Content-Type: text/plain`.

Database-Provider-Specific Namespace Prefixes
---------------------------------------------

This standard refers to database-provider-specific prefixes and database providers.

A list of known providers and their assigned prefixes is published in the form of an OPTIMADE Index Meta-Database with base URL `https://providers.optimade.org <https://providers.optimade.org>`__.
Visiting this URL in a web browser gives a human-readable description of how to retrieve the information in the form of a JSON file, and specifies the procedure for registration of new prefixes.

API implementations SHOULD NOT make up and use new prefixes without first getting them registered in the official list.

**Examples**:

- A database-provider-specific prefix: ``exmpl``. Used as a field name in a response: :field:`_exmpl_custom_field`.

The initial underscore indicates an identifier that is under a separate namespace under the ownership of that organization.
Identifiers prefixed with underscores will not be used for standardized names.

URL Encoding
------------

Clients SHOULD encode URLs according to :RFC:`3986`.
API implementations MUST decode URLs according to :RFC:`3986`.

Relationships
-------------

The API implementation MAY describe many-to-many relationships between entries along with OPTIONAL human-readable descriptions that describe each relationship.
These relationships can be to the same, or to different, entry types.
Response formats have to encode these relationships in ways appropriate for each format.

In the default response format, relationships are encoded as `JSON:API Relationships <https://jsonapi.org/format/1.1/#document-resource-object-relationships>`__, see section `Entry Listing JSON Response Schema`_.

    **For implementers**: For database-specific response formats without a dedicated mechanism to indicate relationships, it is suggested that they are encoded alongside the entry properties.
    For each entry type, the relationships with entries of that type can then be encoded in a field with the name of the entry type, which are to contain a list of the IDs of the referenced entries alongside the respective human-readable description of the relationships.
    It is the intent that future versions of this standard uphold the viability of this encoding by not standardizing property names that overlap with the entry type names.

Properties with an unknown value
--------------------------------

Many databases allow specific data values to exist for some of the entries, whereas for others, no data value is present.
This is referred to as the property having an *unknown* value, or equivalently, that the property value is :val:`null`.

The text in this section describes how the API handles properties with the value :val:`null`.
The use of :val:`null` values inside nested property values (such as, e.g., lists or dictionaries) are described in the definitions of those data structures elsewhere in the specification, see section `Entry List`_.
For these properties, :val:`null` MAY carry a special meaning.

REQUIRED properties with an unknown value MUST be included and returned in the response with the value :val:`null`.

OPTIONAL properties with an unknown value, if requested explicitly via the :query-param:`response_fields` query parameter, MUST be included and returned in the response with the value :val:`null`.
(For more info on the :query-param:`response_fields` query parameter, see section `Entry Listing URL Query Parameters`_.)

The interaction of properties with an unknown value with query filters is described in the section `Filtering on Properties with an unknown value`_.
In particular, filters with :filter-fragment:`IS UNKNOWN` and :filter-fragment:`IS KNOWN` can be used to match entries with values that are, or are not, unknown for some property, respectively.

Handling unknown property names
-------------------------------

When an implementation receives a request with a query filter that refers to an unknown property name it is handled differently depending on the database-specific prefix:

* If the property name has no database-specific prefix, or if it has the database-specific prefix that belongs to the implementation itself, the error :http-error:`400 Bad Request` MUST be returned with a message indicating the offending property name.

* If the property name has a database-specific prefix that does *not* belong to the implementation itself, it MUST NOT treat this as an error, but rather MUST evaluate the query with the property treated as unknown, i.e., comparisons are evaluated as if the property has the value :val:`null`.

  * Furthermore, if the implementation does not recognize the prefix at all, it SHOULD return a warning that indicates that the property has been handled as unknown.

  * On the other hand, if the prefix is recognized, i.e., as belonging to a known database provider, the implementation SHOULD NOT issue a warning but MAY issue diagnostic output with a note explaining how the request was handled.

The rationale for treating properties from other databases as unknown rather than triggering an error is for OPTIMADE to support queries using database-specific properties that can be sent to multiple databases.

For example, the following query can be sent to API implementations `exmpl1` and `exmpl2` without generating any errors:

:filter:`filter=_exmpl1_band_gap<2.0 OR _exmpl2_band_gap<2.5`

Transmission of large property values
-------------------------------------

A property value may be too large to fit in a single response.
OPTIMADE provides a mechanism for a client to handle such properties by fetching them in separate series of requests.
It is up to the implementation to decide which values are too large to represent in a single response, and this decision MAY change between responses.

In this case, the response to the initial query gives the value :val:`null` for the property.
A list of one or more data URLs together with their respective partial data formats are given in the response.
How this list is provided is response format-dependent.
For the JSON response format, see the description of the :field:`partial_data_links` field, nested under :field:`data` and then :field:`meta`, in the section `JSON Response Schema: Common Fields`_.

The default partial data format is named "jsonlines" and is described in the Appendix `OPTIMADE JSON lines partial data format`_.
An implementation SHOULD always include this format as one of the partial data formats provided for a property that has been omitted from the response to the initial query.
Implementations MAY provide links to their own non-standard formats, but non-standard format names MUST be prefixed by a database-provider-specific prefix.

Below follows an example of the :field:`data` and :field:`meta` parts of a response using the JSON response format that communicates that the property value has been omitted from the response, with three different links for different partial data formats provided.

.. code:: jsonc

     {
       // ...
       "data": {
         "type": "structures",
         "id": "2345678",
         "attributes": {
             "a": null
         }
         "meta": {
           "partial_data_links": {
             "a": [
               {
                 "format": "jsonlines",
                 "link": "https://example.org/optimade/v1.2/extensions/partial_data/structures/2345678/a/default_format"
               },
               {
                 "format": "_exmpl_bzip2_jsonlines",
                 "link": "https://db.example.org/assets/partial_values/structures/2345678/a/bzip2_format"
               },
               {
                 "format": "_exmpl_hdf5",
                 "link": "https://cloud.example.org/ACCHSORJGIHWOSJZG"
               }
             ]
           }
         }
       }
     // ...
   }


Metadata properties
-------------------

A metadata property represents entry and property-specific metadata for a given entry.
How these are communicated in the response depends on the response format.
For the JSON response format, the metadata properties are stored in the resource object metadata field, :field:`meta` in a dictionary field :field:`property_metadata` with the keys equal to the names of the respective properties for which metadata is available, see `JSON Response Schema: Common Fields`_.

The format of the metadata property is specified by the field :field:`x-optimade-metadata-definition` in the Property Definition of the field, see `Property Definitions`_.
Database providers are allowed to define their own metadata properties in :field:`x-optimade-metadata-definition`, but they MUST use the database-provider-specific prefix even for metadata of database-specific fields.
For example, the metadata property definition of the field :field:`_exmpl_example_field` MUST NOT define a metadata field named, e.g., :field:`accuracy`; the field rather needs to be named, e.g., :field:`_exmpl_accuracy`.
The reason for this limitation is to avoid name collisions with metadata fields defined by the OPTIMADE standard in the future that apply also to database-specific data fields.

Implementation of the :field:`meta` field is OPTIONAL.
However, when an implementation supports the :field:`property_metadata` field, it SHOULD include metadata fields for all properties which have metadata and are present in the data part of the response.

Example of a response in the JSON response format with two structure entries that each include a metadata property for the attribute field :field:`element_ratios` and the database-specific per entry metadata field :field:`_exmpl_originates_from_project` :

.. code:: jsonc
     {
       "data": [
         {
           "type": "structures",
           "id": "example.db:structs:0001",
           "attributes": {
             "element_ratios":[0.33336, 0.22229, 0.44425]
           },
           "meta": {
             "property_metadata": {
               "element_ratios": {
                 "_exmpl_originates_from_project": "piezoelectic_perovskites"
               }
             }
           }
         },
         {
           "type": "structures",
           "id": "example.db:structs:1234",
           "attributes": {
             "element_ratios":[0.5, 0.5]
           },
           "meta": {
             "property_metadata":{
               "element_ratios": {
                 "_exmpl_originates_from_project": "ferroelectric_binaries"
               }
             }
           }
         }
         //...
       ]
       // ...
     }

Example of the corresponding metadata property definition contained in the field :field:`x-optimade-metadata-definition` which is placed in the property definition of :field:`element_ratios`:

    .. code:: jsonc
         // ...
         "x-optimade-metadata-definition": {
           "title": "Metadata for the element_ratios field",
           "description": "This field contains the per-entry metadata for the element_ratios field.",
           "x-optimade-type": "dictionary",
           "x-optimade-unit": "inapplicable",
           "type": ["object", "null"],
           "properties" : {
             "_exmpl_originates_from_project": {
               "$id": "https://properties.example.com/v1.2.0/element_ratios_meta/_exmpl_originates_from_project",
               "description" : "A string naming the internal example.com project id where this property was added to the database.",
               "x-optimade-type": "string",
               "x-optimade-unit" : "inapplicable"
             }
           }
         }
         // ...

Example of the corresponding metadata property definition contained in the field :field:`x-optimade-metadata-definition` which is placed in the property definition of :field:`element_ratios`:

    .. code:: jsonc
         // ...
         "x-optimade-metadata-definition": {
           "title": "Metadata for the element_ratios field",
           "description": "This field contains the per-entry metadata for the element_ratios field.",
           "x-optimade-type": "dictionary",
           "x-optimade-unit": "inapplicable",
           "type": ["object", "null"],
           "properties" : {
             "_exmpl_originates_from_project": {
               "$id": "https://properties.example.com/v1.2.0/element_ratios_meta/_exmpl_originates_from_project",
               "description" : "A string naming the internal example.com project id where this property was added to the database.",
               "x-optimade-type": "string",
               "x-optimade-unit" : "inapplicable"
             }
           }
         }
         // ...

Responses
=========

Response Format
---------------

This section defines a JSON response format that complies with the `JSON:API v1.1 <http://jsonapi.org/format/1.1>`__ specification.
All endpoints of an API implementation MUST be able to provide responses in the JSON format specified below and MUST respond in this format by default.

Each endpoint MAY support additional formats, and SHOULD declare these formats under the endpoint :endpoint:`/info/<entry type>` (see section `Entry Listing Info Endpoints`_).
Clients can request these formats using the :query-param:`response_format` URL query parameter.
Specifying a :query-param:`response_format` different from :query-val:`json` (e.g. :query-string:`response_format=xml`) allows the API to break conformance not only with the JSON response format specification, but also, e.g., in terms of how content negotiation is implemented.

Database-provider-specific :query-param:`response_format` identifiers MUST include a database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

JSON Response Schema: Common Fields
-----------------------------------

In the JSON response format, property types translate as follows:

- **string**, **boolean**, **list** are represented by their similarly named counterparts in JSON.
- **integer**, **float** are represented as the JSON number type.
- **timestamp** uses a string representation of date and time as defined in `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__.
- **dictionary** is represented by the JSON object type.
- **unknown** properties are represented by either omitting the property or by a JSON :field-val:`null` value.

Every response SHOULD contain the following fields, and MUST contain at least :field:`meta`:

- **meta**: a `JSON:API meta member <https://jsonapi.org/format/1.1/#document-meta>`__ that contains JSON:API meta objects of non-standard meta-information.
  It MUST be a dictionary with these fields:

  - **api\_version**: a string containing the full version of the API implementation.
    The version number string MUST NOT be prefixed by, e.g., "v".
    Examples: :field-val:`1.0.0`, :field-val:`1.0.0-rc.2`.

  - **query**: information on the query that was requested.
    It MUST be a dictionary with this field:

    - **representation**: a string with the part of the URL following the versioned or unversioned base URL that serves the API.
      Query parameters that have not been used in processing the request MAY be omitted.
      In particular, if no query parameters have been involved in processing the request, the query part of the URL MAY be excluded.
      Example: :field-val:`/structures?filter=nelements=2`.

  - **more\_data\_available**: :field-val:`false` if the response contains all data for the request (e.g., a request issued to a single entry endpoint, or a :query-param:`filter` query at the last page of a paginated response) and :field-val:`true` if the response is incomplete in the sense that multiple objects match the request, and not all of them have been included in the response (e.g., a query with multiple pages that is not at the last page).

  :field:`meta` SHOULD also include these fields:

  - **time\_stamp**: a timestamp containing the date and time at which the query was executed.
  - **data\_returned**: an integer containing the total number of data resource objects returned for the current :query-param:`filter` query, independent of pagination.
  - **provider**: information on the database provider of the implementation.
    It MUST be a dictionary with these fields:

    - **name**: a short name for the database provider.
    - **description**: a longer description of the database provider.
    - **prefix**: database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

    :field:`provider` MAY include these fields:

    - **homepage**: a `JSON API link <http://jsonapi.org/format/1.1/#document-links>`__, pointing to the homepage of the database provider, either directly as a string, or as an object which can contain the following fields:

      - **href**: a string containing the homepage URL.
      - **meta**: a meta object containing non-standard meta-information about the database provider's homepage.

  :field:`meta` MAY also include these fields:

  - **data\_available**: an integer containing the total number of data resource objects available in the database for the endpoint.
  - **last\_id**: a string containing the last ID returned.
  - **response\_message**: response string from the server.
  - **request\_delay**: a non-negative float giving time in seconds that the client is suggested to wait before issuing a subsequent request.

  Implementation note: the functionality of this field overlaps to some degree with features provided by the HTTP error :http-error:`429 Too Many Requests` and the `Retry-After HTTP header <https://tools.ietf.org/html/rfc7231.html#section-7.1.3>`__. Implementations are suggested to provide consistent handling of request overload through both mechanisms.

  - **database**: a dictionary describing the specific database accessible at this OPTIMADE API.
    If provided, the dictionary fields SHOULD match those provided in the corresponding links entry for the database in the provider's index meta-database, outlined in `Links Endpoint JSON Response Schema`_.
    The dictionary can contain the following OPTIONAL fields:

    - **id**: the identifier of this database within those served by this provider, i.e., the ID under which this database is served in this provider's index meta-database.
    - **name**: a human-readable name for the database, e.g., for use in clients.
    - **version**: a string describing the version of the database.
    - **description**: a human-readable description of the database, e.g., for use in clients.
    - **homepage**: a `JSON API link <http://jsonapi.org/format/1.0/#document-links>`__, pointing to a homepage for the particular database.
    - **maintainer**: a dictionary providing details about the maintainer of the database, which MUST contain the single field:

      - **email** with the maintainer's email address.

  - **implementation**: a dictionary describing the server implementation, containing the OPTIONAL fields:

    - **name**: name of the implementation.
    - **version**: version string of the current implementation.
    - **homepage**: a `JSON API link <http://jsonapi.org/format/1.1/#document-links>`__, pointing to the homepage of the implementation.
    - **source\_url**: a `JSON API link <http://jsonapi.org/format/1.1/#document-links>`__ pointing to the implementation source, either downloadable archive or version control system.

    - **maintainer**: a dictionary providing details about the maintainer of the implementation, MUST contain the single field:

      - **email** with the maintainer's email address.

    - **issue\_tracker**: a `JSON API link <http://jsonapi.org/format/1.1/#document-links>`__ pointing to the implementation's issue tracker.

  - **warnings**: a list of warning resource objects representing non-critical errors or warnings.
    A warning resource object is defined similarly to a `JSON:API error object <http://jsonapi.org/format/1.1/#error-objects>`__, but MUST also include the field :field:`type`, which MUST have the value :field-val:`"warning"`.
    The field :field:`detail` MUST be present and SHOULD contain a non-critical message, e.g., reporting unrecognized search attributes or deprecated features.
    The field :field:`status`, representing an HTTP response status code, MUST NOT be present for a warning resource object.
    This is an exclusive field for error resource objects.

    Example for a deprecation warning:

    .. code:: jsonc

       {
         "id": "dep_chemical_formula_01",
         "type": "warning",
         "code": "_exmpl_dep_chemical_formula",
         "title": "Deprecation Warning",
         "detail": "chemical_formula is deprecated, use instead chemical_formula_hill"
       }

    **Note**: warning :field:`id`\ s MUST NOT be trusted to identify the exceptional situations (i.e., they are not error codes), use instead the field :field:`code` for this.
    Warning :field:`id`\ s can *only* be trusted to be unique in the list of warning resource objects, i.e., together with the :field:`type`.

    General OPTIMADE warning codes are specified in section `Warnings`_.

  - Other OPTIONAL additional information *global to the query* that is not specified in this document, MUST start with a database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

  - Example for a request made to :query-url:`http://example.com/optimade/v1/structures/?filter=a=1 AND b=2`:

    .. code:: jsonc

       {
         "meta": {
           "query": {
             "representation": "/structures/?filter=a=1 AND b=2"
           },
           "api_version": "1.0.0",
           "schema": "http://schemas.optimade.org/openapi/v1/optimade.json",
           "time_stamp": "2007-04-05T14:30:20Z",
           "data_returned": 10,
           "data_available": 10,
           "more_data_available": false,
           "provider": {
             "name": "Example provider",
             "description": "Provider used for examples, not to be assigned to a real database",
             "prefix": "exmpl",
             "homepage": "http://example.com"
           },
           "implementation": {
             "name": "exmpl-optimade",
             "version": "0.1.0",
             "source_url": "http://git.example.com/exmpl-optimade",
             "maintainer": {
               "email": "admin@example.com"
             },
             "issue_tracker": "http://tracker.example.com/exmpl-optimade"
           },
           "database": {
             "id": "example_db",
             "name": "Example database 1 (of many)",
             "description": "The first example database in a series hosted by the Example Provider.",
             "homepage": "http://database_one.example.com",
             "maintainer": {
               "email": "science_lead@example.com"
             }
           }
         }
         // ...
       }

  - **schema**: a `JSON:API links object <http://jsonapi.org/format/1.1/#document-links>`__ that points to a schema for the response.
    If it is a string, or a dictionary containing no :field:`meta` field, the provided URL MUST point at an `OpenAPI <https://swagger.io/specification/>`__ schema.
    It is possible that future versions of this specification allow for alternative schema types.
    Hence, if the :field:`meta` field of the JSON:API links object is provided and contains a field :field:`schema_type` that is not equal to the string :field-val:`OpenAPI` the client MUST NOT handle failures to parse the schema or to validate the response against the schema as errors.
      **Note**: The :field:`schema` field was previously RECOMMENDED in all responses, but is now demoted to being OPTIONAL since there now is a standard way of specifying a response schema in JSON:API through the :field:`describedby` subfield of the top-level :field:`links` field.

- **data**: The schema of this value varies by endpoint, it can be either a *single* `JSON:API resource object <http://jsonapi.org/format/1.1/#document-resource-objects>`__ or a *list* of JSON:API resource objects.
  Every resource object needs the :field:`type` and :field:`id` fields, and its attributes (described in section `API Endpoints`_) need to be in a dictionary corresponding to the :field:`attributes` field.

  Every resource object MAY also contain a :field:`meta` field which MAY contain the following keys:

  - **property_metadata**: an object containing per-entry and per-property metadata.
    The keys are the names of the fields in :field:`attributes` for which metadata is available.
    The values belonging to these keys are dictionaries containing the relevant metadata fields.
    See also `Metadata properties`_

  - **partial_data_links**: an object used to list links which can be used to fetch data that has been omitted from the :field:`data` part of the response.
    The keys are the names of the fields in :field:`attributes` for which partial data links are available.
    Each value is a list of objects that MUST have the following keys:

    - **format**: String.
      The name of the format provided via this link.
      For one of the objects this :field:`format` field SHOULD have the value "jsonlines", which refers to the format in `OPTIMADE JSON lines partial data format`_.

    - **link**: String.
      A `JSON API link <http://jsonapi.org/format/1.0/#document-links>`__ that points to a location from which the omitted data can be fetched.
      There is no requirement on the syntax or format for the link URL.

    For more information about the mechanism to transmit large property values, including an example of the format of :field:`partial_data_links`, see `Transmission of large property values`_.

The response MAY also return resources related to the primary data in the field:

- **links**: a `JSON API links object <http://jsonapi.org/format/1.1/#document-links>`__ is REQUIRED for implementing pagination.
  (see section `Entry Listing URL Query Parameters`_.)
  Each field of a links object, i.e., a "link", MUST be one of:

  - :field-val:`null`
  - a string representing a URI, or
  - a dictionary ("link object") with fields

    - **href**: a string representing a URI
    - **meta**: (OPTIONAL) a meta object containing non-standard meta-information about the link

  Example links objects:

  - **base\_url**: a links object representing the base URL of the implementation. Example:

    .. code:: jsonc

      {
        "links": {
          "base_url": {
            "href": "http://example.com/optimade",
            "meta": {
              "_exmpl_db_version": "3.2.1"
            }
          }
          // ...
        }
        // ...
      }

  The :field:`links` field SHOULD include the following links objects:

  - **describedby**: a links object giving the URL for a schema that describes the response.
    The URL SHOULD resolve into a JSON formatted response returning a JSON object with top level :field:`$schema` and/or :field:`$id` fields that can be used by the client to identify the schema format.

      **Note**: This field is the standard facility in JSON:API to communicate a response schema.
    It overlaps in function with the field :field:`schema` in the top level :field:`meta` field.

  The following fields are REQUIRED for implementing pagination:

  - **next**: represents a link to fetch the next set of results.
    When the current response is the last page of data, this field MUST be either omitted or :field-val:`null`\ -valued.

  An implementation MAY also use the following reserved fields for pagination.
  They represent links in a similar way as for :field:`next`.

  - **prev**: the previous page of data. :field-val:`null` or omitted when the current response is the first page of data.
  - **last**: the last page of data.
  - **first**: the first page of data.

  Finally, the :field:`links` field MAY also include the following links object:

  - **self**: a links object giving the URL from which the response was obtained.

- **included**: a list of `JSON:API resource objects <http://jsonapi.org/format/1.1/#document-resource-objects>`__ related to the primary data contained in :field:`data`.
  Responses that contain related resources under :field:`included` are known as `compound documents <https://jsonapi.org/format/1.1/#document-compound-documents>`__ in the JSON:API.

  The definition of this field is found in the `JSON:API specification <http://jsonapi.org/format/1.1/#fetching-includes>`__.
  Specifically, if the query parameter :query-param:`include` is included in the request, :field:`included` MUST NOT include unrequested resource objects.
  For further information on the parameter :query-param:`include`, see section `Entry Listing URL Query Parameters`_.

  This value MUST be either an empty array or an array of related resource objects.

If there were errors in producing the response all other fields MAY be present, but the top-level :field:`data` field MUST be skipped, and the following field MUST be present:

- **errors**: a list of `JSON:API error objects <http://jsonapi.org/format/1.1/#error-objects>`__, where the field :field:`detail` MUST be present.
  All other fields are OPTIONAL.

An example of a full response:

.. code:: jsonc

     {
       "links": {
         "next": null,
         "base_url": {
           "href": "http://example.com/optimade",
           "meta": {
              "_exmpl_db_version": "3.2.1"
           }
         }
       },
       "meta": {
         "query": {
           "representation": "/structures?filter=a=1 AND b=2"
         },
         "api_version": "1.0.0",
         "time_stamp": "2007-04-05T14:30:20Z",
         "data_returned": 10,
         "data_available": 10,
         "last_id": "xy10",
         "more_data_available": false,
         "provider": {
           "name": "Example provider",
           "description": "Provider used for examples, not to be assigned to a real database",
           "prefix": "exmpl",
           "homepage": {
             "href": "http://example.com",
             "meta": {
               "_exmpl_title": "This is an example site"
             }
           }
         },
         "response_message": "OK"
         // <OPTIONAL implementation- or database-provider-specific metadata, global to the query>
       },
       "data": [
         // ...
       ],
       "included": [
         // ...
       ]
     }

- **@context**: A JSON-LD context that enables interpretation of data in the response as linked data.
  If provided, it SHOULD be one of the following:

  - An object conforming to a JSON-LD standard, which includes a :field:`@version` field specifying the version of the standard.
  - A string containing a URL that resolves to such an object.

- **jsonapi**: A `JSON:API object <https://jsonapi.org/format/1.1/#document-jsonapi-object>`__.
  The :field:`version` subfield SHOULD be :field-val:`"1.1"`.
  The :field:`meta` subfield SHOULD be included and contain the following subfields:

  - **api**: A string with the value "OPTIMADE".
  - **api-version**: A string with the full version of the OPTIMADE standard that the processing and response adheres to.
    This MAY be the version indicated at the top of this document, but MAY also be another version if the client, e.g., has used the query parameter :query-param:`api_hint` to request processing according to another version.

  If the server is able to handle serialization in such a way that it can dictate the order of the top level object members in the response, it is RECOMMENDED to put the :field:`jsonapi` as the first top level member to simplify identification of the response.


HTTP Response Status Codes
--------------------------

All HTTP response status codes MUST conform to `RFC 7231: HTTP Semantics <http://tools.ietf.org/html/rfc7231>`__.
The code registry is maintained by IANA and can be found `here <http://www.iana.org/assignments/http-status-codes>`__.

See also the JSON:API definitions of responses when `fetching <https://jsonapi.org/format/1.1/#fetching>`__ data, i.e., sending an HTTP GET request.

**Important**: If a client receives an unexpected 404 error when making a query to a base URL, and is aware of the index meta-database that belongs to the database provider (as described in section `Index Meta-Database`_), the next course of action SHOULD be to fetch the resource objects under the :endpoint:`links` endpoint of the index meta-database and redirect the original query to the corresponding database ID that was originally queried, using the object's :field:`base_url` value.

HTTP Response Headers
---------------------

There are relevant use-cases for allowing data served via OPTIMADE to be accessed from in-browser JavaScript, e.g. to enable server-less data aggregation.
For such use, many browsers need the server to include the header :http-header:`Access-Control-Allow-Origin: *` in its responses, which indicates that in-browser JavaScript access is allowed from any site.

Warnings
--------

Non-critical exceptional situations occurring in the implementation SHOULD be reported to the referrer as warnings.
Warnings MUST be expressed as a human-readable message, OPTIONALLY coupled with a warning code.

Warning codes starting with an alphanumeric character are reserved for general OPTIMADE error codes (currently, none are specified).
For implementation-specific warnings, they MUST start with ``_`` and the database-provider-specific prefix of the implementation (see section `Database-Provider-Specific Namespace Prefixes`_).

API Endpoints
=============

Access to API endpoints as described in the subsections below are to be provided under the versioned and/or the unversioned base URL as explained in the section `Base URL`_.

The endpoints are:

- a :endpoint:`versions` endpoint
- an "entry listing" endpoint
- a "single entry" endpoint
- an introspection :endpoint:`info` endpoint
- an "entry listing" introspection :endpoint:`info` endpoint
- a :endpoint:`links` endpoint to discover related implementations
- a custom :endpoint:`extensions` endpoint prefix

These endpoints are documented below.

Query parameters
----------------
Query parameters to the endpoints are documented in the respective subsections below.
However, in addition, all API endpoints MUST accept the :query-param:`api_hint` parameter described under `Version Negotiation`_.

Versions Endpoint
-----------------

The :endpoint:`versions` endpoint aims at providing a stable and future-proof way for a client to discover the major versions of the API that the implementation provides.
This endpoint is special in that it MUST be provided directly on the unversioned base URL at :query-url:`/versions` and MUST NOT be provided under the versioned base URLs.

The response to a query to this endpoint is in a restricted subset of the :RFC:`4180` CSV (`text/csv; header=present`) format.
The restrictions are: (i) field values and header names MUST NOT contain commas, newlines, or double quote characters; (ii) Field values and header names MUST NOT be enclosed by double quotes; (iii) The first line MUST be a header line.
These restrictions allow clients to parse the file line-by-line, where each line can be split on all occurrences of the comma ',' character to obtain the head names and field values.

In the present version of the API, the response contains only a single field that is used to list the major versions of the API that the implementation supports.
The CSV format header line MUST specify :val:`version` as the name for this field.
However, clients MUST accept responses that include other fields that follow the version.

The major API versions in the response are to be ordered according to the preference of the API implementation.
If a version of the API is served on the unversioned base URL as described in the section `Base URL`_, that version MUST be the first value in the response (i.e., it MUST be on the second line of the response directly following the required CSV header).

It is the intent that all future versions of this specification retain this endpoint, its restricted CSV response format, and the meaning of the first field of the response.

Example response:

.. code:: CSV

  version
  1
  0

The above response means that the API versions 1 and 0 are served under the versioned base URLs :query-url:`/v1` and :query-url:`/v0`, respectively.
The order of the versions indicates that the API implementation regards version 1 as preferred over version 0.
If the API implementation allows access to the API on the unversioned base URL, this access has to be to version 1, since the number 1 appears in the first (non-header) line.

