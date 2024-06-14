=========================================
OPTIMADE API specification v1.3.0~develop
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
    For more information, see section `Namespace Prefixes`_.

**Definition provider**
    A service that provides one or more external or domain-specific property definitions that can be used by OPTIMADE API implementations.

**Definition provider prefix**
    Every definition provider is designated a prefix that cannot clash with an existing database provider prefix.
    The prefix is used to separate the namespaces used by these collections of definitions.
    The list of presently defined prefixes is maintained externally from this specification.
    For more information, see section `Namespace Prefixes`_.

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

- Basic types: **string**, **integer**, **float**, **boolean**, **timestamp**, database-provider-specific or definition-provider-specific data type.
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

..

    **Note**: A list of database and definition providers acknowledged by the **Open Databases Integration for Materials Design** consortium is maintained externally from this specification and can be retrieved as described in section `Namespace Prefixes`_.
    This list is also machine-readable, enabling the automatic discoverability of OPTIMADE API services.

Namespace Prefixes
------------------

There are two mechanisms by which a provider can serve properties that are not standardized by the OPTIMADE specification.

1. By serving properties under a database-provider-specific namespace prefix.
   This is the preferred mechanism for serving properties that are specific to a particular database provider.
2. By adopting a property definition external to the specification by a definition provider.
   This is the preferred mechanism in cases where a database-specific field aligns with a field that is already defined by a definition provider, and can be used to enable aggregated filtering over all OPTIMADE APIs that support this property.

A list of known database and definition providers and their assigned prefixes is published in the form of an OPTIMADE Index Meta-Database with base URL `https://providers.optimade.org <https://providers.optimade.org>`__.
Visiting this URL in a web browser gives a human-readable description of how to retrieve the information in the form of a JSON file, and specifies the procedure for registration of new prefixes.
A human-readable dashboard is also hosted at `<https://www.optimade.org/providers-dashboard>`__.

API implementations SHOULD NOT make up and use new prefixes without first getting them registered in the official list.

**Examples**:

- A database-provider-specific prefix: ``exmpl``. Used as a field name in a response: :field:`_exmpl_custom_field`.
- A definition-provider prefix: ``dft``. Used as a field name in a response by multiple different providers: :field:`_dft_cell_volume` (note: this is a hypothetical example).

The initial underscore indicates an identifier that is under a separate namespace under the ownership of that organization or definition provider.
Identifiers prefixed with underscores will not be used for standardized names.

Database-Provider-Specific Namespace Prefixes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This standard refers to database-provider-specific prefixes and database providers.

Database-provider-specific fields only need to be consistent within the context of one particular database.
Providers that serve multiple databases MAY use the same provider-specific field names with different meanings in different databases.
For example, a provider may use the field :field:`_exmpl_band_gap` to mean a computed band gap in one their databases, and a measured band gap in another database.

Database-provider-specific fields SHOULD be fully described at the relevant :endpoint:`/info/<entry_type>` endpoint (see section `Entry Listing Info Endpoints`_)

Definition-Provider-Specific Namespace Prefixes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This standard refers to definition-provider-specific prefixes and definition providers.

Definition providers MUST provide a canonical property definition for all custom fields they define using the OPTIMADE `Property Definitions`_ format.
Definition providers MUST also list these definitions in the relevant :endpoint:`/info/<entry_type>` endpoint of the index meta-database for that provider.
They MAY also provide human-readable webpages for their definitions.

Definition-provider-specific fields MAY be fully described at the relevant :endpoint:`/info/<entry_type>` endpoint (see section `Entry Listing Info Endpoints`_), but can also rely on the canonical definitions provided by the definition provider, provided they return an ``$id`` for the field that resolves to the relevant OPTIMADE property definition.

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

For example, the following query can be sent to API implementations ``exmpl1`` and ``exmpl2`` without generating any errors:

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

Example of a response in the JSON response format with two structure entries that each include a metadata property for the attribute field :field:`elements_ratios` and the database-specific per entry metadata field :field:`_exmpl_originates_from_project`:

.. code:: jsonc

     {
       "data": [
         {
           "type": "structures",
           "id": "example.db:structs:0001",
           "attributes": {
             "elements_ratios":[0.33336, 0.22229, 0.44425]
           },
           "meta": {
             "property_metadata": {
               "elements_ratios": {
                 "_exmpl_originates_from_project": "piezoelectic_perovskites"
               }
             }
           }
         },
         {
           "type": "structures",
           "id": "example.db:structs:1234",
           "attributes": {
             "elements_ratios":[0.5, 0.5]
           },
           "meta": {
             "property_metadata":{
               "elements_ratios": {
                 "_exmpl_originates_from_project": "ferroelectric_binaries"
               }
             }
           }
         }
         //...
       ]
       // ...
     }

Example of the corresponding metadata property definition contained in the field :field:`x-optimade-metadata-definition` which is placed in the property definition of :field:`elements_ratios`:

.. code:: jsonc

     // ...
     "x-optimade-metadata-definition": {
       "title": "Metadata for the elements_ratios field",
       "description": "This field contains the per-entry metadata for the elements_ratios field.",
       "x-optimade-type": "dictionary",
       "x-optimade-unit": "inapplicable",
       "type": ["object", "null"],
       "properties" : {
         "_exmpl_originates_from_project": {
           "$id": "https://properties.example.com/v1.2.0/elements_ratios_meta/_exmpl_originates_from_project",
           "description" : "A string naming the internal example.com project id where this property was added to the database.",
           "x-optimade-type": "string",
           "x-optimade-unit" : "inapplicable",
           "type": ["string", "null"]
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

Database-provider-specific and definition-provider-specific :query-param:`response_format` identifiers MUST include the corresponding prefix (see section `Namespace Prefixes`_).

JSON Response Schema: Common Fields
-----------------------------------

In the JSON response format, property types translate as follows:

- **string**, **boolean**, **list** are represented by their similarly named counterparts in JSON.
- **integer**, **float** are represented as the JSON number type.
- **timestamp** uses a string representation of date and time as defined in `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__.
- **dictionary** is represented by the JSON object type.
- **unknown** properties are represented by either omitting the property or by a JSON :field-val:`null` value.
- database-provider-specific or definition-provider-specific data types use string representations.

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

    Implementation note: the functionality of this field overlaps to some degree with features provided by the HTTP error :http-error:`429 Too Many Requests` and the `Retry-After HTTP header <https://tools.ietf.org/html/rfc7231.html#section-7.1.3>`__.
    Implementations are suggested to provide consistent handling of request overload through both mechanisms.

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

Entry Listing Endpoints
-----------------------

Entry listing endpoints return a list of resource objects representing entries of a specific type.
For example, a list of structures, or a list of calculations.

Each entry in the list includes a set of properties and their corresponding values.
The section `Entry list`_ specifies properties as belonging to one of three categories:

1. Properties marked as REQUIRED in the response.
   These properties MUST always be present for all entries in the response.

2. Properties marked as REQUIRED only if the query parameter :query-param:`response_fields` is not part of the request, or if they are explicitly requested in :query-param:`response_fields`.
   Otherwise they MUST NOT be included.
   One can think of these properties as constituting a default value for :query-param:`response_fields` when that parameter is omitted.

3. Properties not marked as REQUIRED in any case, MUST be included only if explicitly requested in the query parameter :query-param:`response_fields`.
   Otherwise they SHOULD NOT be included.

Examples of valid entry listing endpoint URLs:

- http://example.com/optimade/v1/structures
- http://example.com/optimade/v1/calculations

There MAY be multiple entry listing endpoints, depending on how many types of entries an implementation provides.
Specific standard entry types are specified in section `Entry list`_.

The API implementation MAY provide other entry types than the ones standardized in this specification.
Such entry types MUST be prefixed by a database-provider-specific prefix (i.e., the resource objects' :property:`type` value should start with the database-provider-specific prefix, e.g., :property:`type` = :val:`_exmpl_workflows`).
Each custom entry type SHOULD be served at a corresponding entry listing endpoint under the versioned or unversioned base URL that serves the API with the same name (i.e., equal to the resource objects' :property:`type` value, e.g., :endpoint:`/_exmpl_workflows`).
It is RECOMMENDED to align with the OPTIMADE API specification practice of using a plural for entry resource types and entry type endpoints.
Any custom entry listing endpoint MUST also be added to the :property:`available_endpoints` and :property:`entry_types_by_format` attributes of the `Base Info Endpoint`_.

For more on custom endpoints, see `Custom Extension Endpoints`_.

Entry Listing URL Query Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The client MAY provide a set of URL query parameters in order to alter the response and provide usage information. While these URL query parameters are OPTIONAL for clients, API implementations MUST accept and handle them.
To adhere to the requirement on implementation-specific URL query parameters of `JSON:API v1.1 <http://jsonapi.org/format/1.1>`__, query parameters that are not standardized by that specification have been given names that consist of at least two words separated by an underscore (a LOW LINE character '\_').

Standard OPTIONAL URL query parameters standardized by the JSON:API specification:

- **filter**: a filter string, in the format described below in section `API Filtering Format Specification`_.

- **page\_limit**: sets a numerical limit on the number of entries returned.
  See `JSON:API 1.1 <https://jsonapi.org/format/1.1/#fetching-pagination>`__.
  The API implementation MUST return no more than the number specified.
  It MAY return fewer.
  The database MAY have a maximum limit and not accept larger numbers (in which case the :http-error:`403 Forbidden` error code MUST be returned).
  The default limit value is up to the API implementation to decide.
  Example: :query-url:`http://example.com/optimade/v1/structures?page_limit=100`

- **page\_{offset, number, cursor, above, below}**: A server MUST implement pagination in the case of no user-specified :query-param:`sort` parameter (via the :field:`links` response field, see section `JSON Response Schema: Common Fields`_).
  A server MAY implement pagination in concert with :query-param:`sort`.
  The following parameters, all prefixed by "page\_", are RECOMMENDED for use with pagination.
  If an implementation chooses

  - *offset-based pagination*: using :field:`page_offset` and :field:`page_limit` is RECOMMENDED.
  - *cursor-based pagination*: using :field:`page_cursor` and :field:`page_limit` is RECOMMENDED.
  - *page-based pagination*: using :field:`page_number` and :field:`page_limit` is RECOMMENDED. It is RECOMMENDED that the first page has number 1, i.e., that :field:`page_number` is 1-based.
  - *value-based pagination*: using :field:`page_above`/:field:`page_below` and :field:`page_limit` is RECOMMENDED.

  Examples (all OPTIONAL behavior a server MAY implement):

  - skip 50 structures and fetch up to 100: :query-url:`/structures?page_offset=50&page_limit=100`.
  - fetch page 2 of up to 50 structures per page: :query-url:`/structures?page_number=2&page_limit=50`.
  - fetch up to 100 structures above sort-field value 4000 (in this example, server chooses to fetch results sorted by increasing :field:`id`, so :field:`page_above` value refers to an :field:`id` value): :query-url:`/structures?page_above=4000&page_limit=100`.

- **sort**: If supporting sortable queries, an implementation MUST use the :query-param:`sort` query parameter with format as specified by `JSON:API 1.1 <https://jsonapi.org/format/1.1/#fetching-sorting>`__.

  An implementation MAY support multiple sort fields for a single query.
  If it does, it again MUST conform to the JSON:API 1.1 specification.

  If an implementation supports sorting for an `entry listing endpoint <Entry Listing Endpoints_>`_, then the :endpoint:`/info/<entries>` endpoint MUST include, for each field name :field:`<fieldname>` in its :field:`data.properties.<fieldname>` response value that can be used for sorting, the key :field:`sortable` with value :field-val:`true`.
  If a field name under an entry listing endpoint supporting sorting cannot be used for sorting, the server MUST either leave out the :field:`sortable` key or set it equal to :field-val:`false` for the specific field name.
  The set of field names, with :field:`sortable` equal to :field-val:`true` are allowed to be used in the "sort fields" list according to its definition in the JSON:API 1.1 specification.
  The field :field:`sortable` is in addition to each property description and other OPTIONAL fields.
  An example is shown in section `Entry Listing Info Endpoints`_.

- **include**: A server MAY implement the JSON:API concept of returning `compound documents <https://jsonapi.org/format/1.1/#document-compound-documents>`__ by utilizing the :query-param:`include` query parameter as specified by `JSON:API 1.0 <https://jsonapi.org/format/1.1/#fetching-includes>`__.

  All related resource objects MUST be returned as part of an array value for the top-level :field:`included` field, see section `JSON Response Schema: Common Fields`_.

  The value of :query-param:`include` MUST be a comma-separated list of "relationship paths", as defined in the `JSON:API <https://jsonapi.org/format/1.1/#fetching-includes>`__.
  If relationship paths are not supported, or a server is unable to identify a relationship path a :http-error:`400 Bad Request` response MUST be made.

  The **default value** for :query-param:`include` is :query-val:`references`.
  This means :entry:`references` entries MUST always be included under the top-level field :field:`included` as default, since a server assumes if :query-param:`include` is not specified by a client in the request, it is still specified as :query-string:`include=references`.
  Note, if a client explicitly specifies :query-param:`include` and leaves out :query-val:`references`, :entry:`references` resource objects MUST NOT be included under the top-level field :field:`included`, as per the definition of :field:`included`, see section `JSON Response Schema: Common Fields`_.

    **Note**: A query with the parameter :query-param:`include` set to the empty string means no related resource objects are to be returned under the top-level field :field:`included`.

Standard OPTIONAL URL query parameters not in the JSON:API specification:

- **response\_format**: the output format requested (see section `Response Format`_).
  Defaults to the format string 'json', which specifies the standard output format described in this specification.
  Example: :query-url:`http://example.com/optimade/v1/structures?response_format=xml`
- **email\_address**: an email address of the user making the request.
  The email SHOULD be that of a person and not an automatic system.
  Example: :query-url:`http://example.com/optimade/v1/structures?email_address=user@example.com`
- **response\_fields**: a comma-delimited set of fields to be provided in the output.
  If provided, these fields MUST be returned along with the REQUIRED fields.
  Other OPTIONAL fields MUST NOT be returned when this parameter is present.
  Example: :query-url:`http://example.com/optimade/v1/structures?response_fields=last_modified,nsites`

Additional OPTIONAL URL query parameters not described above are not considered to be part of this standard, and are instead considered to be "custom URL query parameters".
These custom URL query parameters MUST be of the format "<database-provider-specific prefix><url\_query\_parameter\_name>".
These names adhere to the requirements on implementation-specific query parameters of `JSON:API v1.1 <http://jsonapi.org/format/1.1>`__ since the database-provider-specific prefixes contain at least two underscores (a LOW LINE character '\_').

Example uses of custom URL query parameters include providing an access token for the request, to tell the database to increase verbosity in error output, or providing a database-specific extended searching format.

Examples:

- :query-url:`http://example.com/optimade/v1/structures?_exmpl_key=A3242DSFJFEJE`
- :query-url:`http://example.com/optimade/v1/structures?_exmpl_warning_verbosity=10`
- :query-url:`http://example.com/optimade/v1/structures?_exmpl_filter="elements all in [Al, Si, Ga]"`

    **Note**: the specification presently makes no attempt to standardize access control mechanisms.
    There are security concerns with access control based on URL tokens, and the above example is not to be taken as a recommendation for such a mechanism.

Entry Listing JSON Response Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"Entry listing" endpoint response dictionaries MUST have a :field:`data` key.
The value of this key MUST be a list containing dictionaries that represent individual entries.
In the default JSON response format every dictionary (`resource object <http://jsonapi.org/format/1.1/#document-resource-objects>`__) MUST have the following fields:

- **type**: field containing the Entry type as defined in section `Definition of Terms`_
- **id**: field containing the ID of entry as defined in section `Definition of Terms`_. This can be the local database ID.
- **attributes**: a dictionary, containing key-value pairs representing the entry's properties, except for :property:`type` and :property:`id`.

  Database-provider-specific and definition-provider-specific properties MUST include the corresponding prefix (see section `Namespace Prefixes`_).

OPTIONALLY it can also contain the following fields:

- **links**: a `JSON:API links object <http://jsonapi.org/format/1.1/#document-links>`__ can OPTIONALLY contain the field

  - **self**: the entry's URL

- **meta**: a `JSON API meta object <https://jsonapi.org/format/1.1/#document-meta>`__ that is used to communicate metadata.
  See `JSON Response Schema: Common Fields`_ for more information about this field.

- **relationships**: a dictionary containing references to other entries according to the description in section `Relationships`_ encoded as `JSON:API Relationships <https://jsonapi.org/format/1.1/#document-resource-object-relationships>`__.
  The OPTIONAL human-readable description of the relationship MAY be provided in the :field:`description` field inside the :field:`meta` dictionary of the JSON:API resource identifier object.
  All relationships to entries of the same entry type MUST be grouped into the same JSON:API relationship object and placed in the relationships dictionary with the entry type name as key (e.g., :entry:`structures`).

Example:

.. code:: jsonc

     {
       "data": [
         {
           "type": "structures",
           "id": "example.db:structs:0001",
           "attributes": {
             "chemical_formula_descriptive": "Es2 O3",
             "url": "http://example.db/structs/0001",
             "immutable_id": "http://example.db/structs/0001@123",
             "last_modified": "2007-04-05T14:30:20Z"
           }
         },
         {
           "type": "structures",
           "id": "example.db:structs:1234",
           "attributes": {
             "chemical_formula_descriptive": "Es2",
             "url": "http://example.db/structs/1234",
             "immutable_id": "http://example.db/structs/1234@123",
             "last_modified": "2007-04-07T12:02:20Z"
           }
         }
         // ...
       ]
       // ...
     }

Single Entry Endpoints
----------------------

A client can request a specific entry by appending a URL-encoded ID path segment to the URL of an entry listing endpoint. This will return properties for the entry with that ID.

In the default JSON response format, the ID component MUST be the content of the :field:`id` field.

Examples:

- :query-url:`http://example.com/optimade/v1/structures/exmpl%3Astruct_3232823`
- :query-url:`http://example.com/optimade/v1/calculations/232132`

The rules for which properties are to be present for an entry in the response are the same as defined in section `Entry Listing Endpoints`_.

Single Entry URL Query Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The client MAY provide a set of additional URL query parameters for this endpoint type.
URL query parameters not recognized MUST be ignored.
While the following URL query parameters are OPTIONAL for clients, API implementations MUST accept and handle them:
:query-param:`response_format`, :query-param:`email_address`, :query-param:`response_fields`.
The URL query parameter :query-param:`include` is OPTIONAL for both clients and API implementations.
The meaning of these URL query parameters are as defined above in section `Entry Listing URL Query Parameters`_.

Single Entry JSON Response Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The response for a 'single entry' endpoint is the same as for 'entry listing' endpoint responses, except that the value of the :field:`data` field MUST have only one or zero entries.
In the default JSON response format, this means the value of the :field:`data` field MUST be a single response object or :field-val:`null` if there is no response object to return.

Example:

.. code:: jsonc

     {
       "data": {
         "type": "structures",
         "id": "example.db:structs:1234",
         "attributes": {
           "chemical_formula_descriptive": "Es2",
           "url": "http://example.db/structs/1234",
           "immutable_id": "http://example.db/structs/1234@123",
           "last_modified": "2007-04-07T12:02:20Z"
         }
       },
       "meta": {
         "query": {
           "representation": "/structures/example.db:structs:1234?"
         }
         // ...
       }
       // ...
     }

Info Endpoints
--------------

Info endpoints provide introspective information, either about the API implementation itself, or about specific entry types.

There are two types of info endpoints:

1. Base info endpoints: placed directly under the versioned or unversioned base URL that serves the API (e.g., http://example.com/optimade/v1/info or http://example.com/optimade/info)
2. Entry listing info endpoints: placed under the endpoints belonging to specific entry types (e.g., http://example.com/optimade/v1/info/structures or http://example.com/optimade/info/structures)

The types and output content of these info endpoints are described in more detail in the subsections below.
Common for them all are that the :field:`data` field SHOULD return only a single resource object.
If no resource object is provided, the value of the :field:`data` field MUST be :field-val:`null`.

Base Info Endpoint
~~~~~~~~~~~~~~~~~~

The Info endpoint under a versioned or unversioned base URL serving the API (e.g. http://example.com/optimade/v1/info or http://example.com/optimade/info) returns information relating to the API implementation.

The single resource object's response dictionary MUST include the following fields:

- **type**: :field-val:`"info"`
- **id**: :field-val:`"/"`
- **attributes**: Dictionary containing the following fields:

  - **api\_version**: Presently used full version of the OPTIMADE API.
    The version number string MUST NOT be prefixed by, e.g., "v".
    Examples: :field-val:`1.0.0`, :field-val:`1.0.0-rc.2`.

  - **available\_api\_versions**: MUST be a list of dictionaries, each containing the fields:

    - **url**: a string specifying a versioned base URL that MUST adhere to the rules in section `Base URL`_
    - **version**: a string containing the full version number of the API served at that versioned base URL.
      The version number string MUST NOT be prefixed by, e.g., "v".
      Examples: :field-val:`1.0.0`, :field-val:`1.0.0-rc.2`.

  - **formats**: List of available output formats.
  - **entry\_types\_by\_format**: Available entry endpoints as a function of output formats.
  - **available\_endpoints**: List of available endpoints (i.e., the string to be appended to the versioned or unversioned base URL serving the API).
  - **license**: A `JSON API link <http://jsonapi.org/format/1.1/#document-links>`__ giving a URL to a web page containing a human-readable text describing the license (or licensing options if there are multiple) covering all the data and metadata provided by this database.

    Clients are advised not to try automated parsing of this link or its content, but rather rely on the field :field:`available_licenses` instead.
    Example: :field-val:`https://example.com/licenses/example_license.html`.

  :field:`attributes` MAY also include the following OPTIONAL fields:

  - **is\_index**: if :field-val:`true`, this is an index meta-database base URL (see section `Index Meta-Database`_).

    If this member is *not* provided, the client MUST assume this is **not** an index meta-database base URL (i.e., the default is for :field:`is_index` to be :field-val:`false`).

  - **available\_licenses**: List of `SPDX license identifiers <https://spdx.org/licenses/>`__ specifying a set of alternative licenses available to the client for licensing the complete database, i.e., all the entries, metadata, and the content and structure of the database itself.
    If more than one license is available to the client, the identifier of each one SHOULD be included in the list.
    Inclusion of a license identifier in the list is a commitment of the database that the rights are in place to grant clients access to all the individual entries, all metadata, and the content and structure of the database itself according to the terms of any of these licenses (at the choice of the client).
    If the licensing information provided via the field :field:`license` omits licensing options specified in :field:`available_licenses`, or if it otherwise contradicts them, a client MUST still be allowed to interpret the inclusion of a license in :field:`available_licenses` as a full commitment from the database without exceptions, under the respective licenses.
    If the database cannot make that commitment, e.g., if only part of the database is available under a license, the corresponding license identifier MUST NOT appear in :field:`available_licenses` (but, rather, the field :field:`license` is to be used to clarify the licensing situation.)
    An empty list indicates that none of the SPDX licenses apply and that the licensing situation is clarified in human readable form in the field :field:`license`.
    An unknown value means that the database makes no commitment.

  - **available\_licenses\_for\_entries**: List of `SPDX license identifiers <https://spdx.org/licenses/>`__ specifying a set of additional alternative licenses available to the client for licensing individual, and non-substantial sets of, database entries, metadata, and extracts from the database that do not constitute substantial parts of the database.
    Note that the definition of the field :field:`available_licenses` implies that licenses specified in that field are available also for the licensing specified by this field, even if they are not explicitly included in the field :field:`available_licenses_for_entries` or if it is :val:`null` (however, the opposite relationship does not hold).
    If :field:`available_licenses` is unknown, only the licenses in :field:`available_licenses_for_entries` apply.

If this is an index meta-database base URL (see section `Index Meta-Database`_), then the response dictionary MUST also include the field:

- **relationships**: Dictionary that MAY contain a single `JSON:API relationships object <https://jsonapi.org/format/1.1/#document-resource-object-relationships>`__:

  - **default**: Reference to the links identifier object under the :endpoint:`links` endpoint that the provider has chosen as their "default" OPTIMADE API database.
    A client SHOULD present this database as the first choice when an end-user chooses this provider.
    This MUST include the field:

    - **data**: `JSON:API resource linkage <http://jsonapi.org/format/1.1/#document-links>`__.
      It MUST be either :field-val:`null` or contain a single links identifier object with the fields:

      - **type**: :field-val:`links`
      - **id**: ID of the provider's chosen default OPTIMADE API database.
        MUST be equal to a valid child object's :field:`id` under the :field:`links` endpoint.

  Lastly, :field:`is_index` MUST also be included in :field:`attributes` and be :field-val:`true`.

Example:

.. code:: jsonc

    {
      "data": {
        "type": "info",
        "id": "/",
        "attributes": {
          "api_version": "1.0.0",
          "available_api_versions": [
            {"url": "http://db.example.com/optimade/v0/", "version": "0.9.5"},
            {"url": "http://db.example.com/optimade/v0.9/", "version": "0.9.5"},
            {"url": "http://db.example.com/optimade/v0.9.2/", "version": "0.9.2"},
            {"url": "http://db.example.com/optimade/v0.9.5/", "version": "0.9.5"},
            {"url": "http://db.example.com/optimade/v1/", "version": "1.0.0"},
            {"url": "http://db.example.com/optimade/v1.0/", "version": "1.0.0"}
          ],
          "formats": [
            "json",
            "xml"
          ],
          "entry_types_by_format": {
            "json": [
              "structures",
              "calculations"
            ],
            "xml": [
              "structures"
            ]
          },
          "available_endpoints": [
            "structures",
            "calculations",
            "info",
            "links"
          ],
          "is_index": false
        }
      }
      // ...
    }

Example for an index meta-database:

.. code:: jsonc

    {
      "data": {
        "type": "info",
        "id": "/",
        "attributes": {
          "api_version": "1.0.0",
          "available_api_versions": [
            {"url": "http://db.example.com/optimade/v0/", "version": "0.9.5"},
            {"url": "http://db.example.com/optimade/v0.9/", "version": "0.9.5"},
            {"url": "http://db.example.com/optimade/v0.9.2/", "version": "0.9.2"},
            {"url": "http://db.example.com/optimade/v1/", "version": "1.0.0"},
            {"url": "http://db.example.com/optimade/v1.0/", "version": "1.0.0"}
            ],
          "formats": [
            "json",
            "xml"
          ],
          "entry_types_by_format": {
            "json": [],
            "xml": []
          },
          "available_endpoints": [
            "info",
            "links"
          ],
          "is_index": true
        },
        "relationships": {
          "default": {
            "data": { "type": "links", "id": "perovskites" }
          }
        }
      }
      // ...
    }

Entry Listing Info Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Entry listing info endpoints are accessed under the versioned or unversioned base URL serving the API as :endpoint:`/info/<entry_type>` (e.g., http://example.com/optimade/v1/info/structures or http://example.com/optimade/info/structures).
They return information related to the specific entry types served by the API.
The response for these endpoints MUST include the following information in the :field:`data` field:

- **type**: :field-val:`"info"`.
- **id**: This MUST precisely match the entry type name, e.g., :field-val:`"structures"` for the :endpoint:`/info/structures`.
- **description**: Description of the entry.
- **properties**: A dictionary describing properties for this entry type, where each key is a property name and the value is an OPTIMADE Property Definition described in detail in the section `Property Definitions`_.
- **formats**: List of output formats available for this type of entry (see section `Response Format`_)
- **output\_fields\_by\_format**: Dictionary of available output fields for this entry type, where the keys are the values of the :field:`formats` list and the values are the keys of the :field:`properties` dictionary.

    **Note**: Future versions of the OPTIMADE API will deprecate this format and require all keys that are not :field:`type` or :field:`id` to be under the :field:`attributes` key.

An example of the data part of the entry listing info endpoint response follows below, however, note that:

- The description strings have been wrapped for readability only (newline characters are not allowed inside JSON strings)
- The properties in the example, 'nelements' and 'lattice_vectors', mimick OPTIMADE standard properties, but are given here with simplified definitions compared to the standard definitions for these properties.

.. code:: jsonc

    {
      "data": {
        "type": "info",
        "id": "structures",
        "description": "a structures entry",
        "properties": {
          "nelements": {
            "$id": "urn:uuid:10a05e55-0c20-4f68-89ad-35a18eb7076f",
            "title": "Number of elements",
            "x-optimade-type": "integer",
            "type": ["integer", "null"],
            "description": "Number of different elements in the structure as an integer.\n
             \n
             -  Note: queries on this property can equivalently be formulated using `elements LENGTH`.\n
             -  A filter that matches structures that have exactly 4 elements: `nelements=4`.\n
             -  A filter that matches structures that have between 2 and 7 elements: `nelements>=2 AND nelements<=7`.",
            "examples": [
              3
            ],
            "x-optimade-property": {
               "property-format": "1.2"
            },
            "x-optimade-unit": "dimensionless",
            "x-optimade-implementation": {
              "sortable": true,
              "query-support": "all mandatory"
            },
            "x-optimade-requirements": {
              "support": "should",
              "sortable": false,
              "query-support": "all mandatory"
            }
          },
          "lattice_vectors": {
            "$id": "urn:uuid:81edf372-7b1b-4518-9c14-7d482bd67834",
            "title": "Lattice vectors",
            "x-optimade-definition": {
              "label": "lattice_vectors_optimade_structures",
              "kind": "property",
              "format": "1.2",
              "version": "1.2.0",
              "name": "lattice_vectors"
            },
            "x-optimade-type": "list",
            "x-optimade-dimensions": {
               "names": ["dim_lattice", "dim_spatial"],
               "lengths": [3, 3]
            },
            "x-optimade-unit-definitions": [
                {
                  "symbol": "angstrom",
                  "title": "ångström",
                  "description": "The ångström unit of length.",
                  "standard": {
                    "name": "gnu units",
                    "version": "3.09",
                    "symbol": "angstrom"
                  }
                }
              ],
            "x-optimade-unit": "inapplicable",
            "x-optimade-implementation": {
              "sortable": false,
              "query-support": "none"
            },
            "x-optimade-requirements": {
              "support": "should",
              "sortable": false,
              "query-support": "none"
            },
            "type": ["array", "null"],
            "description": "The three lattice vectors in Cartesian coordinates, in ångström (Å).\n
            \n
            - MUST be a list of three vectors *a*, *b*, and *c*, where each of the vectors MUST BE a
              list of the vector's coordinates along the x, y, and z Cartesian coordinates.
            ",
            "examples": [
              [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 1.0, 4.0]]
            ],
            "items": {
              "type": "array",
              "x-optimade-type": "list",
              "x-optimade-unit": "inapplicable",
              "x-optimade-dimensions": {
                "names": ["dim_spatial"],
                "lengths": [3]
              },
              "items": {
                "type": "number",
                "x-optimade-type": "float",
                "x-optimade-unit": "angstrom",
                "x-optimade-implementation": {
                  "sortable": true,
                  "query-support": "none"
                },
                "x-optimade-requirements": {
                  "sortable": false,
                  "query-support": "none"
                }
              }
            }
          }
          // ... <other property descriptions>
        },
        "formats": ["json", "xml"],
        "output_fields_by_format": {
          "json": [
            "nelements",
            "lattice_vectors",
            // ...
          ],
          "xml": ["nelements"]
        }
      }
      // ...
    }

Links Endpoint
--------------

This endpoint exposes information on other OPTIMADE API implementations that are related to the current implementation.
The links endpoint MUST be provided under the versioned or unversioned base URL serving the API at :endpoint:`/links`.

Link Types
~~~~~~~~~~

Each link has a :property:`link_type` attribute that specifies the type of the linked relation.

The :property:`link_type` MUST be one of the following values:

- :field-val:`child`: a link to another OPTIMADE implementation that MUST be within the same provider.
  This allows the creation of a tree-like structure of databases by pointing to children sub-databases.
- :field-val:`root`: a link to the root implementation within the same provider.
  This is RECOMMENDED to be an `Index Meta-Database`_.
  There MUST be only one :val:`root` implementation per provider and all implementations MUST have a link to this :val:`root` implementation.
  If the provider only supplies a single implementation, the :val:`root` link links to the implementation itself.
- :field-val:`external`: a link to an external OPTIMADE implementation.
  This MAY be used to point to any other implementation, also in a different provider.
- :field-val:`providers`: a link to a `List of Providers Links`_ implementation that includes the current implementation, e.g. `providers.optimade.org <https://providers.optimade.org/>`__.

Limiting to the :val:`root` and :val:`child` link types, links can be used as an introspective endpoint, similar to the `Info Endpoints`_, but at a higher level, i.e., `Info Endpoints`_ provide information on the given implementation, while the :endpoint:`/links` endpoint provides information on the links between immediately related implementations (in particular, an array of none or a single object with link type :val:`root` and none or more objects with link type :val:`child`, see section `Internal Links: Root and Child Links`_).

For :endpoint:`/links` endpoints, the API implementation MAY ignore any provided query parameters.
Alternatively, it MAY handle the parameters specified in section `Entry Listing URL Query Parameters`_ for entry listing endpoints.

Links Endpoint JSON Response Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The resource objects' response dictionaries MUST include the following fields:

- **type**: MUST be :field-val:`"links"`.
- **id**: MUST be unique.
- **attributes**: Dictionary that MUST contain the following fields:

  - **name**: Human-readable name for the OPTIMADE API implementation, e.g., for use in clients to show the name to the end-user.
  - **description**: Human-readable description for the OPTIMADE API implementation, e.g., for use in clients to show a description to the end-user.
  - **base\_url**: `JSON API link <http://jsonapi.org/format/1.1/#document-links>`__, pointing to the base URL for this implementation, either directly as a string, or as an object, which can contain the following fields:


    - **href**: a string containing the OPTIMADE base URL.
    - **meta**: a meta object containing non-standard meta-information about the implementation.

  - **homepage**: a `JSON API link <http://jsonapi.org/format/1.1/#document-links>`__, pointing to a homepage URL for this implementation, either directly as a string, or as an object, which can contain the following fields:

    - **href**: a string containing the implementation homepage URL.
    - **meta**: a meta object containing non-standard meta-information about the homepage.

  - **link\_type**: a string containing the link type.
    It MUST be one of the values listed above in section `Link Types`_.

  - **aggregate**: a string indicating whether a client that is following links to aggregate results from different OPTIMADE implementations should follow this link or not. This flag SHOULD NOT be indicated for links where :property:`link_type` is not :val:`child`.

    If not specified, clients MAY assume that the value is :val:`ok`.
    If specified, and the value is anything different than :val:`ok`, the client MUST assume that the server is suggesting not to follow the link during aggregation by default (also if the value is not among the known ones, in case a future specification adds new accepted values).

    Specific values indicate the reason why the server is providing the suggestion.
    A client MAY follow the link anyway if it has reason to do so (e.g., if the client is looking for all test databases, it MAY follow the links where :property:`aggregate` has value :val:`test`).

    If specified, it MUST be one of the values listed in section `Link Aggregate Options`_.

  - **no_aggregate_reason**: an OPTIONAL human-readable string indicating the reason for suggesting not to aggregate results following the link. It SHOULD NOT be present if :property:`aggregate` has value :val:`ok`.

Example:

.. code:: jsonc

    {
      "data": [
        {
          "type": "links",
          "id": "index",
          "attributes": {
            "name": "Index",
            "description": "Index for example's OPTIMADE databases",
            "base_url": "http://example.com/optimade",
            "homepage": "http://example.com",
            "link_type": "root"
          }
        },
        {
          "type": "links",
          "id": "cat_zeo",
          "attributes": {
            "name": "Catalytic Zeolites",
            "description": "Zeolites for deNOx catalysis",
            "base_url": {
              "href": "http://example.com/optimade/denox/zeolites",
              "meta": {
                "_exmpl_catalyst_group": "denox"
              }
            },
            "homepage": "http://example.com",
            "link_type": "child"
          }
        },
        {
          "type": "links",
          "id": "frameworks",
          "attributes": {
            "name": "Zeolitic Frameworks",
            "description": "",
            "base_url": "http://example.com/zeo_frameworks/optimade",
            "homepage": "http://example.com",
            "link_type": "child"
          }
        },
        {
          "type": "links",
          "id": "testdb",
          "attributes": {
            "name": "Test database",
            "description": "A test database",
            "base_url": "http://example.com/testdb/optimade",
            "homepage": "http://example.com",
            "link_type": "child",
            "aggregate": "test"
          }
        },
        {
          "type": "links",
          "id": "internaldb",
          "attributes": {
            "name": "Database for internal use",
            "description": "An internal database",
            "base_url": "http://example.com/internaldb/optimade",
            "homepage": "http://example.com",
            "link_type": "child",
            "aggregate": "no",
            "no_aggregate_reason": "This is a database for internal use and might contain nonsensical data"
          }
        },
        {
          "type": "links",
          "id": "frameworks",
          "attributes": {
            "name": "Some other DB",
            "description": "A DB by the example2 provider",
            "base_url": "http://example2.com/some_db/optimade",
            "homepage": "http://example2.com",
            "link_type": "external"
          }
        },
        {
          "type": "links",
          "id": "optimade",
          "attributes": {
            "name": "Materials Consortia",
            "description": "List of OPTIMADE providers maintained by the Materials Consortia organisation",
            "base_url": "https://providers.optimade.org",
            "homepage": "https://optimade.org",
            "link_type": "providers"
          }
        }
      ]
    }

Internal Links: Root and Child Links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any number of resource objects with :property:`link_type` equal to :val:`child` MAY be present as part of the :field:`data` list.
A :val:`child` object represents a "link" to an OPTIMADE implementation within the same provider exactly one layer **below** the current implementation's layer.

Exactly one resource object with :property:`link_type` equal to :val:`root` MUST be present as part of the :field:`data` list.
Note: the same implementation may of course be linked by other implementations via a :endpoint:`/links` endpoint with :property:`link_type` equal to :val:`external`.

The :val:`root` resource object represents a link to the topmost OPTIMADE implementation of the current provider.
By following :val:`child` links from the :val:`root` object recursively, it MUST be possible to reach the current OPTIMADE implementation.

In practice, this forms a tree structure for the OPTIMADE implementations of a provider.
**Note**: The RECOMMENDED number of layers is two.

List of Providers Links
~~~~~~~~~~~~~~~~~~~~~~~

Resource objects with :property:`link_type` equal to :val:`providers` MUST point to an `Index Meta-Database`_ that supplies a list of OPTIMADE database providers.
The intention is to be able to auto-discover all providers of OPTIMADE implementations.

A list of known database providers can be retrieved as described in section `Namespace Prefixes`_.
This section also describes where to find information for how a provider can be added to this list.

Index Meta-Database Links Endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the provider implements an `Index Meta-Database`_, it is RECOMMENDED to adopt a structure where the index meta-database is the :val:`root` implementation of the provider.

This will make all OPTIMADE databases and implementations by the provider discoverable as links with :val:`child` link type, under the :endpoint:`links` endpoint of the `Index Meta-Database`_.

Link Aggregate Options
~~~~~~~~~~~~~~~~~~~~~~

If specified, the :property:`aggregate` attributed MUST have one of the following values:

- :val:`ok` (default value, if unspecified): it is ok to follow this link when aggregating OPTIMADE results.
- :val:`test`: the linked database is a test database,  whose content might not be correct or might not represent physically-meaningful data. Therefore by default the link should not be followed.
- :val:`staging`: the linked database is almost production-ready, but final checks on its content are being performed, so the content might still contain errors. Therefore by default the link should not be followed.
- :val:`no`: any other reason to suggest not to follow the link during aggregation of OPTIMADE results. The implementation MAY provide mode details in a human-readable form via the attribute :property:`no-aggregate-reason`.

Custom Extension Endpoints
--------------------------

API implementations MAY provide custom endpoints under the Extensions endpoint.
Custom extension endpoints MUST be placed under the versioned or unversioned base URL serving the API at :endpoint:`/extensions`.
The API implementation is free to define roles of further URL path segments under this URL.

API Filtering Format Specification
==================================

An OPTIMADE filter expression is passed in the parameter :query-param:`filter` as a URL query parameter as `specified by JSON:API <https://jsonapi.org/format/1.1/#fetching-filtering>`__.
The filter expression allows desired properties to be compared against search values; several such comparisons can be combined using the logical conjunctions AND, OR, NOT, and parentheses, with their usual semantics.

All properties marked as REQUIRED in section `Entry list`_ MUST be queryable with all mandatory filter features.
The level of query support REQUIRED for other properties is described in `Entry list`_.

When provided as a URL query parameter, the contents of the :query-param:`filter` parameter is URL-encoded by the client in the HTTP GET request, and then URL-decoded by the API implementation before any further parsing takes place.
In particular, this means the client MUST escape special characters in string values as described below for `String values`_ before the URL encoding, and the API implementation MUST first URL-decode the :query-param:`filter` parameter before reversing the escaping of string tokens.

Examples of syntactically correct query strings embedded in queries:

- :query-url:`http://example.org/optimade/v1/structures?filter=_exmpl_melting_point%3C300+AND+nelements=4+AND+chemical_formula_descriptive="SiO2"&response_format=xml`

Or, fully URL encoded:

- :query-url:`http://example.org/optimade/v1/structures?filter=_exmpl_melting_point%3C300+AND+nelements%3D4+AND+chemical_formula_descriptive%3D%22SiO2%22&response_format=xml`

Lexical Tokens
--------------

The following tokens are used in the filter query component:

- **Property names**: the first character MUST be a lowercase letter, the subsequent symbols MUST be composed of lowercase letters or digits; the underscore ("\_", ASCII 95 dec (0x5F)) is considered to  be a lower-case letter when defining identifiers.
  The length of the identifiers is not limited, except that when passed as a URL query parameter the whole query SHOULD NOT be longer than the limits imposed by the URI specification.
  This definition is similar to one used in most widespread programming languages, except that OPTIMADE limits allowed letter set to lowercase letters only.
  This allows to tell OPTIMADE identifiers and operator keywords apart unambiguously without consulting a reserved word table and to encode this distinction concisely in the EBNF Filter Language grammar.

  Examples of valid property names:

  - :property:`band_gap`
  - :property:`cell_length_a`
  - :property:`cell_volume`

  Examples of incorrect property names:

  - :property-fail:`0_kvak` (starts with a number);
  - :property-fail:`"foo bar"` (contains space; contains quotes)
  - :property-fail:`BadLuck` (contains upper-case letters)

  Identifiers that start with an underscore are specific to a database or definition provider, and MUST be on the format of a namespace prefix (see section `Namespace Prefixes`_).

  Examples:

  - :property:`_exmpl_formula_sum` (a property specific to that database)
  - :property:`_exmpl_band_gap`
  - :property:`_exmpl_supercell`
  - :property:`_exmpl_trajectory`
  - :property:`_exmpl_workflow_id`

- **Nested property names** A nested property name is composed of at least two identifiers separated by periods (``.``).

.. _string values:

- **String values** MUST be surrounded by double quote characters (``"``, ASCII symbol 34 dec, 0x22 hex).
  A double quote that is a part of the value, not a delimiter, MUST be escaped by prepending it with a backslash character (``\\``, ASCII symbol 92 dec, 0x5C hex).
  A backslash character that is part of the value (i.e., not used to escape a double quote) MUST be escaped by prepending it with another backslash.
  An example of an escaped string value, including the enclosing double quotes, is given below:

  - "A double quote character (\\", ASCII symbol 34 dec) MUST be prepended by a backslash (\\\\, ASCII symbol 92 dec) when it is a part of the value and not a delimiter; the backslash character \\"\\\\\\" itself MUST be preceded by another backslash, forming a double backslash: \\\\\\\\"

  (Note that at the end of the string value above the four final backslashes represent the two terminal backslashes in the value, and the final double quote is a terminator, it is not escaped.)

  String value tokens are also used to represent **timestamps** in form of the `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__.
  String value tokens as well are used to represent database-provider-specific or definition-provider-specific data types.

- **Numeric values** are represented as decimal integers or in scientific notation, using the usual programming language conventions.
  A regular expression giving the number syntax is given below as a `POSIX Extended Regular Expression (ERE) <https://en.wikipedia.org/w/index.php?title=Regular_expression&oldid=786659796#Standards>`__ or as a `Perl-Compatible Regular Expression (PCRE) <http://www.pcre.org>`__:

  - ERE: :ere:`[-+]?([0-9]+(\.[0-9]\*)?|\.[0-9]+)([eE][-+]?[0-9]+)?`
  - PCRE: :pcre:`[-+]?(?:\d+(\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?`

An implementation of the search filter MAY reject numbers that are outside the machine representation of the underlying hardware; in such case it MUST return the error :http-error:`501 Not Implemented` with an appropriate error message that indicates the cause of the error and an acceptable number range.

- Examples of valid numbers:

  - 12345, +12, -34, 1.2, .2E7, -.2E+7, +10.01E-10, 6.03e23, .1E1, -.1e1, 1.e-12, -.1e-12, 1000000000.E1000000000, 1., .1

- Examples of *invalid* numbers (although they MAY contain correct numbers as substrings):

  - 1.234D12, .e1, -.E1, +.E2, 1.23E+++, +-123

- **Note**: this number representation is more general than the number representation in JSON (for instance, ``1.`` is a valid numeric value for the filtering language specified here, but is not a valid float number in JSON, where the correct format is ``1.0`` instead).

While the filtering language supports tests for equality between properties of floating point type and decimal numbers given in the filter string, such comparisons come with the usual caveats for testing for equality of floating point numbers.
Normally, a client cannot rely on that a floating point number stored in a database takes on a representation that exactly matches the one obtained for a number given in the filtering string as a decimal number or as an integer.
However, testing for equality to zero MUST be supported.

More examples of the number tokens and machine-readable definitions and tests can be found in the `Materials-Consortia API Git repository <https://github.com/Materials-Consortia/API/>`__ (files `integers.lst <https://github.com/Materials-Consortia/API/blob/master/tests/inputs/integers.lst>`__, `not-numbers.lst <https://github.com/Materials-Consortia/API/blob/master/tests/inputs/not-numbers.lst>`__, `numbers.lst <https://github.com/Materials-Consortia/API/blob/master/tests/inputs/numbers.lst>`__, and `reals.lst <https://github.com/Materials-Consortia/API/blob/master/tests/inputs/reals.lst>`__).

- **Boolean values** are represented with the tokens :filter-op:`TRUE` and :filter-op:`FALSE`.

- **Operator tokens** are represented by usual mathematical relation symbols or by case-sensitive keywords.
  Currently the following operators are supported: :filter-op:`=`, :filter-op:`!=`, :filter-op:`<=`, :filter-op:`>=`, :filter-op:`<`, :filter-op:`>` for tests of number, string (lexicographical) or timestamp (temporal) equality, inequality, less-than, more-than, less, and more relations; :filter-op:`AND`, :filter-op:`OR`, :filter-op:`NOT` for logical conjunctions, and a number of keyword operators discussed in the next section.

  In future extensions, operator tokens that are words MUST contain only upper-case letters.
  This requirement guarantees that no operator token will ever clash with a property name.

The Filter Language Syntax
--------------------------

All filtering expressions MUST follow the `EBNF <http://standards.iso.org/ittf/PubliclyAvailableStandards/s026153_ISO_IEC_14977_1996(E).zip>`__ grammar of appendix `The Filter Language EBNF Grammar`_ of this specification.
The appendix contains a complete machine-readable EBNF, including the definition of the lexical tokens described above in section `Lexical Tokens`_. The EBNF is enclosed in special strings constructed as ``BEGIN`` and ``END``, both followed by ``EBNF GRAMMAR Filter``, to enable automatic extraction.

Basic boolean operations
~~~~~~~~~~~~~~~~~~~~~~~~

The filter language supports conjunctions of comparisons using the boolean algebra operators "AND", "OR", and "NOT" and parentheses to group conjunctions.
A comparison clause prefixed by NOT matches entries for which the comparison is false.

Examples:

- :filter:`NOT ( chemical_formula_hill = "Al" AND chemical_formula_anonymous = "A" OR chemical_formula_anonymous = "H2O" AND NOT chemical_formula_hill = "Ti" )`

Numeric and String comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comparisons involving Numeric and String properties can be expressed using the usual comparison operators: '<', '>', '<=', '>=', '=', '!='.
Implementations MUST support comparisons in the forms::

    identifier <operator> constant
    constant <operator> identifier

Where :filter-fragment:`identifier` is a property name and :filter-fragment:`constant` is either a numerical or string type constant.

Implementations MAY also support comparisons with identifiers on both sides, and comparisons with numerical type constants on both sides, i.e., in the forms::

    identifier <operator> identifier
    constant <operator> constant

However, the latter form, :filter-fragment:`constant <operator> constant` where the constants are strings MUST return the error :http-error:`501 Not Implemented`.

    **Note:** The motivation to exclude the form :filter-fragment:`constant <operator> constant` for strings is that filter language strings can refer to data of different data types (e.g., strings and timestamps), and thus this construct is not unambiguous.
    The OPTIMADE specification will strive to address this issue in a future version.

Examples:

- :filter:`nelements > 3`
- :filter:`chemical_formula_hill = "H2O" AND chemical_formula_anonymous != "AB"`
- :filter:`_exmpl_aax <= +.1e8 OR nelements >= 10 AND NOT ( _exmpl_x != "Some string" OR NOT _exmpl_a = 7)`
- :filter:`_exmpl_spacegroup="P2"`
- :filter:`_exmpl_cell_volume<100.0`
- :filter:`_exmpl_band_gap > 5.0 AND _exmpl_molecular_weight < 350`
- :filter:`_exmpl_melting_point<300 AND nelements=4 AND chemical_formula_descriptive="SiO2"`
- :filter:`_exmpl_some_string_property = 42` (This is syntactically allowed without putting 42 in quotation marks, see the notes about comparisons of values of different types below.)
- :filter:`5 < _exmpl_a`
- OPTIONAL: :filter:`((NOT (_exmpl_a>_exmpl_b)) AND _exmpl_x>0)`
- OPTIONAL: :filter:`5 < 7`

Substring comparisons
~~~~~~~~~~~~~~~~~~~~~

In addition to the standard equality and inequality operators, matching of partial strings is provided by keyword operators:

- :filter:`identifier CONTAINS x`: Is true if the substring value x is found anywhere within the property.

- :filter:`identifier STARTS WITH x`: Is true if the property starts with the substring value x. The :filter-op:`WITH` keyword MAY be omitted.

- :filter:`identifier ENDS WITH x`: Is true if the property ends with the substring value x. The :filter-op:`WITH` keyword MAY be omitted.

OPTIONAL features:

- Support for x to be an identifier, rather than a string is OPTIONAL.

Examples:

- :filter:`chemical_formula_anonymous CONTAINS "C2" AND chemical_formula_anonymous STARTS WITH "A2"`
- :filter:`chemical_formula_anonymous STARTS "A2" AND chemical_formula_anonymous ENDS WITH "D1"`

Comparisons of boolean values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Straightforward comparisons ('=' and '!=') MUST be supported for boolean values.
Other comparison operators ('<', '>', '<=', '>=') MUST NOT be supported.
Boolean values are only supposed to be used in direct comparisons with properties, but not compound comparisons.
For example, :filter:`(nsites = 3 AND nelements = 3) = FALSE` is not supported.

Boolean property :filter-fragment:`property` MAY be compared with :filter-fragment:`TRUE` by omitting the :filter-fragment:`= TRUE` altogether: :filter:`property`.
Conversely, it MAY be compared with :filter-fragment:`FALSE` by negating the comparison with :filter-fragment:`TRUE`: :filter:`NOT property`.

Examples:

- :filter:`property = TRUE`
- :filter:`property != FALSE`
- :filter:`_exmpl_has_inversion_symmetry AND NOT _exmpl_is_primitive`

Comparisons of list properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the following, :property:`list` is a list-type property, and :filter-fragment:`values` is one or more :filter-fragment:`value` separated by commas (","), i.e., strings or numbers.
An implementation MAY also support property names and nested property names in :filter-fragment:`values`.

The following constructs MUST be supported:

- :filter:`list HAS value`: matches if at least one element in :filter-fragment:`list` is equal to :filter-fragment:`value`. (If :filter-fragment:`list` has no duplicate elements, this implements the set operator IN.)
- :filter:`list HAS ALL values`: matches if, for each :filter-fragment:`value`, there is at least one element in :filter-fragment:`list` equal to that value. (If both :filter-fragment:`list` and :filter-fragment:`values` do not contain duplicate values, this implements the set operator >=.)
- :filter:`list HAS ANY values`: matches if at least one element in :filter-fragment:`list` is equal to at least one :filter-fragment:`value`. (This is equivalent to a number of HAS statements separated by OR.)
- :filter:`list LENGTH value`: matches if the number of items in the :filter-fragment:`list` property is equal to :filter-fragment:`value`.

The :filter-fragment:`HAS ONLY` construct MAY be supported:

- OPTIONAL: :filter:`list HAS ONLY values`: matches if all elements in :filter-fragment:`list` are equal to at least one :filter-fragment:`value`.
  (If both :filter-fragment:`list` and :filter-fragment:`values` do not contain duplicate values, this implements the <= set operator.)

This construct is OPTIONAL as it can be difficult to realize in some underlying database implementations.
However, if the desired search is over a property that can only take on a finite set of values (e.g., chemical elements) a client can formulate an equivalent search by inverting the list of values into :filter-fragment:`inverse` and express the filter as :filter:`NOT list HAS inverse`.

Furthermore, there is a set of OPTIONAL constructs that allows filters to be formulated over the values in *correlated positions* in multiple list properties.
An implementation MAY support this syntax selectively only for specific properties.
This type of filter is useful for, e.g., filtering on elements and correlated element counts available as two separate list properties.

- :filter-fragment:`list1:list2:... HAS val1:val2:...`
- :filter-fragment:`list1:list2:... HAS ALL val1:val2:...`
- :filter-fragment:`list1:list2:... HAS ANY val1:val2:...`
- :filter-fragment:`list1:list2:... HAS ONLY val1:val2:...`

Finally, all the above constructs that allow a value or lists of values on the right-hand side MAY allow :filter-fragment:`<operator> value` in each place a value can appear.
In that case, a match requires that the :filter-fragment:`<operator>` comparison is fulfilled instead of equality.
Strictly, the definitions of the :filter-fragment:`HAS`, :filter-fragment:`HAS ALL`, :filter-fragment:`HAS ANY`, :filter-fragment:`HAS ONLY` and :filter-fragment:`LENGTH` operators as written above apply, but with the word 'equal' replaced with the :filter-fragment:`<operator>` comparison.

For example:

- OPTIONAL: :filter:`list HAS < 3`: matches all entries for which :filter-fragment:`list` contains at least one element that is less than three.
- OPTIONAL: :filter:`list HAS ALL < 3, > 3`: matches only those entries for which :filter-fragment:`list` simultaneously contains at least one element less than three and one element greater than three.

An implementation MAY support combining the operator syntax with the syntax for correlated lists in particularly on a list correlated with itself. For example:

- OPTIONAL: :filter:`list:list HAS >=2:<=5`: matches all entries for which :filter-fragment:`list` contains at least one element that is between the values 2 and 5.

Further examples of various comparisons of list properties:

- OPTIONAL: :filter:`elements HAS "H" AND elements HAS ALL "H","He","Ga","Ta" AND elements HAS ONLY "H","He","Ga","Ta" AND elements HAS ANY "H", "He", "Ga", "Ta"`
- OPTIONAL: :filter:`elements HAS ONLY "H","He","Ga","Ta"`
- OPTIONAL: :filter:`elements:_exmpl_element_counts HAS "H":6 AND elements:_exmpl_element_counts HAS ALL "H":6,"He":7 AND elements:_exmpl_element_counts HAS ONLY "H":6 AND elements:_exmpl_element_counts HAS ANY "H":6,"He":7 AND elements:_exmpl_element_counts HAS ONLY "H":6,"He":7`
- OPTIONAL: :filter:`_exmpl_element_counts HAS < 3 AND _exmpl_element_counts HAS ANY > 3, = 6, 4, != 8`
  (note: specifying the = operator after HAS ANY is redundant here, if no operator is given, the test is for equality.)
- OPTIONAL: :filter:`elements:_exmpl_element_counts:_exmpl_element_weights HAS ANY > 3:"He":>55.3 , = 6:>"Ti":<37.6 , 8:<"Ga":0`

Nested property names
~~~~~~~~~~~~~~~~~~~~~

Everywhere in a filter string where a property name is accepted, the API implementation MAY accept nested property names as described in section `Lexical Tokens`_, consisting of identifiers separated by periods ('.').
A filter on a nested property name consisting of two identifiers :filter-fragment:`identifier1.identifier2` matches if either one of these points are true:

- :filter-fragment:`identifier1` references a dictionary-type property that contains as an identifier :filter-fragment:`identifier2` and the filter matches for the content of :filter-fragment:`identifier2`.

- :filter-fragment:`identifier1` references a list of dictionaries that contain as an identifier :filter-fragment:`identifier2` and the filter matches for a flat list containing only the contents of :filter-fragment:`identifier2` for every dictionary in the list.
  E.g., if :filter-fragment:`identifier1` is the list :filter-fragment:`[{"identifier2":42, "identifier3":36}, {"identifier2":96, "identifier3":66}]`, then :filter-fragment:`identifier1.identifier2` is understood in the filter as the list :filter-fragment:`[42, 96]`.

The API implementation MAY allow this notation to generalize to arbitrary depth.
A nested property name that combines more than one list MUST, if accepted, be interpreted as a completely flattened list.

Filtering on relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~

As described in the section `Relationships`_, it is possible for the API implementation to describe relationships between entries of the same, or different, entry types.
The API implementation MAY support queries on relationships with an entry type :filter-fragment:`<entry type>` by using special nested property names:

- :filter-fragment:`<entry type>.id` references a list of IDs of relationships with entries of the type :filter-fragment:`<entry type>`.
- :filter-fragment:`<entry type>.description` references a correlated list of the human-readable descriptions of these relationships.

Hence, the filter language acts as, for every entry type, there is a property with that name which contains a list of dictionaries with two keys, :filter-fragment:`id` and :filter-fragment:`description`.
For example: a client queries the :endpoint:`structures` endpoint with a filter that references :filter-fragment:`calculations.id`.
For a specific structures entry, the nested property behaves as the list :filter-fragment:`["calc-id-43", "calc-id-96"]` and would then, e.g., match the filter :filter:`calculations.id HAS "calc-id-96"`.
This means that the structures entry has a relationship with the calculations entry of that ID.

    **Note**: formulating queries on relationships with entries that have specific property values is a multi-step process.
    For example, to find all structures with bibliographic references where one of the authors has the last name "Schmidt" is performed by the following two steps:

    - Query the :endpoint:`references` endpoint with a filter :filter:`authors.lastname HAS "Schmidt"` and store the :filter-fragment:`id` values of the returned entries.
    - Query the :endpoint:`structures` endpoint with a filter :filter-fragment:`references.id HAS ANY <list-of-IDs>`, where :filter-fragment:`<list-of-IDs>` are the IDs retrieved from the first query separated by commas.

    (Note: the type of query discussed here corresponds to a "join"-type operation in a relational data model.)

Filtering on Properties with an unknown value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Properties can have an unknown value, see section `Properties with an unknown value`_.

Filters that match when the property is known, or unknown, respectively can be constructed using the following syntax::

    identifier IS KNOWN
    identifier IS UNKNOWN

Except for the above constructs, filters that use any form of comparison that involve properties of unknown values MUST NOT match.
Hence, by definition, an :filter-fragment:`identifier` of value :filter-fragment:`null` never matches equality (:filter-op:`=`), inequality (:filter-op:`<`, :filter-op:`<=`, :filter-op:`>`, :filter-op:`>=`, :filter-op:`!=`) or other comparison operators besides :filter:`identifier IS UNKNOWN` and :filter:`NOT identifier IS KNOWN`.
In particular, a filter that compares two properties that are both :val:`null` for equality or inequality does not match.

Examples:

- :filter:`chemical_formula_hill IS KNOWN AND NOT chemical_formula_anonymous IS UNKNOWN`

Precedence
~~~~~~~~~~

The precedence (priority) of the operators MUST be as indicated in the list below:

1. Comparison and keyword operators (:filter-op:`<`, :filter-op:`<=`, :filter-op:`=`, :filter-op:`HAS`, :filter-op:`STARTS`, etc.) -- highest priority;
2. :filter-op:`NOT`
3. :filter-op:`AND`
4. :filter-op:`OR` -- lowest priority.

Examples:

- :filter:`NOT a > b OR c = 100 AND f = "C2 H6"`: this is interpreted as :filter:`(NOT (a > b)) OR ( (c = 100) AND (f = "C2 H6") )` when fully braced.
- :filter:`a >= 0 AND NOT b < c OR c = 0`: this is interpreted as :filter:`((a >= 0) AND (NOT (b < c))) OR (c = 0)` when fully braced.

Type handling and conversions in comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The definitions of specific properties in this standard define their types.
Similarly, for `custom properties`_, the database provider decides their types.
In the syntactic constructs that can accommodate values of more than one type, types of all participating values are REQUIRED to match, with a single exception of timestamps (see below).
Different types of values MUST be reported as :http-error:`501 Not Implemented` errors, meaning that type conversion is not implemented in the specification.

As the filter language syntax does not define a lexical token for timestamps, values of this type are expressed using string tokens in `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__.
In a comparison with a timestamp property, a string token represents a timestamp value that would result from parsing the string according to RFC 3339 Internet Date/Time Format.
Interpretation failures MUST be reported with error :http-error:`400 Bad Request`.

Database and definition providers MAY introduce custom types, representing them with string lexical tokens both in filters and responses.
It is up to the providers to decide which comparison operators to support and how the comparisons should be performed.
For example, if a provider intoduces a set-valued property :property:`_exmpl_set`, it may decide to define operator :val:`CONTAINS` so that :filter:`identifier CONTAINS set` is true if :val:`set` is a subset of a property.

Optional filter features
~~~~~~~~~~~~~~~~~~~~~~~~

Some features of the filtering language are marked OPTIONAL.
An implementation that encounters an OPTIONAL feature that it does not support MUST respond with error ``501 Not Implemented`` with an explanation of which OPTIONAL construct the error refers to.

Property Definitions
====================

An OPTIMADE *Property Definition* defines a specific property, which will be referred to as *the defined property* throughout this section.
The definition uses a dictionary-based construct that, when represented in the JSON output format, is compatible with the JSON Schema standard (for more information, see `Property Definition keys from JSON Schema`_).
The format of Property Definitions defined below allows nesting inner Property Definitions to define properties that are comprised by values organized in lists and dictionaries to arbitrary depth.

To make a property definition expressible in any output format, the fields of the property definition below are specified using OPTIMADE data types.
When a property definition is communicated using a specific data format (e.g., JSON), the property definition is implemented in that data format by mapping the OPTIMADE data types into the corresponding data types for that output format.

Clients are meant to be able to rely on the fact that properties with the same :field:`$id` fields represents equivalently defined properties.
Hence, when a Property Definition that has been published previously is updated, it is of major importance to decide if the updates merely amend, annotate, or clarify the definition in a way that leaves it functionally the same and thus can retain the :field:`$id`, or whether the property is redefined.
An example of an update that does not functionally change the definition is the addition or modification of the examples given in the :field:`examples` field.
If a property is redefined, the redefinition MUST change the :field:`$id`.
The nature of an updated definition can also be reflected in the subfield :field:`version` of :field:`x-optimade-definition`, which allows definitions to be versioned using the `semantic versioning v2 <https://semver.org/spec/v2.0.0.html>`__ standard where the update is categorized on the levels of a patch, minor, or major change.

A Property Definition MUST be composed according to the combination of the requirements in the subsection `Property Definition keys from JSON Schema`_ below and the following additional requirements:

**REQUIRED keys for the outermost level of the Property Definition and OPTIONAL for other levels:**

- :field:`$id`: String, :field:`$schema`: String, :field:`title`: String, and :field:`description`: String.
  See the subsection `Property definition keys from JSON Schema`_ for the definitions of these fields.
  They are defined in that subsection as OPTIONAL on any level of the Property Definition, but are REQUIRED on the outermost level.

.. _definition of the x-optimade-definition field:

- :field:`x-optimade-definition`: Dictionary.
  Additional information about the definition that is not covered by fields in the JSON Schema standard.

  **REQUIRED keys:**

.. _definition of the property-format field:

- :field:`format`: String.
  A string that declares the OPTIMADE definition format the definition adheres to.
  Currently, this is expressed as the minor version of the OPTIMADE specification that describes the property definition format used.
  The string MUST be of the format "MAJOR.MINOR", referring to the version of the OPTIMADE standard that describes the format in which this property definition is expressed.
  The version number string MUST NOT be prefixed by, e.g., "v".
  In implementations of the present version of the standard, the value MUST be exactly :field-val:`1.2`.
  A client MUST disregard the property definition if the field is not a string of the format MAJOR.MINOR or if the MAJOR version number is unrecognized.
  This field allows future versions of this standard to support implementations keeping definitions that adhere to older versions of the property definition format.

- :field:`kind`: String.
  A string specifying what entity is being defined.
  For Property Definitions this MUST be the string "property".

- :field:`name`: String.
  An short identifier (as defined in `Definition of Terms`_) that provides a reasonable short non-unique name for the entity being defined.

- :field:`label`: String.
  An extended identifier (as defined in `Definition of Terms`_) that describes the entity being defined in a way that is unique within a set of definitions provided together.
  The label SHOULD start with the name.

    Implementation notes:

    The name and label fields ensure implementations will be able to give meaningful names to definitions if they are translated into other formats with various requirements on human-readable names, e.g., as `RDF data <https://www.w3.org/TR/rdf-schema/>`__ (see, e.g., rdfs:label).

**OPTIONAL keys:**

- :field:`version`: String.
  This string indicates the version of the definition.
  The string SHOULD be in the format described by the `semantic versioning v2 <https://semver.org/spec/v2.0.0.html>`__ standard.
  When a definition is changed in a way that consitutes a redefinition it SHOULD indicate this by incrementing the MAJOR version number.

- :field:`resources`: List.
  A list of dictionaries that references remote resources that describe the property.
  The format of each dictionary is:

  **REQUIRED keys:**

  - :field:`relation`: String.
    A human-readable description of the relationship between the property and the remote resource, e.g., a "natural language description".

  - :field:`resource-id`: String.
    An IRI of the external resource, which MAY be a resolvable URL.

**REQUIRED keys for all levels of the Property Definition:**

.. _definition of the x-optimade-type field:

- :field:`x-optimade-type`: String.
  Specifies the OPTIMADE data type for this level of the defined property.
  MUST be one of :val:`"string"`, :val:`"integer"`, :val:`"float"`, :val:`"boolean"`, :val:`"timestamp"`, :val:`"list"`, or :val:`"dictionary"`.

- :field:`x-optimade-unit`: String.
  A (compound) symbol for the physical unit in which the value of the defined property is given or one of the strings :val:`dimensionless` or :val:`inapplicable`.
  See subsection `Physical Units in Property Definitions`_ for the details on how compound units are represented in OPTIMADE Property Definitions and the precise format of this string.

**OPTIONAL keys at all nested levels of the Property Definition:**

- :field:`x-optimade-unit-definitions`: List.
  A list of definitions of the symbols used in the Property Definition (including its nested levels) for physical units given as values of the :field:`x-optimade-unit` field.
  This field **MUST be included at the outermost level of a property definition** if the defined property, at any level, includes an :field:`x-optimade-unit` with a value that is not :val:`dimensionless` or :val:`inapplicable`, and it MUST include definitions of all units used on all levels in the property definition.
  The field MAY also occur at deeper nesting levels (but this is not required).
  If it does, the unit definitions provided MUST be redundant with those provided at higher nesting levels.
  See subsection `Physical Units in Property Definitions`_ for the details on how units are represented in OPTIMADE Property Definitions and the precise format of this dictionary.

.. _definition of the x-optimade-dimensions field:

- :field:`x-optimade-dimensions`: Dictionary.
  Specification of the dimensions of one or multi-dimensional data represented as multiple levels of lists.
  Each dimension is given a name and optionally a fixed size.

  **REQUIRED keys:**

  - :field:`names`: List of Strings.
    A list of names of the dimensions of the underlying one or multi-dimensionsional data represented as mutiple levels of lists.
    The order is that the the first name applies to the outermost list, the next name to the lists embedded in that list, etc.

  - :field:`sizes`: List of Integers or :val:`null`.
    A list of fixed length requirements on the underlying one or multi-dimensionsional data represented as mutiple levels of lists.
    The order is that the the first name applies to the outermost list, the next name to the lists embedded in that list, etc.
    The data only validates if the respective level consists of lists of exactly this length.
    A value of :val:`null` allows arbitrary-length lists at the corresponding level.

    Note: OPTIMADE Property Definitions use this field, and MUST NOT use the JSON Schema validating fields minItems and maxItems since that would require reprocessing the schema to handle requests using the OPTIMADE features that requests partial data in lists.
    Instead, the length of lists can be validated against the length information provided in the :field:`sizes` subfield of :field:`x-optimade-dimensions` (which, at this time, can only specify a fixed length requirement.)

- :field:`x-optimade-implementation`: Dictionary.
  A dictionary describing the level of OPTIMADE API functionality provided by the present implementation.
  If an implementation omits this field in its response, a client interacting with that implementation SHOULD NOT make any assumptions about the availability of these features.

  The dictionary has the following format:

  **OPTIONAL keys:**

  - :field:`sortable`: Boolean.
    If :val:`TRUE`, specifies that results can be sorted on this property (see `Entry Listing URL Query Parameters`_ for more information on this field).
    If :val:`FALSE`, specifies that results cannot be sorted on this property.
    Omitting the field is equivalent to :val:`FALSE`.

  - :field:`query-support`: String.
    Defines a required level of support in formulating queries on this field.
    The string MUST be one of the following:

    - :val:`all mandatory`: the defined property MUST be queryable using the OPTIMADE filter language with support for all mandatory filter features.
    - :val:`equality only`: the defined property MUST be queryable using the OPTIMADE filter language equality and inequality operators. Other filter language features do not need to be available.
    - :val:`partial`: the defined property MUST be queryable with support for a subset of the filter language operators as specified by the field :field:`query-support-operators`.
    - :val:`none`: the defined property does not need to be queryable with any features of the filter language.

    Omitting the field or :val:`null` is equivalent to :val:`none`.

  - :field:`query-support-operators`: List of Strings.
    Defines the filter language features supported on this property.
    MUST be present and not :val:`null` if and only if :field:`query-support` is :val:`partial`.

    Each string in the list MUST be one of :val:`<`, :val:`<=`, :val:`>`, :val:`>=`, :val:`=`, :val:`!=`, :val:`CONTAINS`, :val:`STARTS WITH`, :val:`ENDS WITH`, :val:`HAS`, :val:`HAS ALL`, :val:`HAS ANY`, :val:`HAS ONLY`, :val:`IS KNOWN`, :val:`IS UNKNOWN` with the following meanings:

    - :val:`<`, :val:`<=`, :val:`>`, :val:`>=`, :val:`=`, :val:`!=`: indicating support for filtering this property using the respective operator.
      If the property is of Boolean type, support for :val:`=` also designates support for boolean comparisons with the property being true that omit ":filter-fragment:`= TRUE`", e.g., specifying that filtering for ":filter:`is_yellow = TRUE`" is supported also implies support for ":filter:`is_yellow`" (which means the same thing).
      Support for ":filter:`NOT is_yellow`" also follows.

    - :val:`CONTAINS`, :val:`STARTS WITH`, :val:`ENDS WITH`: indicating support for substring filtering of this property using the respective operator. MUST NOT appear if the property is not of type String.

    - :val:`HAS`, :val:`HAS ALL`, :val:`HAS ANY`: indicating support of the MANDATORY features for list property comparison using the respective operator. MUST NOT appear if the property is not of type List.

    - :val:`HAS ONLY`: indicating support for list property comparison with all or a subset of the OPTIONAL constructs using this operator. MUST NOT appear if the property is not of type List.

    - :val:`IS KNOWN`, :val:`IS UNKNOWN`: indicating support for filtering this property on unknown values using the respective operator.

  - :field:`response-default`: Boolean.
    The value :val:`TRUE` means the implementation includes the property in responses by default, i.e., when not specifically requested.
    The value :val:`FALSE` means that the property is only included when requested.
    Omitting the field or :val:`null` means the implementation does not declare if the property will be included in responses by default or not.

- :field:`x-optimade-requirements`: Dictionary.
  A dictionary describing the level of OPTIMADE API functionality required by all implementations of this property.
  Omitting this field means the corresponding functionality is OPTIONAL.
  The dictionary has the same format as :field:`x-optimade-implementation`, *except that* the :field:`response-default` field SHOULD NOT appear, and the following additional OPTIONAL fields are allowed:

  - :field:`support`: String.
    Describes the minimal required level of support for the Property by an implementation.
    This field only has meaning for the defined property when appearing in the :field:`x-optimade-requirements` at the outermost level of the definition.
    Nevertheless, it MAY appear in other places, e.g., if a nested property definition has been inserted that references its own :field:`$id`.
    The string MUST be one of the following:

    - :val:`must`: the defined property MUST be recognized by the implementation (e.g., in filter strings) and MUST NOT be :val:`null`.
    - :val:`should`: the defined property MUST be recognized by the implementation (e.g., in filter strings) and SHOULD NOT be :val:`null`.
    - :val:`may`: it is OPTIONAL for the implementation to recognize the defined property and it MAY be equal to :val:`null`.

    Omitting the field is equivalent to :val:`may`.

    Note: the specification by this field of whether the defined property can be :val:`null` or not MUST match the value of the :field:`type` field.
    If :val:`null` values are allowed, that field must be a list where the string :val:`"null"` is the second element.

  - :field:`response-default-level`: String.
    Expresses if an implementation of this property is required to include or exclude it in responses when not specifically requested.
    This field only has meaning for the defined property when appearing in the :field:`x-optimade-requirements` at the outermost level of the definition.
    Nevertheless, it MAY appear in other places, e.g., if a nested property definition has been inserted that references its own :field:`$id`.

    The string MUST be one of the following:

    - :val:`always`: the defined property MUST always be included in responses and cannot be excluded even by request via, e.g., the :query-param:`response_fields` query parameter.
      This is primarily intended for the :field:`id` and :field:`type` fields, which are required for the JSON:API response format to be valid.
    - :val:`must`: the defined property MUST be included in responses unless specifically excluded.
    - :val:`should`: the defined property SHOULD be included in responses unless specifically excluded.
    - :val:`may`: it is OPTIONAL for the implementation to include the defined property in responses.
    - :val:`should not`: the defined property SHOULD NOT be included in responses unless specifically requested.
    - :val:`must not`: the defined property MUST NOT be included in responses unless specifically requested.

    Omitting the field is equivalent to :val:`may`.

Property Definition keys from JSON Schema
-----------------------------------------

In addition to the requirements on the format of a Property Definition in the previous section, it MUST also adhere to the OPTIONAL and REQUIRED keys described in this subsection.
The format described in this subsection forms a subset of the `JSON Schema Validation Draft 2020-12 <https://json-schema.org/draft/2020-12/json-schema-validation.html>`__ and `JSON Schema Core Draft 2020-12 <https://json-schema.org/draft/2020-12/json-schema-core.html>`__ standards.

**REQUIRED keys**

.. _definition of the type field:

- :field:`type`: List.
  Specifies the corresponding JSON type for this level of the defined property and whether the property can be :val:`null` or not.
  The value is directly correlated with :field:`x-optimade-type` (cf. the `definition of the x-optimade-type field`_).

  It MUST be a list of one or two elements where the first element is a string correlated with :field:`x-optimade-type` as follows; if :field:`x-optimade-type` is:

  * :val:`"boolean"`, :val:`"string"`, or :val:`"integer"` then :field:`type` is the same string.
  * :val:`"dictionary"` then :field:`type` is `"object"`.
  * :val:`"list"` then :field:`type` is `"array"`.
  * :val:`"float"` then :field:`type` is `"number"`.
  * :val:`"timestamp"` then :field:`type` is `"string"`.

  If the second element is included, it MUST be the string :val:`"null"`.
  This two element form specifies that the defined property can be :val:`null`.

  The inclusion or not of :val:`"null"` in the field :field:`type` for a subfield defined at a nested level by a Property Definition declares if that subfield is nullable.
  Property Definitions for which the nullability of a subfield differs MUST NOT share the same :field:`$id`.
  However, the nullability of the subfield SHOULD NOT be taken into account when comparing the nested Property Definition for that subfield with other definitions, i.e., a nullable and non-nullable subfield that are otherwise defined the same SHOULD share the same :field:`$id`.
  Hence, formally OPTIMADE Property Definitions regard nullability of a subfield to belong one level *above* where it appears in the JSON Schema definition.

  **Implementation notes:**

  - The field :field:`type` can be derived from the field :field:`x-optimade-type` and its role is only to provide the JSON type names corresponding to :field:`x-optimade-type`.
    The motivation to include these type names is that it makes the JSON representation of a Property Definition a fully valid standard JSON Schema.
    Nevertheless, for consistency across formats, these JSON type names MUST still be included when a property definition is represented in other output formats (i.e., the JSON names MUST NOT be translated into the type names of that output format).

  - The allowed values of the :field:`type` field are highly restricted compared to what is permitted using the full JSON Schema standard.
    Values can only be defined to be a single OPTIMADE data type or, optionally, :val:`null`.
    This restriction is intended to reduce the complexity of possible data types that implementations have to handle in different formats and database backends.

**Keys that are REQUIRED on the outermost level of a Property Definition, but otherwise OPTIONAL:**

- :field:`$schema`: String.
  A URL for a meta schema that describes the Property Definitions format.
  For Property Definitions adhering to the format described in this document, it should be set to: :val:`https://schemas.optimade.org/meta/v1.2/optimade/property_definition.json`.

.. _definition of the $id field:

- :field:`$id`: String.
  A static IRI identifier that is a URN or URL representing the specific version of this level of the defined property.
  (If it is a URL, clients SHOULD NOT assign any interpretation to the response when resolving that URL.)
  It SHOULD NOT be changed as long as the property definition remains the same, and MUST be changed when the property definition changes.

- :field:`title`: String.
  A short single-line human-readable explanation of the defined property appropriate to show as part of a user interface.

.. _definition of the description field:

- :field:`description`: String.
  A human-readable multi-line description that explains the purpose, requirements, and conventions of the defined property.
  The format SHOULD be a one-line description, followed by a new paragraph (two newlines), followed by a more detailed description of all the requirements and conventions of the defined property.
  Formatting in the text SHOULD use Markdown in the `CommonMark v0.3 format <https://spec.commonmark.org/0.30/>`__ format, with mathematical expressions written to render correctly with the LaTeX mode of `Mathjax 3.2 <https://docs.mathjax.org/en/v3.2-latest/>`__.
  When possible, it is preferable for mathematical expressions to use as straightforward notation as possible to make them readable also when not rendered.

**OPTIONAL keys**

- :field:`$comment`: String.
  A human-readable comment relevant in the context of the raw definition data.
  These comments should normally not be shown to the end users.
  Comments pertaining to the Property Definition that are relevant to end users should go into the field :field:`description`.
  Formatting in the text SHOULD use Markdown using the format described in the `definition of the description field`_.

- :field:`deprecated`: Boolean.
  If :val:`TRUE`, implementations SHOULD not use the defined property, and it MAY be removed in the future.
  If :val:`FALSE`, the defined property is not deprecated.
  The field not being present means :val:`FALSE`.
  A Property Definition marked as deprecated is generally considered to be the same as its non-deprecated counterpart, i.e., it SHOULD retain its :field:`$id`.

- :field:`examples`: List.
  A list of example values that the defined property can have.
  These examples MUST all be of a data type that matches the :field:`type` field and otherwise adhere to the rest of the Property Definition.

- :field:`enum`: List.
  The defined property MUST take one of the values given in the provided list.
  The items in the list MUST all be of a data type that matches the :field:`type` field and otherwise adhere to the rest of the Property Definition.
  If this key is given, for :val:`null` to be a valid value of the defined property, the list MUST contain a :val:`null` value and the :field:`type` MUST be a list where the second value is the string :val:`"null"`.

Furthermore, depending on what string the :field:`type` is equal to, or contains as first element, the following additional requirements also apply:

- :val:`"object"`:

  **REQUIRED**

  - :field:`properties`: Dictionary.
    Gives key-value pairs where each value is an inner Property Definition.
    The defined property is a dictionary that can only contain keys present in this dictionary, and, if so, the corresponding value is described by the respective inner Property Definition.
    (Or, if the :field:`type` field is the list "object" and "null", it can also be :val:`null`.)

  **OPTIONAL**

  - :field:`required`: List.
    The list MUST only contain strings.
    The defined property MUST have keys that match all the strings in this list.
    Other keys present in the :field:`properties` field are OPTIONAL in the defined property.
    If not present or empty, all keys in :field:`properties` are regarded as OPTIONAL.

  - :field:`maxProperties`: Integer.
    The defined property is a dictionary where the number of keys MUST be less than or equal to the number given.

  - :field:`minProperties`: Integer.
    The defined property is a dictionary where the number of keys MUST be greater than or equal to the number given.

  - :field:`dependentRequired`: Dictionary.
    The dictionary keys are strings and the values are lists of unique strings.
    If the defined property has a key that is equal to a key in the given dictionary, the defined property MUST also have keys that match each of the corresponding values.
    No restriction is inferred from this field for keys in the defined property that do not match any key in the given dictionary.

- :val:`"array"`:

  **REQUIRED**

  - :field:`items`: Dictionary.
    Specifies an inner Property Definition.
    The defined property is a list where each item MUST match this inner Property Definition.

  **OPTIONAL**

  - :field:`uniqueItems`: Boolean.
    If :val:`TRUE`, the defined property is an array that MUST only contain unique items.
    If :val:`FALSE`, this field sets no limitation on the defined property.

  Furthermore, despite being defined in the JSON Schema standard, the fields :field:`minItems` and :field:`maxItems` MUST NOT be used to indicate limits of the number of items of a list.
  See the `definition of the x-optimade-dimensions field`_ for more information.

- :val:`"integer"`:

  **OPTIONAL**

  - :field:`multipleOf`: Integer.
    An integer is strictly greater than 0.
    The defined property MUST have an integer value that when divided by the given integer results in an integer (i.e., it must be even divisible by this integer without a fractional part).

  - :field:`maximum`: Integer.
    The defined property is an integer that MUST be less than or equal to this number.

  - :field:`exclusiveMaximum`: Integer.
    The defined property is an integer that MUST be strictly less than this number; it cannot be equal to the number.

  - :field:`minimum`: Integer.
    The defined property is an integer that MUST be greater than or equal to this number.

  - :field:`exclusiveMinimum`: Integer.
    The defined property is an integer that MUST be strictly greater than this number; it cannot be equal to the number.

- :val:`"number"`:

  **OPTIONAL**

  - :field:`multipleOf`: Float.
    An integer is strictly greater than 0.
    The defined property MUST have an integer value that when divided by the given integer results in an integer (i.e., it must be even divisible by this integer without a fractional part).

  - :field:`maximum`: Float.
    The defined property is a float that MUST be less than or equal to this number.

  - :field:`exclusiveMaximum`: Float.
    The defined property is a float that MUST be strictly less than this number; it cannot be equal to the number.

  - :field:`minimum`: Float.
    The defined property is a float that MUST be greater than or equal to this number.

  - :field:`exclusiveMinimum`: Float.
    The defined property is a float that MUST be strictly greater than this number; it cannot be equal to the number.

- :val:`"string"`:

  **OPTIONAL**

  - :field:`maxLength`: Integer.
    A non-negative integer.
    The defined property is a string that MUST have a length that is less than or equal to the given integer.
    (The length of the string is the number of individual Unicode characters it is composed of.)

  - :field:`minLength`: Integer.
    A non-negative integer.
    The defined property is a string that MUST have a length that is less than or equal to the given integer.
    (The definition of the length of a string is the same as in the field :field:`maxLength`.)

  - :field:`format`: String.
    Choose one of the following values to indicate that the defined property is a string that MUST adhere to the specified format:

    - :val:`"date-time"`: the date-time production in :RFC:`3339` section 5.6.
    - :val:`"date"`: the full-date production in :RFC:`3339` section 5.6.
    - :val:`"time"`: the full-time production in :RFC:`3339` section 5.6.
    - :val:`"duration"`: the duration production in :RFC:`3339` Appendix A.
    - :val:`"email"`: the "Mailbox" ABNF rule in :RFC:`5321` section 4.1.2.
    - :val:`"uri"`: a string instance is valid against this attribute if it is a valid URI according to :RFC:`3986`.
    - :val:`"iri"`: a string instance is valid against this attribute if it is a valid IRI according to :RFC:`3987`.

  - :field:`pattern`: String.
    This string SHOULD be a valid regular expression, according to the ECMA-262 regular expression dialect.
    A string instance is considered valid if the regular expression matches the instance successfully.
    The regular expression is not implicitly anchored, i.e., it can match the string at any position unless the expression contains a leading '^' or a trailing '$'.

A complete example of a Property Definition is found in the appendix `Property Definition Example`_.

Physical Units in Property Definitions
--------------------------------------

In OPTIMADE, there is no facility to allow a property to be represented in a choice of units, e.g., either ångström (Å) or meter (m).
The unit is always permanently fixed by the Property Definition.
Clients and servers that use other units internally thus have to do unit conversions as part of preparing and processing OPTIMADE responses.

The physical unit of a property, the embedded items of a list, or values of a dictionary, are defined with the field :field:`x-optimade-unit` with the following requirements:

- The field MUST be given with a non-:val:`null` value both at the highest level in the OPTIMADE Property Definition and all inner Property Definitions.
- If the property refers to a physical quantity that is dimensionless and unitless (often also referred to as having the dimension 1) or refers to a dimensionless and unitless count of something (e.g., the number of protons in a nucleus) the field MUST have the value :val:`dimensionless`.
  However, quantities that use counting units, e.g., the mole, or quantities that use dimensionless units, e.g., the radian MUST NOT set the field to :val:`dimensionless`.
- If the property refers to an entity for which the assignment of a unit would not make sense, e.g., a string representing a chemical formula or a serial number the field MUST have the value :val:`inapplicable`.
- If the field does not take the value :val:`dimensionless` or :val:`inapplicable`, it MUST be set to a single unit symbol or a Compound Unit Expressions from a set of unit symbols using the format described in `Compound Unit Expressions`_.
- All unit symbols used in :field:`x-optimade-unit` fields at any level in a Property Definition MUST be defined in the :field:`units` field inside the :field:`x-optimade-property` field in the outermost level of the Property Definition, or in the :field:`units` field in the Entry info endpoint (the latter is only possible for Property Definitions embedded in such a response).
- The :field:`units` MUST be a list of dictionaries using the format for OPTIMADE Physical Unit Definitions described in `Physical Unit Definitions`_.

Compound Unit Expressions
-------------------------

A Compound Unit Expression is formed by a sequence of symbols for units or constants separated by a single multiplication ``*`` character.
Each symbol can also be suffixed by a single ``^`` character followed by a positive or negative integer to indicate the power of the preceding symbol, e.g., ``m^3`` for cubic meter, ``m^-3`` for inverse cubic meter.
(Positive integers MUST NOT be preceded by a plus sign.)
Each unit or constant symbol MAY be directly prefixed by a prefix symbol.
A prefix symbol MUST be directly followed by a unit symbol, i.e., it MUST NOT be used on its own, and MUST NOT be followed by ``^`` to indicate a power.
When defining prefix symbols it is important to ensure that they do not introduce ambiguity.
If there are ambiguous interpretations of a symbol as either having or not having a prefix, it MUST be interpreted as a unit without a prefix.

Furthermore:

- No whitespace, parentheses, or other symbols than specified above are permitted.
- The (prefixed) unit and constant symbols MUST appear in alphabetical order.

Physical Unit Definitions
-------------------------

An OPTIMADE Physical Unit Definition is a dictionary adhering to the following format:

**REQUIRED keys:**

- :field:`$schema`: String.
  A URL for a meta schema that describes the Physical Unit Definitions format.
  For Property Definitions adhering to the format described in this document, it should be set to: :val:`https://schemas.optimade.org/meta/v1.2/optimade/physical_unit_definition.json`.

- :field:`x-optimade-definition`: Dictionary.
  The same field as defined in the `definition of the x-optimade-definition field`_ for Property Definitions but where the :field:`kind` subfield MUST be :val:`unit`.

.. _definition of the $id field in Physical Unit Definitions:

- :field:`$id`: String.
  A static IRI identifier that is a URN or URL representing the specific version of the Physical Unit Definition.
  (If it is a URL, clients SHOULD NOT assign any interpretation to the response when resolving that URL.)
  It SHOULD NOT be changed as long as the Physical Unit Definition remains the same, and SHOULD be changed when the definition changes.
  Physical Unit Definitions SHOULD be regarded as the same if they only differ by:

  - Additions of annotating notes to end of the :field:`description` field.
  - Changes to the following specific fields at any level: :field:`deprecated` and :field:`$comment`.

- :field:`symbol`: String.
  Specifies the symbol to be used in :field:`x-optimade-unit` to reference this unit.

- :field:`title`: String.
  A human-readable single-line string name for the unit.

- :field:`description`: String.
  A human-readable multiple-line detailed description of the unit.

  Additions appended to the end of the :field:`description` field that are clearly marked as notes that clarify the definition without changing it are viewed as annotations to the Physical Unit Definition rather than an integral part of it.
  Such annotations SHOULD only be added to the end of an otherwise unmodified :field:`description` and MUST NOT change the meaning or interpretation of the text above them.
  The purpose is to provide a way to add explanations and clarifications to a definition without having to regard it as a new definition.
  For example, these annotations to the description MAY be used to explain why a definition has been deprecated.

**OPTIONAL keys:**

- :field:`standard`: Dictionary.
  This field is used to express that the unit is part of a preexisting standard.
  The dictionary has the following format:

  **REQUIRED keys:**

  - :field:`name`: String.
    The abbreviated name of the standard being referenced.
    One of the following:

    - :val:`"si"`: the symbol is defined as part of the SI standard of unit symbols and prefixes.
    - :val:`"codata"`: the symbol is defined as part of one of the CODATA series of publications.
    - :val:`"iso-iec-80000"`: the symbol is defined in the iso-iec-80000 standard.
    - :val:`"gnu units"`: the symbol is a (compound) unit expression based on the symbols in the file ``definitions.units`` distributed with `GNU Units software <https://www.gnu.org/software/units/>`__.

      A standard set of symbols for units and prefixes for OPTIMADE is taken from version 3.15 of the (separately versioned) unit database ``definitions.units`` included with the `source distribution <http://ftp.gnu.org/gnu/units/>`__ of `GNU Units <https://www.gnu.org/software/units/>`__ version 2.22.
      A prefix is indicated in the file by a trailing ``-``, but that trailing character MUST NOT be included when using it as a prefix.
      If the unit is available in this database, or if it can be expressed as a Compound Unit Expression using these units and prefixes, the value of :field:`x-optimade-unit` SHOULD use the (compound) string symbol.
      If there are multiple prefixes in the file with the same meaning, an implementation SHOULD use the *shortest one* consisting of only lowercase letters a-z and underscores, but no other symbols.
      If there are multiple ones with the same shortest length, then the first one of those SHOULD be used.
      For example, the GNU Units database defines the symbol :val:`"km"` for kilometers by a combination of the ``k-`` SI kilo prefix and the ``m`` symbol for the SI meter unit.

    - :val:`"ucum"`: the symbol is defined in `The Unified Code for Units of Measure <https://unitsofmeasure.org/ucum.html>`__ (UCUM) standard.
    - :val:`"qudt"`: the symbol is defined in the `QUDT <http://qudt.org/>`__ standard.
      Not only symbols strictly defined within the standard are allowed, but also other compound unit expressions created according to the scheme for how new such symbols are formed in this standard.

  - :field:`symbol`: String.
    The symbol to use from the referenced standard, expressed according to that standard.
    The field MAY use mathematical expressions written the same way as described in the `definition of the description field`_.
    This field MAY be different from the symbol being defined via the definition if the unit will be referenced in :field:`x-optimade-unit` field using a different symbol than the one used in the standard or if the symbol is expressed in the standard in a way that requires mathematical notation.
    However, if possible, the :field:`symbol` field SHOULD be the same.

  **OPTIONAL keys:**

  - :field:`version`: String.
    The version string of the referenced standard.

  - :field:`year`: Integer.
    The year that the standard adopted the definition.

  - :field:`category`
    The category of the definition in case the standard uses categories to organize definitions.

- :field:`alternate-symbols`: List of String.
  A list of other symbols that are commonly associated with the unit.
  The stings MAY use mathematical expressions written the same way as described in the `definition of the description field`_.

- :field:`property-format`: String.
  Specifies the minor version of the Property Definitions format that the Physical Units Definition is expressed in.
  (The Physical Units Definition format is not versioned independently.)
  The format is the same as described above for the `definition of the property-format field`_ in Property Definitions.
  This field MUST be included when Physical Unit Definitions are used standalone, i.e., when they are not embedded inside a Property Definition that already declares a :field:`property-format` at the top level.

- :field:`version`: String.
  This string indicates the version of the Physical Unit Definition.
  The string SHOULD be in the format described by the `semantic versioning v2 <https://semver.org/spec/v2.0.0.html>`__ standard.

- :field:`resources`: List of Dictionaries.
  A list of dictionaries that reference remote resources that describe the unit.
  The format of each dictionary is:

  **REQUIRED keys:**

  - :field:`relation`: String.
    A human-readable description of the relationship between the unit and the remote resource, e.g., a "natural language description".

  - :field:`resource-id`: String.
    An IRI of the external resource (which MAY be a resolvable URL).

.. _definition of defining-relation:

- :field:`defining-relation`: Dictionary.
  A dictionary that encodes a defining relation to another unit or set of units, with the primary intended use of relating a unit to its definition in SI units, if such a relationship exists.
  Some units, e.g., the atomic mass unit (also known as dalton, commonly denoted ``u``), only has an approximate relationship to SI units, in which case the :field:`defining-relation` MUST be omitted or :val:`null`.
  The dictionary MUST adhere to the following format:

  **OPTIONAL keys:**

  - :field:`base-units`: List of Dictionaries.
    A list specifying the base IRIs and unit symbols for the units in which the dimensional formula for the defining relation is expressed.
    Each item MUST be a dictionary that adheres to the following format:

    **REQUIRED keys:**

    - :field:`symbol`: String.
      The symbol used to reference this unit in the dimensional formula.

    - :field:`id`: String.
      The IRI of one of the units referenced in the dimensional formula for the defining relation.

  - :field:`base-units-expression`: String.
    A string expressing the base units part of the defining relation for the unit being defined.
    It MUST adhere to the format for compound unit expression described in `Physical Units in Property Definitions`_.
    If the field is missing or :val:`null` the base-units-expression is taken to be equal to 1, i.e., the defining relation is dimensionless.

  - :field:`scale`: Dictionary.
    A dictionary specifying the scale in the defining relation, adhering to the following format:

    **OPTIONAL keys:**

    - :field:`numerator`: Integer.
    - :field:`denominator`: Integer.
    - :field:`base`: Integer.
    - :field:`exponent`: Integer.

    These four fields specify the value as the rational number :field:`numerator` / :field:`denominator`, multiplied by :field:`base` to the power of :field:`exponent`.
    If omitted or :val:`null`, the defaults for the :field:`numerator`, :field:`denominator`, :field:`base`, and :field:`exponent` are respectively 1, 1, 10, and 0.

    - :field:`standard_uncertainty`: Float.
      The standard uncertainty of the value used in the defining relation.
      Some definitions define an entity (e.g. a constant) to a specific value along with an uncertainty of that value.

  - :field:`offset`: Dictionary.
    A dictionary specifying the offset value, adhering to the same format as :field:`scale`.
    If omitted or :val:`null`, the defaults for the :field:`numerator`, :field:`denominator`, and :field:`exponent` are respectively 0, 1, and 0.

  If the fields in :field:`scale` are designated as ``sn``, ``sd``, and ``se``; and the fields in :field:`offset` are designated as ``on``, ``od``, and ``oe``; and :field:`base-units-expression` is designated as ``b``, these fields state the following defining relation: a value ``v`` multiplied by the unit being defined is equal to the following expression ``(v * (sn/sd) * 10**se + (on/od) * 10**oe)*b``, where ``*`` designates multiplication and ``**`` designates exponentiation.
  For example, the defining relation of the temperature unit Fahrenheit ``F`` in Celsius ``C``, that says that ``x F = (x - 32) * (5/9) C = 5/9 x + (-160/9) C`` could be expressed as follows:

  .. code:: jsonc

    "defining-relation": {
      "base-units": [
        {
          "symbol": "C",
          "id": "https://units.example.com/celsius"
        }
      ],
      "base-units-expression": "C",
      "scale": {
        "numerator": 5,
        "denominator": 9
      },
      "offset": {
        "numerator": -160,
        "denominator": 9
      }
    }

- :field:`approximate-relations`: List of Dictionary.
  A list of dictionaries that encode approximate relations to another unit or set of units.
  The intended use is to express one or a few approximate relationships from the unit being defined to other unit systems (primarily intended to be SI).
  This field is useful for units not defined by such a relationship, in which case the :field:`defining-relation` field would be used.
  For example, the atomic mass unit (also known as dalton, commonly denoted ``u``) is defined as one twelfth of the mass of a free carbon-12 atom at rest and only has an approximate relationship to the SI kilogram.
  While this field allows expressing multiple relationships, the intent is only to provide the most relevant relationships (e.g., to an SI base unit) from which other relationships can be derived.

  Each element in the list MUST be a dictionary adhering to the following format:

  **OPTIONAL keys:**

  - :field:`base-units`: List of Dictionaries, and :field:`base-units-expression`: String.
    These fields take the same format and roles as in the `definition of defining-relation`_

  - :field:`scale`: Dictionary.
    A dictionary specifying the scale in the approximate relation.
    It MUST adhere to the following format:

    **REQUIRED keys:**

    - :field:`value`: Float.
      The value of the scale in the approximate relation.

    **OPTIONAL keys:**

    - :field:`standard_uncertainty`: Float.
      The standard uncertainty of the value in the approximate relation.

    - :field:`relative_standard_uncertainty`: Float.
      The relative standard uncertainty of the value in the approximate relation.

  - :field:`offset`: Dictionary.
    A dictionary specifying the offset in the approximate relation.
    It MUST adhere to the same format as the :field:`scale` field above.

  The values for :field:`scale` and :field:`offset` take the same meaning as in the `definition of defining-relation`_ to express a relationship between the unit being defined and the compound unit expression in :field:`base-units-expression`.

- :field:`deprecated`: Boolean.
  If :val:`TRUE`, implementations SHOULD not use the unit defined in this Physical Unit Definition.
  If :val:`FALSE`, the unit defined in this Physical Unit Definition is not deprecated.
  The field not being present means :val:`FALSE`.

- :field:`$comment`: String.
  A human-readable comment relevant in the context of the raw definition data.
  These comments should normally not be shown to the end users.
  Comments pertaining to the Property Definition that are relevant to end users should go into the field :field:`description`.
  Formatting in the text SHOULD use Markdown using the format described in the `definition of the description field`_ of Property Definitions.

An example of a Physical Unit Definition, including a defining relation that involves more than one other unit, is embedded in the example of a Property Definition in the appendix `Property Definition Example`_.

Prefixes and constants
----------------------

Prefixes and constants are defined in OPTIMADE using nearly identical schemas as the one for units in `Physical Unit Definitions`_.
The only difference is that for prefixes:

- The :field:`$schema` SHOULD be set to: "https://schemas.optimade.org/meta/v1.2/optimade/prefix_definition.json".

- The subfield :field:`kind` of the field :field:`x-optimade-definition` MUST be :val:`prefix`.

And for Constants:

- The :field:`$schema` SHOULD be set to: "https://schemas.optimade.org/meta/v1.2/optimade/constant_definition.json".

- The subfield :field:`kind` of the field :field:`x-optimade-definition` MUST be :val:`constant`.

Unrecognized keys in property definitions
-----------------------------------------

Implementations MAY add their own keys in Property Definitions, both inside and outside of the fields :field:`x-optimade-property`, :field:`x-optimade-implementation`, and :field:`x-optimade-requirements` in the form of :field:`x-exmpl-name` where :field:`exmpl` is the database-specific prefix (without underscore characters) and :field:`name` is the part of the key chosen by the implementation.
Implementations MUST NOT add keys to property definitions on other formats.

Client and server implementations that interpret an OPTIMADE Property Definition and encounter unrecognized keys starting with :field:`x-exmpl-` where :field:`exmpl` is a recognized database prefix MAY issue errors or warnings.
Other unrecognized keys starting with :field:`x-` MUST NOT issue errors, SHOULD NOT issue warnings, and MUST otherwise be ignored.

To allow forward compatibility with future versions of both OPTIMADE and the JSON Schema standards, unrecognized keys that do not start with :field:`x-` SHOULD issue a warning but MUST otherwise be ignored.

Entry List
==========

This section defines standard entry types and their properties.

Properties Used by Multiple Entry Types
---------------------------------------

id
~~

- **Description**: An entry's ID as defined in section `Definition of Terms`_.
- **Type**: string.
- **Requirements/Conventions**:

  - **Support**: MUST be supported by all implementations, MUST NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - **Response**: REQUIRED in the response.
  - See section `Definition of Terms`_.

- **Examples**:

  - :val:`"db/1234567"`
  - :val:`"cod/2000000"`
  - :val:`"cod/2000000@1234567"`
  - :val:`"nomad/L1234567890"`
  - :val:`"42"`

type
~~~~

- **Description**: The name of the type of an entry.
- **Type**: string.
- **Requirements/Conventions**:

  - **Support**: MUST be supported by all implementations, MUST NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - **Response**: REQUIRED in the response.
  - MUST be an existing entry type.
  - The entry of type ``<type>`` and ID ``<id>`` MUST be returned in response to a request for :endpoint:`/<type>/<id>` under the versioned or unversioned base URL serving the API.

- **Examples**:

  - :val:`"structures"`

immutable\_id
~~~~~~~~~~~~~

- **Description**: The entry's immutable ID (e.g., a UUID). This is important for databases having preferred IDs that point to "the latest version" of a record, but still offer access to older variants. This ID maps to the version-specific record, in case it changes in the future.
- **Type**: string.
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.

- **Examples**:

  - :val:`"8bd3e750-b477-41a0-9b11-3a799f21b44f"`
  - :val:`"fjeiwoj,54;@=%<>#32"` (Strings that are not URL-safe are allowed.)

last\_modified
~~~~~~~~~~~~~~

- **Description**: Date and time representing when the entry was last modified.
- **Type**: timestamp.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - **Response**: REQUIRED in the response unless the query parameter :query-param:`response_fields` is present and does not include this property.

- **Examples**:

  - As part of JSON response format: :VAL:`"2007-04-05T14:30:20Z"` (i.e., encoded as an `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__ string.)

Custom properties
~~~~~~~~~~~~~~~~~

- **Description**: Providers are able to add database-provider-specific and definition-provider-specific properties in the output of both standard entry types and custom entry types.
  Similarly, an implementation MAY add keys with a namespace prefix to dictionary properties and their sub-dictionaries.
  For example, the database-provider-specific property :property:`_exmpl_oxidation_state`, can be placed within the OPTIMADE property :property:`species`.

- **Type**: Decided by the API implementation.
  MUST be one of the OPTIMADE `Data types`_.
- **Requirements/Conventions**:

  - **Support**: Support for database-provider-specific properties is fully OPTIONAL.
  - **Query**: Support for queries on these properties are OPTIONAL.
    If supported, only a subset of the filter features MAY be supported.
  - **Response**: API implementations are free to choose whether database-provider-specific properties are only included when requested using the query parameter :query-param:`response_fields`, or if they are included also when :query-param:`response_fields` is not present.
    Implementations are thus allowed to decide that some of these properties are part of what can be seen as the default value of :query-param:`response_fields` when that query parameter is omitted.
    Implementations SHOULD NOT include database-provider-specific properties when the query parameter :query-param:`response_fields` is present but does not list them.
  - These MUST be prefixed by a database-provider-specific prefix (see appendix `Namespace Prefixes`_).
  - Implementations MUST add the properties to the list of :property:`properties` under the respective entry listing :endpoint:`info` endpoint (see `Entry Listing Info Endpoints`_).

- **Examples**: A few examples of valid database-provided-specific property names, for a predefined prefix ``_exmpl``, are as follows:

  - :property:`_exmpl_formula_sum`
  - :property:`_exmpl_band_gap`
  - :property:`_exmpl_supercell`
  - :property:`_exmpl_trajectory`
  - :property:`_exmpl_workflow_id`

Structures Entries
------------------

:entry:`structures` entries (or objects) have the properties described above in section `Properties Used by Multiple Entry Types`_, as well as the following properties:

elements
~~~~~~~~

- **Description**: The chemical symbols of the different elements present in the structure.
- **Type**: list of strings.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - The strings are the chemical symbols, i.e., either a single uppercase letter or an uppercase letter followed by a number of lowercase letters.
  - The order MUST be alphabetical.
  - MUST refer to the same elements in the same order, and therefore be of the same length, as `elements_ratios`_, if the latter is provided.
  - Note: This property SHOULD NOT contain the string "X" to indicate non-chemical elements or "vacancy" to indicate vacancies (in contrast to the field :field:`chemical_symbols` for the :property:`species` property).

- **Examples**:

  - :val:`["Si"]`
  - :val:`["Al","O","Si"]`

- **Query examples**:

  - A filter that matches all records of structures that contain Si, Al **and** O, and possibly other elements: :filter:`elements HAS ALL "Si", "Al", "O"`.
  - To match structures with exactly these three elements, use :filter:`elements HAS ALL "Si", "Al", "O" AND elements LENGTH 3`.
  - Note: length queries on this property can be equivalently formulated by filtering on the `nelements`_ property directly.

nelements
~~~~~~~~~

- **Description**: Number of different elements in the structure as an integer.
- **Type**: integer
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - MUST be equal to the lengths of the list properties `elements`_ and `elements_ratios`_, if they are provided.

- **Examples**:

  - :val:`3`

- **Querying**:

  -  Note: queries on this property can equivalently be formulated using :filter-fragment:`elements LENGTH`.
  -  A filter that matches structures that have exactly 4 elements: :filter:`nelements=4`.
  -  A filter that matches structures that have between 2 and 7 elements: :filter:`nelements>=2 AND nelements<=7`.

elements\_ratios
~~~~~~~~~~~~~~~~

- **Description**: Relative proportions of different elements in the structure.
- **Type**: list of floats
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - Composed by the proportions of elements in the structure as a list of floating point numbers.
  - The sum of the numbers MUST be 1.0 (within floating point accuracy)
  - MUST refer to the same elements in the same order, and therefore be of the same length, as `elements`_, if the latter is provided.

- **Examples**:

  - :val:`[1.0]`
  - :val:`[0.3333333333333333, 0.2222222222222222, 0.4444444444444444]`

- **Query examples**:

  - Note: Useful filters can be formulated using the set operator syntax for correlated values.
    However, since the values are floating point values, the use of equality comparisons is generally inadvisable.
  - OPTIONAL: a filter that matches structures where approximately 1/3 of the atoms in the structure are the element Al is: :filter:`elements:elements_ratios HAS ALL "Al":>0.3333, "Al":<0.3334`.

chemical\_formula\_descriptive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: The chemical formula for a structure as a string in a form chosen by the API implementation.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - The chemical formula is given as a string consisting of properly capitalized element symbols followed by integers or decimal numbers, balanced parentheses, square, and curly brackets ``(``,\ ``)``, ``[``,\ ``]``, ``{``, ``}``, commas, the ``+``, ``-``, ``:`` and ``=`` symbols.
    The parentheses are allowed to be followed by a number.
    Spaces are allowed anywhere except within chemical symbols.
    The order of elements and any groupings indicated by parentheses or brackets are chosen freely by the API implementation.
  - The string SHOULD be arithmetically consistent with the element ratios in the :property:`chemical_formula_reduced` property.
  - It is RECOMMENDED, but not mandatory, that symbols, parentheses and brackets, if used, are used with the meanings prescribed by `IUPAC's Nomenclature of Organic Chemistry <https://www.qmul.ac.uk/sbcs/iupac/bibliog/blue.html>`__.

- **Examples**:

  - :val:`"(H2O)2 Na"`
  - :val:`"NaCl"`
  - :val:`"CaCO3"`
  - :val:`"CCaO3"`
  - :val:`"(CH3)3N+ - [CH2]2-OH = Me3N+ - CH2 - CH2OH"`

- **Query examples**:

  - Note: the free-form nature of this property is likely to make queries on it across different databases inconsistent.
  - A filter that matches an exactly given formula: :filter:`chemical_formula_descriptive="(H2O)2 Na"`.
  - A filter that does a partial match: :filter:`chemical_formula_descriptive CONTAINS "H2O"`.

chemical\_formula\_reduced
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: The reduced chemical formula for a structure as a string with element symbols and integer chemical proportion numbers.
  The proportion number MUST be omitted if it is 1.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property.
    However, support for filters using partial string matching with this property is OPTIONAL (i.e., BEGINS WITH, ENDS WITH, and CONTAINS).
    Intricate queries on formula components are instead suggested to be formulated using set-type filter operators on the multi valued :property:`elements` and :property:`elements_ratios` properties.
  - Element symbols MUST have proper capitalization (e.g., :val:`"Si"`, not :VAL:`"SI"` for "silicon").
  - Elements MUST be placed in alphabetical order, followed by their integer chemical proportion number.
  - For structures with no partial occupation, the chemical proportion numbers are the smallest integers for which the chemical proportion is exactly correct.
  - For structures with partial occupation, the chemical proportion numbers are integers that within reasonable approximation indicate the correct chemical proportions. The precise details of how to perform the rounding is chosen by the API implementation.
  - No spaces or separators are allowed.

- **Examples**:

  - :val:`"H2NaO"`
  - :val:`"ClNa"`
  - :val:`"CCaO3"`

- **Query examples**:

  - A filter that matches an exactly given formula is :filter:`chemical_formula_reduced="H2NaO"`.

chemical\_formula\_hill
~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: The chemical formula for a structure in `Hill form <https://dx.doi.org/10.1021/ja02046a005>`__ with element symbols followed by integer chemical proportion numbers.
  The proportion number MUST be omitted if it is 1.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, only a subset of the filter features MAY be supported.
  - The overall scale factor of the chemical proportions is chosen such that the resulting values are integers that indicate the most chemically relevant unit of which the system is composed.
    For example, if the structure is a repeating unit cell with four hydrogens and four oxygens that represents two hydroperoxide molecules, :property:`chemical_formula_hill` is :val:`"H2O2"` (i.e., not :val:`"HO"`, nor :val:`"H4O4"`).
  - If the chemical insight needed to ascribe a Hill formula to the system is not present, the property MUST be handled as unset.
  - Element symbols MUST have proper capitalization (e.g., :val:`"Si"`, not :VAL:`"SI"` for "silicon").
  - Elements MUST be placed in `Hill order <https://dx.doi.org/10.1021/ja02046a005>`__, followed by their integer chemical proportion number.
    Hill order means: if carbon is present, it is placed first, and if also present, hydrogen is placed second.
    After that, all other elements are ordered alphabetically.
    If carbon is not present, all elements are ordered alphabetically.
  - If the system has sites with partial occupation and the total occupations of each element do not all sum up to integers, then the Hill formula SHOULD be handled as unset.
  - No spaces or separators are allowed.

- **Examples**:

  - :val:`"H2O2"`

- **Query examples**:

  - A filter that matches an exactly given formula is :filter:`chemical_formula_hill="H2O2"`.

chemical\_formula\_anonymous
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: The anonymous formula is the :property:`chemical_formula_reduced`, but where the elements are instead first ordered by their chemical proportion number, and then, in order left to right, replaced by anonymous symbols A, B, C, ..., Z, Aa, Ba, ..., Za, Ab, Bb, ... and so on.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property.
    However, support for filters using partial string matching with this property is OPTIONAL (i.e., BEGINS WITH, ENDS WITH, and CONTAINS).

- **Examples**:

  - :val:`"A2B"`
  - :val:`"A42B42C16D12E10F9G5"`

- **Querying**:

  - A filter that matches an exactly given formula is :filter:`chemical_formula_anonymous="A2B"`.

dimension\_types
~~~~~~~~~~~~~~~~

- **Description**: List of three integers describing the periodicity of the boundaries of the unit cell.
  For each direction indicated by the three `lattice_vectors`_, this list indicates if the direction is periodic (value :val:`1`) or non-periodic (value :val:`0`).
  Note: the elements in this list each refer to the direction of the corresponding entry in `lattice_vectors`_ and *not* the Cartesian x, y, z directions.
- **Type**: list of integers.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - MUST be a list of length 3.
  - Each integer element MUST assume only the value 0 or 1.

- **Examples**:

  - A nonperiodic structure, for example, for a single molecule: :val:`[0, 0, 0]`
  - A unit cell that is periodic in the direction of the third lattice vector, for example for a carbon nanotube: :val:`[0, 0, 1]`
  - For a 2D surface/slab, with a unit cell that is periodic in the direction of the first and third lattice vectors: :val:`[1, 0, 1]`
  - For a bulk 3D system with a unit cell that is periodic in all directions: :val:`[1, 1, 1]`

nperiodic\_dimensions
~~~~~~~~~~~~~~~~~~~~~

- **Description**: An integer specifying the number of periodic dimensions in the structure, equivalent to the number of non-zero entries in `dimension_types`_.
- **Type**: integer
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - The integer value MUST be between 0 and 3 inclusive and MUST be equal to the sum of the items in the `dimension_types`_ property.
  - This property only reflects the treatment of the lattice vectors provided for the structure, and not any physical interpretation of the dimensionality of its contents.

- **Examples**:

  - :val:`2` should be indicated in cases where :property:`dimension_types` is any of :val:`[1, 1, 0]`, :val:`[1, 0, 1]`, :val:`[0, 1, 1]`.

- **Query examples**:

  - Match only structures with exactly 3 periodic dimensions: :filter:`nperiodic_dimensions=3`
  - Match all structures with 2 or fewer periodic dimensions: :filter:`nperiodic_dimensions<=2`

lattice\_vectors
~~~~~~~~~~~~~~~~

- **Description**: The three lattice vectors in Cartesian coordinates, in ångström (Å).
- **Type**: list of list of floats or unknown values.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - MUST be a list of three vectors *a*, *b*, and *c*, where each of the vectors MUST BE a list of the vector's coordinates along the x, y, and z Cartesian coordinates.
    (Therefore, the first index runs over the three lattice vectors and the second index runs over the x, y, z Cartesian coordinates).
  - For databases that do not define an absolute Cartesian system (e.g., only defining the length and angles between vectors), the first lattice vector SHOULD be set along *x* and the second on the *xy*-plane.
  - MUST always contain three vectors of three coordinates each, independently of the elements of property `dimension_types`_.
    The vectors SHOULD by convention be chosen so the determinant of the :property:`lattice_vectors` matrix is different from zero.
    The vectors in the non-periodic directions have no significance beyond fulfilling these requirements.
  - The coordinates of the lattice vectors of non-periodic dimensions (i.e., those dimensions for which `dimension_types`_ is :val:`0`) MAY be given as a list of all :val:`null` values.
    If a lattice vector contains the value :val:`null`, all coordinates of that lattice vector MUST be :val:`null`.

- **Examples**:

  - :val:`[[4.0,0.0,0.0],[0.0,4.0,0.0],[0.0,1.0,4.0]]` represents a cell, where the first vector is :val:`(4, 0, 0)`, i.e., a vector aligned along the :val:`x` axis of length 4 Å; the second vector is :val:`(0, 4, 0)`; and the third vector is :val:`(0, 1, 4)`.

space\_group\_symmetry\_operations\_xyz
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: a list of symmetry operations given as general position x, y and z coordinates in algebraic form.

- **Type** list of strings
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.

    - The property is RECOMMENDED if coordinates are returned in a form to which these operations can or must be applied (e.g. fractional atom coordinates of an asymmetric unit).
    - The property is REQUIRED if symmetry operations are necessary to reconstruct the full model of the material and no other symmetry information (e.g., the Hall symbol) is provided that would allow the user to derive symmetry operations unambiguously.
  - **Query**: Support for queries on this property is not required and in fact is NOT RECOMMENDED.
  - MUST be :val:`null` if :property:`nperiodic_dimensions` is equal to 0.
  - Each symmetry operation is described by a string that gives that symmetry operation in Jones' faithful representation (Bradley & Cracknell, 1972: pp. 35-37), adapted for computer string notation.
  - The letters :val:`x`, :val:`y` and :val:`z` that are typesetted with overbars in printed text represent coordinate values multiplied by -1 and are encoded as :val:`-x`, :val:`-y` and :val:`-z`, respectively.
  - The syntax of the strings representing symmetry operations MUST conform to regular expressions given in appendix `The Symmetry Operation String Regular Expressions`_.
  - The interpretation of the strings MUST follow the conventions of the IUCr CIF core dictionary (IUCr, 2023).
    In particular, this property MUST explicitly provide all symmetry operations needed to generate all the atoms in the unit cell from the atoms in the asymmetric unit, for the setting used.
  - This symmetry operation set MUST always include the :val:`x,y,z` identity operation.
  - The symmetry operations are to be applied to fractional atom coordinates.
    In case only Cartesian coordinates are available, these Cartesian coordinates must be converted to fractional coordinates before the application of the provided symmetry operations.
  - If the symmetry operation list is present, it MUST be compatible with other space group specifications (e.g. the ITC space group number, the Hall symbol, the Hermann-Mauguin symbol) if these are present.

- **Examples**:

  - Space group operations for the space group with ITC number 3 (H-M symbol :val:`P 2`, extended H-M symbol :val:`P 1 2 1`, Hall symbol :val:`P 2y`): :val:`["x,y,z", "-x,y,-z"]`
  - Space group operations for the space group with ITC number 5 (H-M symbol :val:`C 2`, extended H-M symbol :val:`C 1 2 1`, Hall symbol :val:`C 2y`): :val:`["x,y,z", "-x,y,-z", "x+1/2,y+1/2,z", "-x+1/2,y+1/2,-z"]`

- **Notes:** The list of space group symmetry operations applies to the whole periodic array of atoms and together with the lattice translations given in the :property:`lattice_vectors` property provides the necessary information to reconstruct all atom site positions of the periodic material.
  Thus, the symmetry operations described in this property are only applicable to material models with at least one periodic dimension.
  This property is not meant to represent arbitrary symmetries of molecules, non-periodic (finite) collections of atoms or non-crystallographic symmetry.

- **Bibliographic References**:

  Bradley, C. J. and Cracknell, A. P. (1972) The Mathematical Theory of Symmetry in Solids. Oxford, Clarendon Press (paperback edition 2010) 745 p. ISBN `978-0-19-958258-7 <https://isbnsearch.org/isbn/9780199582587>`__.

  IUCr (2023) Core dictionary (coreCIF) version 2.4.5; data name `\_space\_group\_symop\_operation\_xyz`. Available from: https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_symop_operation_xyz.html [Accessed 2023-06-18T16:46+03:00].

space\_group\_symbol\_hall
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: A Hall space group symbol representing the symmetry of the structure as defined in (Hall, 1981, 1981a).
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - The change-of-basis operations are used as defined in the International Tables of Crystallography (ITC) Vol. B, Sect. 1.4, Appendix A1.4.2 (IUCr, 2001).
  - Each component of the Hall symbol MUST be separated by a single space symbol.
  - If there exists a standard Hall symbol which represents the symmetry it SHOULD be used.
  - MUST be :val:`null` if :property:`nperiodic_dimensions` is not equal to 3.

- **Examples**:

  - Space group symbols with explicit origin (the Hall symbols):

    - :val:`P 2c -2ac`
    - :val:`-I 4bd 2ab 3`

  - Space group symbols with change-of-basis operations:

    - :val:`P 2yb (-1/2*x+z,1/2*x,y)`
    - :val:`-I 4 2 (1/2*x+1/2*y,-1/2*x+1/2*y,z)`

- **Bibliographic References**:

  Hall, S. R. (1981) Space-group notation with an explicit origin. Acta Crystallographica Section A, 37, 517-525, International Union of Crystallography (IUCr), DOI: https://doi.org/10.1107/s0567739481001228

  Hall, S. R. (1981a) Space-group notation with an explicit origin; erratum.  Acta Crystallographica Section A, 37, 921-921, International Union of Crystallography (IUCr), DOI: https://doi.org/10.1107/s0567739481001976

  IUCr (2001). International Tables for Crystallography vol. B. Reciprocal Space. Ed. U. Shmueli. 2-nd edition. Dordrecht/Boston/London, Kluwer Academic Publishers.

space\_group\_symbol\_hermann\_mauguin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description** A human- and machine-readable string containing the short Hermann-Mauguin (H-M) symbol which specifies the space group of the structure in the response.

- **Type**: string
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - The H-M symbol SHOULD aim to convey the closest representation of the symmetry information that can be specified using the short format used in the International Tables for Crystallography vol. A (IUCr, 2005), Table 4.3.2.1 as described in the accompanying text.
  - The symbol MAY be a non-standard short H-M symbol.
  - The H-M symbol does not unambiguously communicate the axis, cell, and origin choice, and the given symbol SHOULD NOT be amended to convey this information.
  - To encode as character strings, the following adaptations MUST be made when representing H-M symbols given in their typesetted form:

    - the overbar above the numbers MUST be changed to the minus sign in front of the digit (e.g. '-2');
    - subscripts that denote screw axes are written as digits immediately after the axis designator without a space (e.g. 'P 32')
    - the space group generators MUST be separated by a single space (e.g. 'P 21 21 2');
    - there MUST be no spaces in the space group generator designation (i.e. use 'P 21/m', not the 'P 21 / m');

- **Examples**:

  - :val:`C 2`
  - :val:`P 21 21 21`

- **Bibliographic References**:

  IUCr (2005). International Tables for Crystallography vol. A. Space-Group Symmetry. Ed. Theo Hahn. 5-th edition. Dordrecht, Springer.

space\_group\_symbol\_hermann\_mauguin\_extended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description** A human- and machine-readable string containing the extended Hermann-Mauguin (H-M) symbol which specifies the space group of the structure in the response.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - The H-M symbols SHOULD be given as specified in the International Tables for Crystallography vol. A (IUCr, 2005), Table 4.3.2.1.
  - The change-of-basis operation SHOULD be provided for the non-standard axis and cell choices.
  - The extended H-M symbol does not unambiguously communicate the origin choice, and the given symbol SHOULD NOT be amended to convey this information.
  - The description of the change-of-basis SHOULD follow conventions of the ITC Vol. B, Sect. 1.4, Appendix A1.4.2 (IUCr, 2001).
  - The same character string encoding conventions MUST be used as for the specification of the :property:`space_group_symbol_hermann_mauguin` property.

- **Examples**:

  - :val:`C 1 2 1`

- **Bibliographic References**:

  IUCr (2001). International Tables for Crystallography vol. B. Reciprocal Space. Ed. U. Shmueli. 2-nd edition. Dordrecht/Boston/London, Kluwer Academic Publishers.

  IUCr (2005). International Tables for Crystallography vol. A. Space-Group Symmetry. Ed. Theo Hahn. 5-th edition. Dordrecht, Springer.

space\_group\_it\_number
~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: Space group number which specifies the space group of the structure as defined in the International Tables for Crystallography Vol. A. (IUCr, 2005).
- **Type**: integer
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - The integer value MUST be between 1 and 230.
  - MUST be :val:`null` if :property:`nperiodic_dimensions` is not equal to 3.

cartesian\_site\_positions
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: Cartesian positions of each site in the structure.
  A site is usually used to describe positions of atoms; what atoms can be encountered at a given site is conveyed by the :property:`species_at_sites` property, and the species themselves are described in the :property:`species` property.
- **Type**: list of list of floats
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - It MUST be a list of length equal to the number of sites in the structure, where every element is a list of the three Cartesian coordinates of a site expressed as float values in the unit angstrom (Å).
  - An entry MAY have multiple sites at the same Cartesian position (for a relevant use of this, see e.g., the property `assemblies`_).

- **Examples**:

  - :val:`[[0,0,0],[0,0,2]]` indicates a structure with two sites, one sitting at the origin and one along the (positive) *z*-axis, 2 Å away from the origin.

nsites
~~~~~~

- **Description**: An integer specifying the length of the :property:`cartesian_site_positions` property.
- **Type**: integer
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.

- **Examples**:

  - :val:`42`

- **Query examples**:

  - Match only structures with exactly 4 sites: :filter:`nsites=4`
  - Match structures that have between 2 and 7 sites: :filter:`nsites>=2 AND nsites<=7`

species\_at\_sites
~~~~~~~~~~~~~~~~~~

- **Description**: Name of the species at each site (where values for sites are specified with the same order of the property `cartesian_site_positions`_).
  The properties of the species are found in the property `species`_.
- **Type**: list of strings.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - MUST have length equal to the number of sites in the structure (first dimension of the list property `cartesian_site_positions`_).
  - Each species name mentioned in the :property:`species_at_sites` list MUST be described in the list property `species`_ (i.e. for each value in the :property:`species_at_sites` list there MUST exist exactly one dictionary in the :property:`species` list with the :property:`name` attribute equal to the corresponding :property:`species_at_sites` value).
  - Each site MUST be associated only to a single species.
    **Note**: However, species can represent mixtures of atoms, and multiple species MAY be defined for the same chemical element.
    This latter case is useful when different atoms of the same type need to be grouped or distinguished, for instance in simulation codes to assign different initial spin states.

- **Examples**:

  - :val:`["Ti","O2"]` indicates that the first site is hosting a species labeled :val:`"Ti"` and the second a species labeled :val:`"O2"`.
  - :val:`["Ac", "Ac", "Ag", "Ir"]` indicates that the first two sites contain the :val:`"Ac"` species, while the third and fourth sites contain the :val:`"Ag"` and :val:`"Ir"` species, respectively.

species
~~~~~~~

- **Description**: A list describing the species of the sites of this structure.
  Species can represent pure chemical elements, virtual-crystal atoms representing a statistical occupation of a given site by multiple chemical elements, and/or a location to which there are attached atoms, i.e., atoms whose precise location are unknown beyond that they are attached to that position (frequently used to indicate hydrogen atoms attached to another element, e.g., a carbon with three attached hydrogens might represent a methyl group, -CH3).

- **Type**: list of dictionary with keys:

  - :property:`name`: string (REQUIRED)
  - :property:`chemical_symbols`: list of strings (REQUIRED)
  - :property:`concentration`: list of float (REQUIRED)
  - :property:`attached`: list of strings (OPTIONAL)
  - :property:`nattached`: list of integers (OPTIONAL)
  - :property:`mass`: list of floats (OPTIONAL)
  - :property:`original_name`: string (OPTIONAL).

- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - Each list member MUST be a dictionary with the following keys:

    - **name**: REQUIRED; gives the name of the species; the **name** value MUST be unique in the :property:`species` list;

    - **chemical\_symbols**: REQUIRED; MUST be a list of strings of all chemical elements composing this species. Each item of the list MUST be one of the following:

      - a valid chemical-element symbol, or
      - the special value :val:`"X"` to represent a non-chemical element, or
      - the special value :val:`"vacancy"` to represent that this site has a non-zero probability of having a vacancy (the respective probability is indicated in the :property:`concentration` list, see below).

      If any one entry in the :property:`species` list has a :property:`chemical_symbols` list that is longer than 1 element, the correct flag MUST be set in the list :property:`structure_features` (see property `structure_features`_).

    - **concentration**: REQUIRED; MUST be a list of floats, with same length as :property:`chemical_symbols`. The numbers represent the relative concentration of the corresponding chemical symbol in this species.
      The numbers SHOULD sum to one. Cases in which the numbers do not sum to one typically fall only in the following two categories:

      - Numerical errors when representing float numbers in fixed precision, e.g. for two chemical symbols with concentrations :val:`1/3` and :val:`2/3`, the concentration might look something like :val:`[0.33333333333, 0.66666666666]`. If the client is aware that the sum is not one because of numerical precision, it can renormalize the values so that the sum is exactly one.
      - Experimental errors in the data present in the database. In this case, it is the responsibility of the client to decide how to process the data.

      Note that concentrations are uncorrelated between different sites (even of the same species).

    - **attached**: OPTIONAL; if provided MUST be a list of length 1 or more of strings of chemical symbols for the elements attached to this site, or "X" for a non-chemical element.
    - **nattached**: OPTIONAL; if provided MUST be a list of length 1 or more of integers indicating the number of attached atoms of the kind specified in the value of the :field:`attached` key.

      The implementation MUST include either both or none of the :field:`attached` and :field:`nattached` keys, and if they are provided, they MUST be of the same length.
      Furthermore, if they are provided, the `structure_features`_ property MUST include the string :val:`site_attachments`.

    - **mass**: OPTIONAL. If present MUST be a list of floats, with the same length as :property:`chemical_symbols`, providing element masses expressed in a.m.u.
      Elements denoting vacancies MUST have masses equal to 0.
    - **original\_name**: OPTIONAL. Can be any valid Unicode string, and SHOULD contain (if specified) the name of the species that is used internally in the source database.

    **Note**: With regard to "source database", we refer to the immediate source being queried via the OPTIMADE API implementation.
    The main use of this field is for source databases that use species names, containing characters that are not allowed (see description of the list property `species_at_sites`_).

  - For systems that have only species formed by a single chemical symbol, and that have at most one species per chemical symbol, SHOULD use the chemical symbol as species name (e.g., :val:`"Ti"` for titanium, :val:`"O"` for oxygen, etc.)
    However, note that this is OPTIONAL, and client implementations MUST NOT assume that the key corresponds to a chemical symbol, nor assume that if the species name is a valid chemical symbol, that it represents a species with that chemical symbol.
    This means that a species :val:`{"name": "C", "chemical_symbols": ["Ti"], "concentration": [1.0]}` is valid and represents a titanium species (and *not* a carbon species).
  - It is NOT RECOMMENDED that a structure includes species that do not have at least one corresponding site.

- **Examples**:

  - :val:`[ {"name": "Ti", "chemical_symbols": ["Ti"], "concentration": [1.0]} ]`: any site with this species is occupied by a Ti atom.
  - :val:`[ {"name": "Ti", "chemical_symbols": ["Ti", "vacancy"], "concentration": [0.9, 0.1]} ]`: any site with this species is occupied by a Ti atom with 90 % probability, and has a vacancy with 10 % probability.
  - :val:`[ {"name": "BaCa", "chemical_symbols": ["vacancy", "Ba", "Ca"], "concentration": [0.05, 0.45, 0.5], "mass": [0.0, 137.327, 40.078]} ]`: any site with this species is occupied by a Ba atom with 45 % probability, a Ca atom with 50 % probability, and by a vacancy with 5 % probability.
  - :val:`[ {"name": "C12", "chemical_symbols": ["C"], "concentration": [1.0], "mass": [12.0]} ]`: any site with this species is occupied by a carbon isotope with mass 12.
  - :val:`[ {"name": "C13", "chemical_symbols": ["C"], "concentration": [1.0], "mass": [13.0]} ]`: any site with this species is occupied by a carbon isotope with mass 13.
  - :val:`[ {"name": "CH3", "chemical_symbols": ["C"], "concentration": [1.0], "attached": ["H"], "nattached": [3]} ]`: any site with this species is occupied by a methyl group, -CH3, which is represented without specifying precise positions of the hydrogen atoms.

assemblies
~~~~~~~~~~

- **Description**: A description of groups of sites that are statistically correlated.
- **Type**: list of dictionary with keys:

  - :property:`sites_in_groups`: list of list of integers (REQUIRED)
  - :property:`group_probabilities`: list of floats (REQUIRED)

- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - The property SHOULD be :val:`null` for entries that have no partial occupancies.
  - If present, the correct flag MUST be set in the list :property:`structure_features` (see property `structure_features`_).
  - Client implementations MUST check its presence (as its presence changes the interpretation of the structure).
  - If present, it MUST be a list of dictionaries, each of which represents an assembly and MUST have the following two keys:

    - **sites\_in\_groups**: Index of the sites (0-based) that belong to each group for each assembly.

      Example: :val:`[[1], [2]]`: two groups, one with the second site, one with the third.
      Example: :val:`[[1,2], [3]]`: one group with the second and third site, one with the fourth.

    - **group\_probabilities**: Statistical probability of each group. It MUST have the same length as :property:`sites_in_groups`.
      It SHOULD sum to one.
      See below for examples of how to specify the probability of the occurrence of a vacancy.
      The possible reasons for the values not to sum to one are the same as already specified above for the :property:`concentration` of each :property:`species`, see property `species`_.

  - If a site is not present in any group, it means that it is present with 100 % probability (as if no assembly was specified).
  - A site MUST NOT appear in more than one group.

- **Examples** (for each entry of the assemblies list):

  - :val:`{"sites_in_groups": [[0], [1]], "group_probabilities": [0.3, 0.7]}`: the first site and the second site never occur at the same time in the unit cell.
    Statistically, 30 % of the times the first site is present, while 70 % of the times the second site is present.
  - :val:`{"sites_in_groups": [[1,2], [3]], "group_probabilities": [0.3, 0.7]}`: the second and third sites are either present together or not present; they form the first group of atoms for this assembly.
    The second group is formed by the fourth site.
    Sites of the first group (the second and the third) are never present at the same time as the fourth site.
    30 % of times sites 1 and 2 are present (and site 3 is absent); 70 % of times site 3 is present (and sites 1 and 2 are absent).

- **Notes**:

  - Assemblies are essential to represent, for instance, the situation where an atom can statistically occupy two different positions (sites).
  - By defining groups, it is possible to represent, e.g., the case where a functional molecule (and not just one atom) is either present or absent (or the case where it is present in two conformations).
  - Considerations on virtual alloys and on vacancies: In the special case of a virtual alloy, these specifications allow two different, equivalent ways of specifying them.
    For instance, for a site at the origin with 30 % probability of being occupied by Si, 50 % probability of being occupied by Ge, and 20 % of being a vacancy, the following two representations are possible:

    - Using a single species:

      .. code:: jsonc

           {
             "cartesian_site_positions": [[0,0,0]],
             "species_at_sites": ["SiGe-vac"],
             "species": [
               {
                 "name": "SiGe-vac",
                 "chemical_symbols": ["Si", "Ge", "vacancy"],
                 "concentration": [0.3, 0.5, 0.2]
               }
             ]
             // ...
           }


    - Using multiple species and the assemblies:

      .. code:: jsonc

           {
             "cartesian_site_positions": [ [0,0,0], [0,0,0], [0,0,0] ],
             "species_at_sites": ["Si", "Ge", "vac"],
             "species": [
               { "name": "Si", "chemical_symbols": ["Si"], "concentration": [1.0] },
               { "name": "Ge", "chemical_symbols": ["Ge"], "concentration": [1.0] },
               { "name": "vac", "chemical_symbols": ["vacancy"], "concentration": [1.0] }
             ],
             "assemblies": [
               {
                 "sites_in_groups": [ [0], [1], [2] ],
                 "group_probabilities": [0.3, 0.5, 0.2]
               }
             ]
             // ...
           }

  - It is up to the database provider to decide which representation to use, typically depending on the internal format in which the structure is stored.
    However, given a structure identified by a unique ID, the API implementation MUST always provide the same representation for it.
  - The probabilities of occurrence of different assemblies are uncorrelated.
    So, for instance in the following case with two assemblies:

    .. code:: jsonc

         {
           "assemblies": [
             {
               "sites_in_groups": [ [0], [1] ],
               "group_probabilities": [0.2, 0.8]
             },
             {
               "sites_in_groups": [ [2], [3] ],
               "group_probabilities": [0.3, 0.7]
             }
           ]
         }

    Site 0 is present with a probability of 20 % and site 1 with a probability of 80 %. These two sites are correlated (either site 0 or 1 is present). Similarly, site 2 is present with a probability of 30 % and site 3 with a probability of 70 %.
    These two sites are correlated (either site 2 or 3 is present).
    However, the presence or absence of sites 0 and 1 is not correlated with the presence or absence of sites 2 and 3 (in the specific example, the pair of sites (0, 2) can occur with 0.2\*0.3 = 6 % probability; the pair (0, 3) with 0.2\*0.7 = 14 % probability; the pair (1, 2) with 0.8\*0.3 = 24 % probability; and the pair (1, 3) with 0.8\*0.7 = 56 % probability).

structure\_features
~~~~~~~~~~~~~~~~~~~

- **Description**: A list of strings that flag which special features are used by the structure.
- **Type**: list of strings
- **Requirements/Conventions**:

  - **Support**: MUST be supported by all implementations, MUST NOT be :val:`null`.
  - **Query**: MUST be a queryable property.
    Filters on the list MUST support all mandatory HAS-type queries.
    Filter operators for comparisons on the string components MUST support equality, support for other comparison operators are OPTIONAL.
  - MUST be an empty list if no special features are used.
  - MUST be sorted alphabetically.
  - If a special feature listed below is used, the list MUST contain the corresponding string.
  - If a special feature listed below is not used, the list MUST NOT contain the corresponding string.
  - **List of strings used to indicate special structure features**:

    - :val:`disorder`: this flag MUST be present if any one entry in the `species`_ list has a :field:`chemical_symbols` list that is longer than 1 element.
    - :val:`implicit_atoms`: this flag MUST be present if the structure contains atoms that are not assigned to sites via the property `species_at_sites`_ (e.g., because their positions are unknown).
      When this flag is present, the properties related to the chemical formula will likely not match the type and count of atoms represented by the `species_at_sites`_, `species`_, and `assemblies`_ properties.
    - :val:`site_attachments`: this flag MUST be present if any one entry in the `species`_ list includes :field:`attached` and :field:`nattached`.
    - :val:`assemblies`: this flag MUST be present if the property `assemblies`_ is present.

- **Examples**:

  - A structure having implicit atoms and using assemblies: :val:`["assemblies", "implicit_atoms"]`

Calculations Entries
--------------------

The :entry:`calculations` entries have the properties described above in section `Properties Used by Multiple Entry Types`_.

References Entries
------------------

The :entry:`references` entries describe bibliographic references.
The following properties are used to provide the bibliographic details:

- **address**, **annote**, **booktitle**, **chapter**, **crossref**, **edition**, **howpublished**, **institution**, **journal**, **key**, **month**, **note**, **number**, **organization**, **pages**, **publisher**, **school**, **series**, **title**, **volume**, **year**: meanings of these properties match the `BibTeX specification <http://bibtexml.sourceforge.net/btxdoc.pdf>`__, values are strings;

- **bib_type**: type of the reference, corresponding to **type** property in the BibTeX specification, value is string;

- **authors** and **editors**: lists of *person objects* which are dictionaries with the following keys:

  - **name**: Full name of the person, REQUIRED.
  - **firstname**, **lastname**: Parts of the person's name, OPTIONAL.

- **doi** and **url**: values are strings.

- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., any of the properties MAY be :val:`null`.
  - **Query**: Support for queries on any of these properties is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - Every references entry MUST contain at least one of the properties.

Example:

.. code:: jsonc

    {
      "data": {
        "type": "references",
        "id": "Dijkstra1968",
        "attributes": {
          "authors": [
            {
              "name": "Edsger Dijkstra",
              "firstname": "Edsger",
              "lastname": "Dijkstra"
            }
          ],
          "year": "1968",
          "title": "Go To Statement Considered Harmful",
          "journal": "Communications of the ACM",
          "doi": "10.1145/362929.362947"
        }
      }
    }

Files Entries
-------------

The :entry:`files` entries describe files.
The following properties are used to do so:

url
~~~

- **Description**: The URL to get the contents of a file.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: MUST be supported by all implementations, MUST NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - **Response**: REQUIRED in the response.
  - The URL MUST point to the actual contents of a file (i.e. byte stream), not an intermediate (preview) representation.
    For example, if referring to a file on GitHub, a link should point to raw contents.

- **Examples**:

  - :val:`"https://example.org/files/cifs/1000000.cif"`

url\_stable\_until
~~~~~~~~~~~~~~~~~~

- **Description**: Point in time until which the URL in :property:`url` is guaranteed to stay stable.
- **Type**: timestamp
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - :val:`null` means that there is no stability guarantee for the URL in :property:`url`.
    Indefinite support could be communicated by providing a date sufficiently far in the future, for example, :val:`9999-12-31`.

name
~~~~

- **Description**: Base name of a file.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: MUST be supported by all implementations, MUST NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - File name extension is an integral part of a file name and, if available, MUST be included.

- **Examples**:

  - :val:`"1000000.cif"`

size
~~~~

- **Description**: Size of a file in bytes.
- **Type**: integer
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - If provided, it MUST be guaranteed that either exact size of a file is given or its upper bound.
    This way if a client reserves a static buffer or truncates the download stream after this many bytes the whole file would be received.
    Such provision is included to allow the providers to serve on-the-fly compressed files.

media\_type
~~~~~~~~~~~

- **Description**: Media type identifier (also known as MIME type), for a file as per `RFC 6838 Media Type Specifications and Registration Procedures <https://datatracker.ietf.org/doc/html/rfc6838>`__.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.

- **Examples**:

  - :val:`"chemical/x-cif"`

version
~~~~~~~

- **Description**: Version information of a file (e.g. commit, revision, timestamp).
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - If provided, it MUST be guaranteed that file contents pertaining to the same combination of :field:`id` and :field:`version` are the same.

modification\_timestamp
~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: Timestamp of the last modification of file contents.
  A modification is understood as an addition, change or deletion of one or more bytes, resulting in file contents different from the previous.
- **Type**: timestamp
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - Timestamps of subsequent file modifications SHOULD be increasing (not earlier than previous timestamps).

description
~~~~~~~~~~~

- **Description**: Free-form description of a file.
- **Type**: string
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.

- **Examples**:

  - :val:`"POSCAR format file"`

checksums
~~~~~~~~~

* **Description**: Dictionary providing checksums of file contents.
* **Type**: dictionary with keys identifying checksum functions and values (strings) giving the actual checksums
* **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - Supported dictionary keys: :property:`md5`, :property:`sha1`, :property:`sha224`, :property:`sha256`, :property:`sha384`, :property:`sha512`.
    Checksums outside this list MAY be used, but their names MUST be prefixed by a database-provider-specific namespace prefix (see appendix `Namespace Prefixes`_).

atime
~~~~~

- **Description**: Time of last access of a file as per POSIX standard.
- **Type**: timestamp
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.

ctime
~~~~~

- **Description**: Time of last status change of a file as per POSIX standard.
- **Type**: timestamp
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.

mtime
~~~~~

- **Description**: Time of last modification of a file as per POSIX standard.
- **Type**: timestamp
- **Requirements/Conventions**:

  - **Support**: OPTIONAL support in implementations, i.e., MAY be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
  - It should be noted that the values of :field:`last_modified`, :field:`modification_timestamp` and :field:`mtime` do not necessary match.
    :field:`last_modified` pertains to the modification of the OPTIMADE metadata, :field:`modification_timestamp` pertains to file contents and :field:`mtime` pertains to the modification of the file (not necessary changing its contents).
    For example, appending an empty string to a file would result in the change of :field:`mtime` in some operating systems, but this would not be deemed as a modification of its contents.

Custom Entry Types
------------------

Database and definition providers can define custom entry types.
The names of such entry types MUST start with corresponding namespace prefix (see appendix `Namespace Prefixes`_).
Custom entry types MUST have all properties described above in section `Properties Used by Multiple Entry Types`_.

- **Requirements/Conventions for properties in custom entry types**:

  - **Support**: Support for any properties in database-provider-specific or definition-provider-specific entry types is fully OPTIONAL.
  - **Query**: Support for queries on these properties are OPTIONAL.
    If supported, only a subset of the filter features MAY be supported.

Relationships Used by Multiple Entry Types
------------------------------------------

In accordance with section `Relationships`_, all entry types MAY use relationships to describe relations to other entries.

References
~~~~~~~~~~

The references relationship is used to provide bibliographic references for any of the entry types.
It relates an entry with any number of :entry:`references` entries.

If the response format supports inclusion of entries of a different type in the response, then the response SHOULD include all references-type entries mentioned in the response.

For example, for the JSON response format, the top-level :field:`included` field SHOULD be used as per the `JSON:API 1.1 specification <https://jsonapi.org/format/1.1/#fetching-includes>`__:

.. code:: jsonc

    {
      "data": {
        "type": "structures",
        "id": "example.db:structs:1234",
        "attributes": {
          "formula": "Es2",
          "url": "http://example.db/structs/1234",
          "immutable_id": "http://example.db/structs/1234@123",
          "last_modified": "2007-04-07T12:02:20Z"
        },
        "relationships": {
          "references": {
            "data": [
              { "type": "references", "id": "Dijkstra1968" },
              {
                "type": "references",
                "id": "1234",
                "meta": {
                  "description": "Reference for the general crystal prototype."
                }
              }
            ]
          }
        }
      },
      "included": [
        {
          "type": "references",
          "id": "Dijkstra1968",
          "attributes": {
            "authors": [
              {
                "name": "Edsger Dijkstra",
                "firstname": "Edsger",
                "lastname": "Dijkstra"
              }
            ],
            "year": "1968",
            "title": "Go To Statement Considered Harmful",
            "journal": "Communications of the ACM",
            "doi": "10.1145/362929.362947"
          }
        },
        {
          "type": "references",
          "id": "1234",
          "attributes": {
            "doi": "10.1234/1234"
          }
        }
      ]
    }

Calculations
~~~~~~~~~~~~

Relationships with calculations MAY be used to indicate provenance where a structure is either an input to or an output of calculations.

    **Note**: We intend to implement in a future version of this API a standardized mechanism to differentiate these two cases, thus allowing databases a common way of exposing the full provenance tree with inputs and outputs between structures and calculations.

    At the moment the database providers are suggested to extend their API the way they choose, always using their database-provider-specific prefix in non-standardized fields.

Files
~~~~~

Relationships with files may be used to relate an entry with any number of :entry:`files` entries.

.. code:: jsonc

    {
      "data": {
        "type": "structures",
        "id": "example.db:structs:1234",
        "attributes": {
          "chemical_formula_descriptive": "H2O"
        },
        "relationships": {
          "files": {
            "data": [
              { "type": "files", "id": "example.db:files:1234" }
            ]
          }
        }
      },
      "included": [
        {
          "type": "files",
          "id": "example.db:files:1234",
          "attributes": {
            "media_type": "chemical/x-cif",
            "url": "https://example.org/files/cifs/1234.cif"
          }
        }
      ]
    }

Appendices
==========

The Filter Language EBNF Grammar
--------------------------------

.. code:: ebnf

    (* BEGIN EBNF GRAMMAR Filter *)
    (* The top-level 'filter' rule: *)

    Filter = [Spaces], Expression ;

    (* Values *)

    OrderedConstant = String | Number ;
    UnorderedConstant = ( TRUE | FALSE ) ;

    Value = ( UnorderedConstant | OrderedValue ) ;

    OrderedValue = ( OrderedConstant | Property ) ;
    (* Note: support for Property in OrderedValue is OPTIONAL *)

    ValueListEntry = ( Value | ValueEqRhs | ValueRelCompRhs | FuzzyStringOpRhs ) ;
    (* Note: support for ValueEqRhs, ValueRelCompRhs and FuzzyStringOpRhs in ValueListEntry are OPTIONAL *)

    ValueList = ValueListEntry, { Comma, ValueListEntry } ;
    ValueZip = ValueListEntry, Colon, ValueListEntry, { Colon, ValueListEntry } ;

    ValueZipList = ValueZip, { Comma, ValueZip } ;

    (* Expressions *)

    Expression = ExpressionClause, [ OR, Expression ] ;

    ExpressionClause = ExpressionPhrase, [ AND, ExpressionClause ] ;

    ExpressionPhrase = [ NOT ], ( Comparison | OpeningBrace, Expression, ClosingBrace ) ;

    Comparison = ConstantFirstComparison
               | PropertyFirstComparison ;
    (* Note: support for ConstantFirstComparison is OPTIONAL *)

    ConstantFirstComparison = ( OrderedConstant, ValueOpRhs
                              | UnorderedConstant, ValueEqRhs ) ;

    PropertyFirstComparison = Property, [ ValueOpRhs
                                        | KnownOpRhs
                                        | FuzzyStringOpRhs
                                        | SetOpRhs
                                        | SetZipOpRhs
                                        | LengthOpRhs ] ;
    (* Note: support for SetZipOpRhs in Comparison is OPTIONAL *)

    ValueOpRhs = ( ValueEqRhs | ValueRelCompRhs ) ;

    ValueEqRhs = EqualityOperator, Value ;

    ValueRelCompRhs = RelativeComparisonOperator, OrderedValue ;

    KnownOpRhs = IS, ( KNOWN | UNKNOWN ) ;

    FuzzyStringOpRhs = CONTAINS, Value
                     | STARTS, [ WITH ], Value
                     | ENDS, [ WITH ], Value ;

    SetOpRhs = HAS, ( ( Value | EqualityOperator, Value | RelativeComparisonOperator, OrderedValue | FuzzyStringOpRhs ) | ALL, ValueList | ANY, ValueList | ONLY, ValueList ) ;
    (* Note: support for the alternatives with EqualityOperator, RelativeComparisonOperator, FuzzyStringOpRhs, and ONLY in SetOpRhs are OPTIONAL *)

    SetZipOpRhs = PropertyZipAddon, HAS, ( ValueZip | ONLY, ValueZipList | ALL, ValueZipList | ANY, ValueZipList ) ;

    PropertyZipAddon = Colon, Property, { Colon, Property } ;

    LengthOpRhs = LENGTH, [ Operator ], Value ;
    (* Note: support for [ Operator ] in LengthOpRhs is OPTIONAL *)

    (* Property *)

    Property = Identifier, { Dot, Identifier } ;

    (* TOKENS *)

    (* Separators: *)

    OpeningBrace = '(', [Spaces] ;
    ClosingBrace = ')', [Spaces] ;

    Dot = '.', [Spaces] ;
    Comma = ',', [Spaces] ;
    Colon = ':', [Spaces] ;

    (* Boolean relations: *)

    AND = 'AND', [Spaces] ;
    NOT = 'NOT', [Spaces] ;
    OR = 'OR', [Spaces] ;

    IS = 'IS', [Spaces] ;
    KNOWN = 'KNOWN', [Spaces] ;
    UNKNOWN = 'UNKNOWN', [Spaces] ;

    CONTAINS = 'CONTAINS', [Spaces] ;
    STARTS = 'STARTS', [Spaces] ;
    ENDS = 'ENDS', [Spaces] ;
    WITH = 'WITH', [Spaces] ;

    LENGTH = 'LENGTH', [Spaces] ;
    HAS = 'HAS', [Spaces] ;
    ALL = 'ALL', [Spaces] ;
    ONLY = 'ONLY', [Spaces] ;
    ANY = 'ANY', [Spaces] ;

    (* Comparison operator tokens: *)

    Operator = ( EqualityOperator | RelativeComparisonOperator ) ;
    EqualityOperator = [ '!' ], '=' , [Spaces] ;
    RelativeComparisonOperator = ( '<' | '>' ), [ '=' ], [Spaces] ;

    (* Boolean values *)

    TRUE = 'TRUE', [Spaces] ;
    FALSE = 'FALSE', [Spaces] ;

    (* Property syntax *)

    Identifier = LowercaseLetter, { LowercaseLetter | Digit }, [Spaces] ;

    Letter = UppercaseLetter | LowercaseLetter ;

    UppercaseLetter = 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I'
                    | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R'
                    | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' ;

    LowercaseLetter = 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i'
                    | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r'
                    | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '_' ;

    (* Strings: *)

    String = '"', { EscapedChar }, '"', [Spaces] ;

    EscapedChar = UnescapedChar | '\', '"' | '\', '\' ;

    UnescapedChar = Letter | Digit | Space | Punctuator | UnicodeHighChar ;

    Punctuator = '!' | '#' | '$' | '%' | '&' | "'" | '(' | ')' | '*' | '+'
               | ',' | '-' | '.' | '/' | ':' | ';' | '<' | '=' | '>' | '?'
               | '@' | '[' | ']' | '^' | '`' | '{' | '|' | '}' | '~' ;

    (* BEGIN EBNF GRAMMAR Number *)
    (* Number token syntax: *)

    Number = [ Sign ] ,
             ( Digits, [ '.', [ Digits ] ] | '.' , Digits ),
             [ Exponent ], [Spaces] ;

    Exponent =  ( 'e' | 'E' ) , [ Sign ] , Digits ;

    Sign = '+' | '-' ;

    Digits =  Digit, { Digit } ;

    Digit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;

    (* White-space: *)

    (* Special character tokens: *)

    tab = ? \t ?;
    nl  = ? \n ?;
    cr  = ? \r ?;
    vt  = ? \v ?;
    ff  = ? \f ?;

    Space = ' ' | tab | nl | cr | vt | ff ;

    Spaces = Space, { Space } ;

    (* The 'UnicodeHighChar' specifies any Unicode character above 0x7F.
       It is specified in this grammar by an extension to EBNF that allows a
       regular expression to specify terminal symbol ranges. *)

    UnicodeHighChar = ? [^\x00-\x7F] ? ;

    (* END EBNF GRAMMAR Number *)
    (* END EBNF GRAMMAR Filter *)

Note: when implementing a parser according this grammar, the implementers MAY choose to construct a lexer that ignores all whitespace (spaces, tabs, newlines, vertical tabulation and form feed characters, as described in the grammar 'Space' definition), and use such a lexer to recognize language elements that are described in the ``(* TOKENS *)`` section of the grammar.
In that case, it can be beneficial to remove the '[Spaces]' element from the ``Filter = [Spaces], Expression`` definition as well and use the remaining grammar rules as a parser generator input (e.g., for yacc, bison, antlr).

Regular Expressions for OPTIMADE Filter Tokens
----------------------------------------------

The string below contains Perl-Compatible Regular Expressions to recognize identifiers, number, and string values as specified in this specification.

.. code::

    #BEGIN PCRE identifiers
    [a-z_][a-z_0-9]*
    #END PCRE identifiers

    #BEGIN PCRE numbers
    [-+]?(?:\d+(\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?
    #END PCRE numbers

    #BEGIN PCRE strings
    "([^\\"]|\\.)*"
    #END PCRE strings

The strings below contain Extended Regular Expressions (EREs) to recognize identifiers, number, and string values as specified in this specification.

.. code::

    #BEGIN ERE identifiers
    [a-z_][a-z_0-9]*
    #END ERE identifiers

    #BEGIN ERE numbers
    [-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?
    #END ERE numbers

    #BEGIN ERE strings
    "([^\"]|\\.)*"
    #END ERE strings

The Symmetry Operation String Regular Expressions
-------------------------------------------------

Symmetry operation strings that comprise the :property:`space_group_symmetry_operations_xyz` property MUST conform to the following regular expressions.
The regular expressions are recorded below in two forms, one in a more readable form using variables and the other as an explicit pattern compatible with the `OPTIMADE Regular Expression Format`_.

- Perl Compatible Regular Expression (PCRE) syntax, with `Perl extensions <https://perldoc.perl.org/perlre>`__ used for readability and expressivity.
  The :val:`symop_definitions` section defines several variables in Perl syntax that capture common parts of the regular expressions (REs) and need to be interpolated into the final REs used for matching.
  The :val:`symops` section contains the REs themselves.
  The whitespace characters in these definitions are not significant; if used in Perl programs, these expressions MUST be processed with the :code:`/x` RE modifier.
  A working example of these REs in action can be found in the :code:`tests/cases/pcre_symops_001.sh` and other test cases.


  .. code:: PCRE

     #BEGIN PCRE symop_definitions

     $translations = '1\/2|[12]\/3|[1-3]\/4|[1-5]\/6';

     $symop_translation_appended = "[-+]? [xyz] ([-+][xyz])? ([-+] ($translations) )?";
     $symop_translation_prepended = "[-+]? ($translations) ([-+] [xyz] ([-+][xyz])? )?";

     $symop_re = "($symop_translation_appended|$symop_translation_prepended)";

     #END PCRE symop_definitions

  .. code:: PCRE

     #BEGIN PCRE symops

     ^ # From the beginning of the string...
     ($symop_re)(,$symop_re){2}
     $ # ... match to the very end of the string

     #END PCRE symops

- The regular expression is also provided in an expanded form as an OPTIMADE regex:

  .. code:: ECMA

     #BEGIN ECMA symops

     ^([-+]?[xyz]([-+][xyz])?([-+](1/2|[12]/3|[1-3]/4|[1-5]/6))?|[-+]?(1/2|[12]/3|[1-3]/4|[1-5]/6)([-+][xyz]([-+][xyz])?)?),([-+]?[xyz]([-+][xyz])?([-+](1/2|[12]/3|[1-3]/4|[1-5]/6))?|[-+]?(1/2|[12]/3|[1-3]/4|[1-5]/6)([-+][xyz]([-+][xyz])?)?),([-+]?[xyz]([-+][xyz])?([-+](1/2|[12]/3|[1-3]/4|[1-5]/6))?|[-+]?(1/2|[12]/3|[1-3]/4|[1-5]/6)([-+][xyz]([-+][xyz])?)?)$

     #END ECMA symops

OPTIMADE JSON lines partial data format
---------------------------------------
The OPTIMADE JSON lines partial data format is a lightweight format for transmitting property data that are too large to fit in a single OPTIMADE response.
The format is based on `JSON Lines <https://jsonlines.org/>`__, which enables streaming of JSON data.
Note: since the below definition references both JSON fields and OPTIMADE properties, the data type names depend on context: for JSON they are, e.g., "array" and "object" and for OPTIMADE properties they are, e.g., "list" and "dictionary".

.. _slice object:

To aid the definition of the format below, we first define a "slice object" to be a JSON object describing slices of arrays.
The dictionary has the following OPTIONAL fields:

- :field:`"start"`: Integer.
  The slice starts at the value with the given index (inclusive).
  The default is 0, i.e., the value at the start of the array.
- :field:`"stop"`: Integer.
  The slice ends at the value with the given index (inclusive).
  If omitted, the end of the slice is the last index of the array.
- :field:`"step"`: Integer.
  The absolute difference in index between two subsequent values that are included in the slice.
  The default is 1, i.e., every value in the range indicated by :field:`start` and :field:`stop` is included in the slice.
  Hence, a value of 2 denotes a slice of every second value in the array.

For example, for the array :val:`["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]` the slice object :val:`{"start": 1, "end": 7, "step": 3}` refers to the items :val:`["b", "e", "h"]`.

Furthermore, we also define the following special markers:

- The *end-of-data-marker* is this exact JSON: :val:`["PARTIAL-DATA-END", [""]]`.
- A *reference-marker* is this exact JSON: :val:`["PARTIAL-DATA-REF", ["<url>"]]`, where :val:`"<url>"` is to be replaced with a URL being referenced.
  A reference-marker MUST only occur in a place where the property being communicated could have an embedded list.
- A *next-marker* is this exact JSON: :val:`["PARTIAL-DATA-NEXT", ["<url>"]]`, where :val:`"<url>"` is to be replaced with the target URL for the next link.

There is no requirement on the syntax or format of the URLs provided in these markers.
When data is fetched from these URLs the response MUST use the JSON lines partial data format, i.e., the markers cannot be used to link to partial data provided in other formats.
The markers have been deliberately designed to be valid JSON objects but *not* valid OPTIMADE property values.
Since the OPTIMADE list data type is defined as a list of values of the same data type or :val:`null`, the above markers cannot be encountered inside the actual data of an OPTIMADE property.

  **Implementation note:** the recognizable string values for the markers should make it possible to prescreen the raw text of the JSON data lines for the reference-marker string to determine which are the lines that one can exclude from further processing to resolve references (alternatively, this screening can be done by the string parser used by the JSON parser).
  The underlying design idea is that for lines that have reference-markers, the time it takes to process the data structure to locate the markers should be negligible compared to the time it takes to resolve and handle the large data they reference.
  Hence, the most relevant optimization is to avoid spending time processing data structures to find markers for lines where there are none.

The full response MUST be valid `JSON Lines <https://jsonlines.org/>`__ that adheres to the following format:

- The first line is a header object (defined below).
- The following lines are data lines adhering to the formats described below.
- The final line is either an end-of-data-marker (indicating that there is no more data to be given), or a next-marker indicating that more data is available, which can be obtained by retrieving data from the provided URL.

The first line MUST be a JSON object providing header information.
The header object MUST contain the keys:

- :field:`"optimade-partial-data"`: Object.
  An object identifying the response as being on OPTIMADE partial data format.

  It MUST contain the following key:

  - :field:`"format"`: String.
    Specifies the minor version of the partial data format used.
    The string MUST be of the format "MAJOR.MINOR", referring to the version of the OPTIMADE standard that describes the format.
    The version number string MUST NOT be prefixed by, e.g., "v". In implementations of the present version of the standard, the value MUST be exactly :val:`1.2`.
    A client MUST NOT expect to be able to parse the :field:`format` value if the field is not a string of the format MAJOR.MINOR or if the MAJOR version number is unrecognized.

- :field:`"layout"`: String.
  A string either equal to :val:`"dense"` or :val:`"sparse"` to indicate whether the returned format uses a dense or sparse layout.

The following key is RECOMMENDED in the header object:

- :field:`"returned_ranges"`: Array of Object.
  For dense layout, and sparse layout of one dimensional list properties, the array contains a single element which is a `slice object`_ representing the range of data present in the response.
  In the specific case of a hierarchy of list properties represented as a sparse multidimensional array, if the field :field:`"returned_ranges"` is given, it MUST contain one slice object per dimension of the multidimensional array, representing slices for each dimension that cover the data given in the response.

The header object MAY also contain the keys:

- :field:`"property_name"`: String.
  The name of the property being provided.

- :field:`"entry"`: Object.
  An object that MUST have the following two keys:

  - :field:`"id"`: String.
    The id of the entry of the property being provided.

  - :field:`"type"`: String.
    The type of the entry of the property being provided.

- :field:`"has_references"`: Boolean.
  An optional boolean to indicate whether any of the data lines in the response contains a reference marker.
  A value of :val:`false` means that the client does not have to process any of the lines to detect reference markers, which may speed up the parsing.

- :field:`"item_schema"`: Object.
  An object that represents a JSON Schema that validates the data lines of the response.
  The format SHOULD be the relevant partial extract of a valid property definition as described in `Property Definitions`_.
  If a schema is provided, it MUST be a valid JSON schema using the same version of JSON schema as described in that section.

- :field:`"links"`: Object.
  An object to provide relevant links for the property being provided.
  It MAY contain the following key:

  - :field:`"base_url"`: String.
    The base URL of the implementation serving the database to which this property belongs.

  - :field:`"item_describedby"`: String.
    A URL to an external JSON Schema that validates the data lines of the response.
    The format and requirements on this schema are the same as for the inline schema field :field:`item_schema`.

The format of data lines of the response (i.e., all lines except the first and the last) depends on whether the header object specifies the layout as :val:`"dense"` or :val:`"sparse"`.

- **Dense layout:** In the dense partial data layout, each data line reproduces one item from the OPTIMADE list property being transmitted in the JSON format.
  If OPTIMADE list properties are embedded inside the item, they can either be included in full or replaced with a reference-marker.
  If a list is replaced by a reference marker, the client MAY use the provided URL to obtain the list items.
  If the field :field:`"returned_ranges"` is omitted, then the client MUST assume that the data is a continuous range of data from the start of the array up to the number of elements given until reaching the end-of-data-marker or next-marker.

- **Sparse layout for one-dimensional list:** When the response sparsely communicates items for a one-dimensional OPTIMADE list property, each data line contains a JSON array of the format:

  - The first item of the array is the zero-based index of list property item being provided by this line.
  - The second item of the array is the list property item located at the indicated index, represented using the same format as each line in the dense layout.
    In the same way as for the dense layout, reference-markers are allowed inside the item data for embedded lists that do not fit in the response (see example below).

- **Sparse layout for multidimensional lists:** the server MAY use a specific sparse layout for the case that the OPTIMADE property represents a series of directly hierarchically embedded lists (i.e., a multidimensional sparse array).
  In this case, each data line contains a JSON array of the format:

  - All array items except the last one are integer zero-based indices of the list property item being provided by this line; these indices refer to the aggregated dimensions in the order of outermost to innermost.
  - The last item of the array is the list property item located at the indicated coordinates, represented using the same format as each line in the dense layout.
    In the same way as for the dense layout, reference-markers are allowed inside the item data for embedded lists that do not fit in the response (see example below).

If the final line of the response is a next-marker, the client MAY continue fetching the data for the property by retrieving another partial data response from the provided URL.
If the final line is an end-of-data-marker, any data not covered by any of the responses are to be assigned the value :val:`null`.

If :field:`"returned_ranges"` is included in the response and the client encounters a next-marker before receiving all lines indicated by the slice, it should proceed by not assigning any values to the corresponding items, i.e., this is not an error.
Since the remaining values are not assigned a value, they will be :val:`null` if they are not assigned values by another response retrieved via a next link encountered before the final end-of-data-marker.
(Since there is no requirement that values are assigned in a specific order between responses, it is possible that the omitted values are already assigned.
In that case the values shall remain as assigned, i.e., they are not overwritten by :val:`null` in this situation.)

Examples
~~~~~~~~

Below follows an example of a dense response for a partial array data of integer values.
The request returns the first three items and provides the next-marker link to continue fetching data:

.. code:: jsonl

   {"optimade-partial-data": {"format": "1.2.0"}, "layout": "dense", "returned_ranges": [{"start": 10, "stop": 20, "step": 2}]}
   123
   345
   -12.6
   ["PARTIAL-DATA-NEXT", ["https://example.db.org/value4"]]

Below follows an example of a dense response for a list property as a partial array of multidimensional array values.
The item with index 10 in the original list is provided explicitly in the response and is the first one provided in the response since start=10.
The item with index 12 in the list, the second data item provided since start=10 and step=2, is not included only referenced.
The third provided item (index 14 in the original list) is only partially returned: it is a list of three items, the first and last are explicitly provided, the second one is only referenced.

.. code:: jsonl

   {"optimade-partial-data": {"format": "1.2.0"}, "layout": "dense", "returned_ranges": [{"start": 10, "stop": 20, "step": 2}]}
   [[10,20,21], [30,40,50]]
   ["PARTIAL-DATA-REF", ["https://example.db.org/value2"]]
   [[11, 110], ["PARTIAL-DATA-REF", ["https://example.db.org/value3"]], [550, 333]]
   ["PARTIAL-DATA-NEXT", ["https://example.db.org/value4"]]

Below follows an example of the sparse layout for multidimensional lists with three aggregated dimensions.
The underlying property value can be taken to be sparse data in lists in four dimensions of 10000 x 10000 x 10000 x N, where the innermost list is a non-sparse list of arbitrary length of numbers.
The only non-null items in the outer three dimensions are, say, [3,5,19], [30,15,9], and [42,54,17].
The response below communicates the first item explicitly; the second one by deferring the innermost list using a reference-marker; and the third item is not included in this response, but deferred to another page via a next-marker.

.. code:: jsonl

   {"optimade-partial-data": {"format": "1.2.0"}, "layout": "sparse"}
   [3,5,19,  [10,20,21,30]]
   [30,15,9, ["PARTIAL-DATA-REF", ["https://example.db.org/value1"]]]
   ["PARTIAL-DATA-NEXT", ["https://example.db.org/"]]

An example of the sparse layout for multidimensional lists with three aggregated dimensions and integer values:

.. code:: jsonl

   {"optimade-partial-data": {"format": "1.2.0"}, "layout": "sparse"}
   [3,5,19,  10]
   [30,15,9, 31]
   ["PARTIAL-DATA-NEXT", ["https://example.db.org/"]]

An example of the sparse layout for multidimensional lists with three aggregated dimensions and values that are multidimensional lists of integers of arbitrary lengths:

.. code:: jsonl

   {"optimade-partial-data": {"format": "1.2.0"}, "layout": "sparse"}
   [3,5,19, [ [10,20,21], [30,40,50] ] ]
   [3,7,19, ["PARTIAL-DATA-REF", ["https://example.db.org/value2"]]]
   [4,5,19, [ [11, 110], ["PARTIAL-DATA-REF", ["https://example.db.org/value3"]], [550, 333]]]
   ["PARTIAL-DATA-END", [""]]

Property Definition Example
---------------------------

This appendix provides a more complete example of a Property Definition in the format defined in `Property Definitions`_.
(Note: the description strings have been wrapped for readability only.)

.. code:: jsonc

  {
    "title": "Forces and atomic masses list",
    "$id": "https://properties.example.com/v1.2.0/forces_and_masses",
    "x-optimade-type": "list",
    "x-optimade-property": {
      "version": "1.2.0",
      "property-format": "1.2",
      "units": [
        {
          "title": "Newton",
          "symbol": "N",
          "$id": "https://units.example.com/v1.2.0/N",
          "description": "The newton SI unit of force, defined as 1 kg m/s^2
                          using the 2019 redefinition of the SI base units.",
          "standard": {
            "name": "gnu units",
            "version": "3.15",
            "symbol": "newton"
          },
          "defining-relation": {
            "base-units": [
              {
                "symbol": "kg",
                "id": "https://units.example.com/v1.2.0/kg"
              },
              {
                "symbol": "m",
                "id": "https://units.example.com/v1.2.0/m"
              },
              {
                "symbol": "s",
                "id": "https://units.example.com/v1.2.0/s"
              }
            ],
            "base-units-expression": "kg*m*s^-2"
          }
        },
        {
          "title": "Dalton mass unit",
          "symbol": "u",
          "$id": "https://units.example.com/v1.2.0/u",
          "description": "The dalton mass unit defined as 1/12 of the mass of an
                          unbound neutral atom of carbon-12 in its nuclear and
                          electronic ground state and at rest. Approximately
                          equal to $1.66053906660(50)*10^{-27}$ kg",
          "standard": {
            "name": "gnu units",
            "version": "3.15",
            "symbol": "atomicmassunit"
          }
        }
      ]
    },
    "type": ["array", "null"],
    "description": "A list of forces and atomic masses",
    "examples": [
      [{"force": 42.0, "mass": 28.0855}, {"force": 44.2, "mass": 15.9994}],
      [{"force": 12.0, "mass": 24.3050}]
    ],
    "x-optimade-unit": "inapplicable",
    "x-optimade-requirements": {
      "support": "should",
      "sortable": false,
      "query-support": "none"
    },
    "items": {
      "title": "Force and atomic mass pair",
      "x-optimade-type": "dictionary",
      "description": "A dictionary containing a force and mass value",
      "x-optimade-unit": "inapplicable",
      "type": ["object"],
      "properties": {
        "force": {
          "title": "Force",
          "description": "A force value",
          "x-optimade-type": "float",
          "x-optimade-unit": "N",
          "type": ["number"],
          "examples": [42.0]
        },
        "mass": {
          "title": "Mass",
          "description": "An atomic mass",
          "x-optimade-type": "float",
          "x-optimade-unit": "u",
          "type": ["number"],
          "examples": [15.9994]
        }
      }
    }
  }

OPTIMADE Regular Expression Format
----------------------------------
This section defines a Unicode string representation of regular expressions (regexes) to be referenced from other parts of the specification.
The format will be referred to as an "OPTIMADE regex".

Regexes are commonly embedded in a context where they need to be enclosed by delimiters (e.g., double quotes or slash characters).
If this is the case, some outer-level escape rules likely apply to allow the end delimiter to appear within the regex.
Such delimiters and escape rules are *not* included in the definition of the OPTIMADE regex format itself and need to be clarified when this format is referenced.
The format defined in this section applies after such outer escape rules have been applied (e.g., when all occurrences of ``\/`` have been translated into ``/`` for a format where an unescaped slash character is the end delimiter).
Likewise, if an OPTIMADE regex is embedded in a serialized data format (e.g., JSON), this section documents the format of the Unicode string resulting from the deserialization of that format.

An OPTIMADE regex is a regular expression that adheres to `ECMA-262, section 21.2.1 <https://262.ecma-international.org/11.0/#sec-patterns>`__ with additional restrictions described below which define a subset of the ECMA-262 format chosen to match features commonly available in different database backends.
The regex is interpreted according to the ECMA-262 processing rules that apply for an expression where only the Unicode variable is set to true of all variables set by the RegExp internal slot described by `ECMA-262, section 21.2.2.1 <https://262.ecma-international.org/11.0/#sec-notation>`__.

The subset includes only the following tokens and features:

- Individual Unicode characters matching themselves, as defined by the JSON specification (:RFC:`8259`).
- The ``.`` character to match any one Unicode character except the line break characters LINE FEED (LF) (U+000A), CARRAGE RETURN (U+000D), LINE SEPARATOR (U+2028), PARAGRAPH SEPARATOR (U+2029) (see `ECMA-262 section 2.2.2.7 <https://262.ecma-international.org/14.0/?_gl=1*yqtzjq*_ga*MjEzNTE2ODEyNi4xNzA0NTQ1NTk5*_ga_TDCK4DWEPP*MTcwNzk5ODA1My43LjEuMTcwNzk5OTYxNC4wLjAuMA..#sec-compileatom>`__).
- A literal escape of `one of the characters defined as syntax characters in the ECMA-262 standard <https://262.ecma-international.org/11.0/#prod-SyntaxCharacter>`__, i.e., the escape character (``\``) followed by one of the following characters ``^ $ \ . * + ? ( ) [ ] { } |`` to represent that literal character.
  No other characters can be escaped.
  (This rule prevents other escapes that are interpreted differently depending on regex flavor.)
- Simple character classes (e.g., ``[abc]``), complemented character classes (e.g. ``[^abc]``), and their ranged versions (e.g., ``[a-z]``, ``[^a-z]``) with the following constraints:

  * The character ``-`` designates ranges, unless it is the first or last character of the class in which case it represents a literal ``-`` character.
  * If the first character is ``^`` then the expression matches all characters *except* the ones specified by the class as defined by the characters that follows.
  * The characters ``\ [ ]`` can only appear escaped with a preceding backslash, e.g. ``\\`` designates that the class includes a literal ``\`` character.
    The other syntax characters may appear either escaped or unescaped to designate that the class includes them.
    (This rule prevents other escapes inside classes that are not the same across regex flavors and expressions that, in some flavors, are interpreted as nested classes.)
  * Except as specified above, all characters represent themselves literally (including syntax characters).
  * Characters that represent themselves literally can only appear at most once.
    (This rule prevents various kinds of extended character class syntax that differs between regex formats that assigns special meaning to duplicated characters such as POSIX character classes, e.g., ``[:alpha:]``, equivalence classes, e.g., ``[=a=]``, set constructs, e.g. ``[A--B]``, ``[A&&B]``, etc.).
- Simple quantifiers: ``+`` (one or more), ``*`` (zero or more), ``?`` (zero or one) that appear directly after a character, group, or character class.
  (This rule prevents expressions with special meaning in some regex flavors, e.g., ``+?`` and ``(?...)``.)
- The beginning-of-input (``^``) and end-of-input (``$``) anchors.
- Simple grouping (``(...)``) and alternation (``|``).

Note that lazy quantifiers (``+?``, ``*?``, ``??``) are *not* included, nor are range quantifiers (``{x}``, ``{x,y}``, ``{x,}``).
Furthermore, there is no support for escapes designating shorthand character classes as ``\`` and a letter or number, nor is there any way to represent a Unicode character by specifying a code point as a number, only via the Unicode character itself.
(However, the regex can be embedded in a context that defines such escapes, e.g., in serialized JSON a string containing the character ``\u`` followed by four hexadecimal digits is deserialized into the corresponding Unicode character.)

An OPTIMADE regex matches the string at any position unless it contains a leading beginning-of-input (``^``) or trailing end-of-input (``$``) anchor listed above, i.e., the anchors are not implicitly assumed.
For example, the OPTIMADE regex "es" matches "expression".

Regexes that utilize tokens and features beyond the designated subset are allowed to have an undefined behavior, i.e., they MAY match or not match *any* string or MAY produce an error.
Implementations that do not produce errors in this situation are RECOMMENDED to generate warnings if possible.

  Compatibility notes:

  * The subset is intended to be compatible with, but even further restricted than, the subset recommended in the JSON Schema standard, see `JSON Schema: A Media Type for Describing JSON Documents 2020-12, section 6.4 <https://json-schema.org/draft/2020-12/json-schema-core#section-6.4>`__.
    The compatibility with the JSON Schema standard is expressed here as "intended" since there is some room for interpretation of the precise features included in the recommendation given in that standard.

  * The definition tolerates (with undefined behavior) regexes that use tokens and features beyond the defined subset.
    Hence, a regex can be directly handed over to a backend implementation compatible with the subset without needing validation or translation.

  * Additional consideration of how the ``.`` character operates in relation to line breaks may be required for multiline text.
    If the regex is applied to strings containing only the LINE FEED (U+000A) character and none of the other Unicode line break characters, most regex backend implementations are compatible with the defined behavior.
    If the regex is applied to string data containing arbitrary combinations of Unicode line break characters and the right behavior cannot be achieved via environmental settings and regex options, implementations can consider a translation step where other line break characters are translated into LINE FEED in the text operated on.

  * Compatibility with different regex implementations may change depending on the environment, implementation programming language versions, and options and has to be verified by implementations.
    However, as a general guide, we have used third-party sources, e.g., the `Regular Expression Engine Comparison Chart <https://gist.github.com/CMCDragonkai/6c933f4a7d713ef712145c5eb94a1816>`__ to collect the following information for compatibility when operating on text using LINE FEED as the line break character:

    * `ECMAScript (also known as javascript) <https://262.ecma-international.org/>`__ and version 1 and 2 of `PCRE <https://www.pcre.org/>`__ are meant to be compatible by design when used with appropriate options.

    * The following regex formats appear generally compatible when operating in Unicode mode: `Perl <https://perldoc.perl.org/perlre>`__, `Python <https://docs.python.org/3/library/re.html>`__, `Ruby <https://ruby-doc.org/3.2.2/Regexp.html>`__, `Rust <https://docs.rs/regex/latest/regex/>`__, `Java <https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html>`__, `.NET <https://learn.microsoft.com/en-us/dotnet/standard/base-types/details-of-regular-expression-behavior>`__, `MySQL 8 <https://dev.mysql.com/doc/refman/8.0/en/regexp.html>`__, `MongoDB <https://www.mongodb.com/docs/manual/reference/operator/query/regex/>`__, `Oracle <https://docs.oracle.com/cd/B13789_01/appdev.101/b10795/adfns_re.htm>`__, `IBM Db2 <https://www.ibm.com/docs/en/db2/11.5?topic=reference-regular-expressions>`__, `Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html>`__, `DuckDB <https://duckdb.org/docs/sql/functions/patternmatching.html#regular-expressions>`__ (which uses the `re2 <https://github.com/google/re2/wiki/Syntax>`__ library).
    * SQLite supports regexes via libraries and thus can use a compatible format (e.g., PCRE2).
    * XML Schema appears to use a compatible regex format, except it is implicitly anchored: i.e., the beginning-of-input ``^`` and end-of-input ``$`` anchors must be removed, and missing anchors replaced by ``.*``.
    * POSIX Extended regexes (and their extended GNU implementations) are incompatible because ``\`` is not a special character in character classes.
      POSIX Basic regexes also have further differences, e.g., the meaning of some escaped syntax characters is reversed.
