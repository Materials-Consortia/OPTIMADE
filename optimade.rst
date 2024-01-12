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

..

    **Note**: A list of database providers acknowledged by the **Open Databases Integration for Materials Design** consortium is maintained externally from this specification and can be retrieved as described in section `Database-Provider-Specific Namespace Prefixes`_.
    This list is also machine-readable, optimizing the automatic discoverability.

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
Any custom entry listing endpoint MUST also be added to the :property:`available\_endpoints` and :property:`entry\_types\_by\_format` attributes of the `Base Info Endpoint`_.

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
- :query-url:`http://example.com/optimade/v1/structures?\_exmpl\_filter="elements all in [Al, Si, Ga]"`

    **Note**: the specification presently makes no attempt to standardize access control mechanisms.
    There are security concerns with access control based on URL tokens, and the above example is not to be taken as a recommendation for such a mechanism.

Entry Listing JSON Response Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"Entry listing" endpoint response dictionaries MUST have a :field:`data` key.
The value of this key MUST be a list containing dictionaries that represent individual entries.
In the default JSON response format every dictionary (`resource object <http://jsonapi.org/format/1.1/#document-resource-objects>`__) MUST have the following fields:

- **type**: field containing the Entry type as defined in section `Definition of Terms`_
- **id**: field containing the ID of entry as defined in section `Definition of Terms`_. This can be the local database ID.
- **attributes**: a dictionary, containing key-value pairs representing the entry's properties, except for `type` and `id`.

  Database-provider-specific properties need to include the database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

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

  - **available\_licenses**: List of `SPDX license identifiers <https://spdx.org/licenses/>` specifying a set of alternative licenses under which the client is granted access to all the data and metadata in this database.
    If the data and metadata is available under multiple alternative licenses, identifiers of these multiple licenses SHOULD be provided to let clients know under which conditions the data and metadata can be used.
    Inclusion of a license identifier in the list is a commitment of the database that the rights are in place to grant clients access to all the data and metadata according to the terms of either of these licenses (at the choice of the client).
    If the licensing information provided via the field :field:`license` omits licensing options specified in :field:`available_licenses`, or if it otherwise contradicts them, a client MUST still be allowed to interpret the inclusion of a license in :field:`available_licenses` as a full commitment from the database that the data and metadata is available, without exceptions, under the respective licenses.
    If the database cannot make that commitment, e.g., if only part of the data is available under a license, the corresponding license identifier MUST NOT appear in :field:`available_licenses` (but, rather, the field :field:`license` is to be used to clarify the licensing situation.)
    An empty list indicates that none of the SPDX licenses apply for the entirety of the database and that the licensing situation is clarified in human readable form in the field :field:`license`.

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

Example (note: the description strings have been wrapped for readability only):

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
            "title": "Unit cell lattice vectors",
            "x-optimade-type": "list",
            "type": ["array", "null"],
            "description": "The three lattice vectors in Cartesian coordinates, in ångström (Å).\n
            \n
            - MUST be a list of three vectors *a*, *b*, and *c*, where each of the vectors MUST BE a
              list of the vector's coordinates along the x, y, and z Cartesian coordinates.
            ",
            "examples": [
              [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 1.0, 4.0]]
            ],
            "x-optimade-unit": "inapplicable",
            "x-optimade-property": {
              "property-format": "1.2",
              "unit-definitions": [
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
              ]
            },
            "x-optimade-implementation": {
              "sortable": false,
              "query-support": "none"
            },
            "x-optimade-requirements": {
              "support": "should",
              "sortable": false,
              "query-support": "none"
            },
            "maxItems": 3,
            "minItems": 3,
            "items": {
              "type": "array",
              "x-optimade-type": "list",
              "x-optimade-unit": "inapplicable",
              "maxItems": 3,
              "minItems": 3,
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

A list of known providers can be retrieved as described in section `Database-Provider-Specific Namespace Prefixes`_.
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

-  :query-url:`http://example.org/optimade/v1/structures?filter=_exmpl_melting_point%3C300+AND+nelements=4+AND+chemical_formula_descriptive="SiO2"&response_format=xml`

Or, fully URL encoded :

-  :query-url:`http://example.org/optimade/v1/structures?filter=_exmpl_melting_point%3C300+AND+nelements%3D4+AND+chemical_formula_descriptive%3D%22SiO2%22&response_format=xml`

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

  Identifiers that start with an underscore are specific to a database provider, and MUST be on the format of a database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

  Examples:

  - :property:`_exmpl_formula_sum` (a property specific to that database)
  - :property:`_exmpl_band_gap`
  - :property:`_exmpl_supercell`
  - :property:`_exmpl_trajectory`
  - :property:`_exmpl_workflow_id`

- **Nested property names** A nested property name is composed of at least two identifiers separated by periods (``.``).

.. _string values:

- **String values** MUST be surrounded by double quote characters (`"`, ASCII symbol 34 dec, 0x22 hex).
  A double quote that is a part of the value, not a delimiter, MUST be escaped by prepending it with a backslash character (`\\`, ASCII symbol 92 dec, 0x5C hex).
  A backslash character that is part of the value (i.e., not used to escape a double quote) MUST be escaped by prepending it with another backslash.
  An example of an escaped string value, including the enclosing double quotes, is given below:

  - "A double quote character (\\", ASCII symbol 34 dec) MUST be prepended by a backslash (\\\\, ASCII symbol 92 dec) when it is a part of the value and not a delimiter; the backslash character \\"\\\\\\" itself MUST be preceded by another backslash, forming a double backslash: \\\\\\\\"

  (Note that at the end of the string value above the four final backslashes represent the two terminal backslashes in the value, and the final double quote is a terminator, it is not escaped.)

  String value tokens are also used to represent **timestamps** in form of the `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__.

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

-  :filter:`NOT a > b OR c = 100 AND f = "C2 H6"`: this is interpreted as :filter:`(NOT (a > b)) OR ( (c = 100) AND (f = "C2 H6") )` when fully braced.
-  :filter:`a >= 0 AND NOT b < c OR c = 0`: this is interpreted as :filter:`((a >= 0) AND (NOT (b < c))) OR (c = 0)` when fully braced.

Type handling and conversions in comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The definitions of specific properties in this standard define their types.
Similarly, for `database-provider-specific properties`_, the database provider decides their types.
In the syntactic constructs that can accommodate values of more than one type, types of all participating values are REQUIRED to match, with a single exception of timestamps (see below).
Different types of values MUST be reported as :http-error:`501 Not Implemented` errors, meaning that type conversion is not implemented in the specification.

As the filter language syntax does not define a lexical token for timestamps, values of this type are expressed using string tokens in `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__.
In a comparison with a timestamp property, a string token represents a timestamp value that would result from parsing the string according to RFC 3339 Internet Date/Time Format.
Interpretation failures MUST be reported with error :http-error:`400 Bad Request`.

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

A Property Definition MUST be composed according to the combination of the requirements in the subsection `Property Definition keys from JSON Schema`_ below and the following additional requirements:

**REQUIRED keys for the outermost level of the Property Definition:**

- :field:`$id`: String, :field:`title`: String, and :field:`description`: String.
  See the subsection `Property definition keys from JSON Schema`_ for the definitions of these fields.
  They are defined in that subsection as OPTIONAL on any level of the Property Definition, but are REQUIRED on the outermost level.

- :field:`x-optimade-property`: Dictionary.
  Additional information to define the property that is not covered by fields in the JSON Schema standard.

  **REQUIRED keys:**

  - :field:`property-format`: String.
    Specifies the minor version of the property definition format used.
    The string MUST be of the format "MAJOR.MINOR", referring to the version of the OPTIMADE standard that describes the format in which this property definition is expressed.
    The version number string MUST NOT be prefixed by, e.g., "v".
    In implementations of the present version of the standard, the value MUST be exactly :field-val:`1.2`.
    A client MUST disregard the property definition if the field is not a string of the format MAJOR.MINOR or if the MAJOR version number is unrecognized.
    This field allows future versions of this standard to support implementations keeping definitions that adhere to older versions of the property definition format.

  **OPTIONAL keys:**

  - :field:`version`: String.
    This string indicates the version of the property definition.
    The string SHOULD be in the format described by the `semantic versioning v2 <https://semver.org/spec/v2.0.0.html>`__ standard.

  - :field:`unit-definitions`: List.
    A list of definitions of the symbols used in the Property Definition (including its nested levels) for physical units given as values of the :field:`x-optimade-unit` field.
    This field MUST be included if the defined property, at any level, includes an :field:`x-optimade-unit` with a value that is not :val:`dimensionless` or :val:`inapplicable`.
    See subsection `Physical Units in Property Definitions`_ for the details on how units are represented in OPTIMADE Property Definitions and the precise format of this dictionary.

  - :field:`resource-uris`: List.
    A list of dictionaries that references remote resources that describe the property.
    The format of each dictionary is:

    **REQUIRED keys:**

    - :field:`relation`: String.
      A human-readable description of the relationship between the property and the remote resource, e.g., a "natural language description".

    - :field:`uri`: String.
      A URI of the external resource (which MAY be a resolvable URL).

**REQUIRED keys for all levels of the Property Definition:**

- :field:`x-optimade-type`: String
  Specifies the OPTIMADE data type for this level of the defined property.
  MUST be one of :val:`"string"`, :val:`"integer"`, :val:`"float"`, :val:`"boolean"`, :val:`"timestamp"`, :val:`"list"`, or :val:`"dictionary"`.

- :field:`x-optimade-unit`: String.
  A (compound) symbol for the physical unit in which the value of the defined property is given or one of the strings :val:`dimensionless` or :val:`inapplicable`.
  See subsection `Physical Units in Property Definitions`_ for the details on how compound units are represented in OPTIMADE Property Definitions and the precise format of this string.

**OPTIONAL keys at all nested levels of the Property Definition:**

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

  - :field:`query-support-operators`: List of Strings.
    Defines the filter language features supported on this property.
    Each string in the list MUST be one of :val:`<`, :val:`<=`, :val:`>`, :val:`>=`, :val:`=`, :val:`!=`, :val:`CONTAINS`, :val:`STARTS WITH`, :val:`ENDS WITH`:, :val:`HAS`, :val:`HAS ALL`, :val:`HAS ANY`, :val:`HAS ONLY`, :val:`IS KNOWN`, :val:`IS UNKNOWN` with the following meanings:

    - :val:`<`, :val:`<=`, :val:`>`, :val:`>=`, :val:`=`, :val:`!=`: indicating support for filtering this property using the respective operator.
      If the property is of Boolean type, support for :val:`=` also designates support for boolean comparisons with the property being true that omit ":filter-fragment:`= TRUE`", e.g., specifying that filtering for ":filter:`is_yellow = TRUE`" is supported also implies support for ":filter:`is_yellow`" (which means the same thing).
      Support for ":filter:`NOT is_yellow`" also follows.

    - :val:`CONTAINS`, :val:`STARTS WITH`, :val:`ENDS WITH`: indicating support for substring filtering of this property using the respective operator. MUST NOT appear if the property is not of type String.

    - :val:`HAS`, :val:`HAS ALL`, :val:`HAS ANY`: indicating support of the MANDATORY features for list property comparison using the respective operator. MUST NOT appear if the property is not of type List.

    - :val:`HAS ONLY`: indicating support for list property comparison with all or a subset of the OPTIONAL constructs using this operator. MUST NOT appear if the property is not of type List.

    - :val:`IS KNOWN`, :val:`IS UNKNOWN`: indicating support for filtering this property on unknown values using the respective operator.

- :field:`x-optimade-requirements`: Dictionary.
  A dictionary describing the level of OPTIMADE API functionality required by all implementations of this property.
  Omitting this field means the corresponding functionality is OPTIONAL.
  The dictionary has the same format as :field:`x-optimade-implementation`, except that it also allows the following OPTIONAL field:

  - :field:`support`: String.
    Describes the minimal required level of support for the Property by an implementation.
    This field SHOULD only appear in an :field:`x-optimade-requirements` that is at the outermost level of a Property Definition, as the meaning of its inclusion on other levels is not defined.
    The string MUST be one of the following:

    - :val:`must`: the defined property MUST be recognized by the implementation (e.g., in filter strings) and MUST NOT be :val:`null`.
    - :val:`should`: the defined property MUST be recognized by the implementation (e.g., in filter strings) and SHOULD NOT be :val:`null`.
    - :val:`may`: it is OPTIONAL for the implementation to recognize the defined property and it MAY be equal to :val:`null`.

    Omitting the field is equivalent to :val:`may`.

    Note: the specification by this field of whether the defined property can be :val:`null` or not MUST match the value of the :field:`type` field.
    If :val:`null` values are allowed, that field must be a list where the string :val:`"null"` is the second element.

Property Definition keys from JSON Schema
-----------------------------------------

In addition to the requirements on the format of a Property Definition in the previous section, it MUST also adhere to the OPTIONAL and REQUIRED keys described in this subsection.
The format described in this subsection forms a subset of the `JSON Schema Validation Draft 2020-12 <https://json-schema.org/draft/2020-12/json-schema-validation.html>`__ and `JSON Schema Core Draft 2020-12 <https://json-schema.org/draft/2020-12/json-schema-core.html>`__ standards.

**REQUIRED keys**

- :field:`type`: String or List.
  Specifies the corresponding JSON type for this level of the defined property and whether the property can be :val:`null` or not.
  The value is directly correlated with :field:`x-optimade-type` as explained below.

  It MUST be one of:

  - A string correlated with :field:`x-optimade-type` as follows.
    If :field:`x-optimade-type` is:

    * :val:`"boolean"`, `"string"`, or `"integer"` then :field:`type` is the same string.
    * :val:`"dictionary"` then :field:`type` is `"object"`.
    * :val:`"list"` then :field:`type` is `"array"`.
    * :val:`"float"` then :field:`type` is `"number"`.
    * :val:`"timestamp"` then :field:`type` is `"string"`.

  - A list where the first item MUST be the string described above (correlated to the field :field:`x-optimade-type` in the same way) and the second item MUST be the string :val:`"null"`.
    This form specifies that the defined property can be :val:`null`.

..

  Implementation notes:

    - The field :field:`type` can be derived from the field :field:`x-optimade-type` and its role is only to provide the JSON type names corresponding to :field:`x-optimade-type`.
      The motivation to include these type names is that it makes the JSON representation of a Property Definition a fully valid standard JSON Schema.
      Nevertheless, for consistency across formats, these JSON type names MUST still be included when a property definition is represented in other output formats (i.e., the JSON names MUST NOT be translated into the type names of that output format).

    - The allowed values of the :field:`type` field are highly restricted compared to what is permitted using the full JSON Schema standard.
      Values can only be defined to be a single OPTIMADE data type or, optionally, :val:`null`.
      This restriction is intended to reduce the complexity of possible data types that implementations have to handle in different formats and database backends.

**OPTIONAL keys**

- :field:`$id`: String.
  A static URI identifier that is a URN or URL representing the specific version of this level of the defined property.
  It SHOULD NOT be changed as long as the property definition remains the same, and SHOULD be changed when the property definition changes.
  (If it is a URL, clients SHOULD NOT assign any interpretation to the response when resolving that URL.)

- :field:`title`: String.
  A short single-line human-readable explanation of the defined property appropriate to show as part of a user interface.

- :field:`description`: String.
  A human-readable multi-line description that explains the purpose, requirements, and conventions of the defined property.
  The format SHOULD be a one-line description, followed by a new paragraph (two newlines), followed by a more detailed description of all the requirements and conventions of the defined property.
  Formatting in the text SHOULD use Markdown in the `CommonMark v0.3 format <https://spec.commonmark.org/0.30/>`__.

- :field:`deprecated`: Boolean.
  If :val:`TRUE`, implementations SHOULD not use the defined property, and it MAY be removed in the future.
  If :val:`FALSE`, the defined property is not deprecated.
  The field not being present means :val:`FALSE`.

- :field:`enum`: List.
  The defined property MUST take one of the values given in the provided list.
  The items in the list MUST all be of a data type that matches the :field:`type` field and otherwise adhere to the rest of the Property Description.
  If this key is given, for :val:`null` to be a valid value of the defined property, the list MUST contain a :val:`null` value and the :field:`type` MUST be a list where the second value is the string :val:`"null"`.

- :field:`examples`: List.
  A list of example values that the defined property can have.
  These examples MUST all be of a data type that matches the :field:`type` field and otherwise adhere to the rest of the Property Description.

Depending on what string the :field:`type` is equal to, or contains as first element, the following additional requirements also apply:

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

  - :field:`maxItems`: Integer.
    A non-negative integer.
    The defined property is an array that MUST contain a number of items that is less than or equal to the given integer.

  - :field:`minItems`: Integer.
    A non-negative integer.
    The defined property is an array that MUST contain a number of items that is greater than or equal to the given integer.

  - :field:`uniqueItems`: Boolean.
    If :val:`TRUE`, the defined property is an array that MUST only contain unique items.
    If :val:`FALSE`, this field sets no limitation on the defined property.

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
    - :val:`"uri"`: a string instance is valid against this attribute if it is a valid URI, according to :RFC:`3986`.

Physical Units in Property Definitions
--------------------------------------

In OPTIMADE, there is no facility to allow a property to be represented in a choice of units, e.g., either ångström (Å) or meter (m).
The unit is always permanently fixed by the Property Definition.
Clients and servers that use other units internally thus have to do unit conversions as part of preparing and processing OPTIMADE responses.

The physical unit of a property, the embedded items of a list, or values of a dictionary, are defined with the field :field:`x-optimade-unit` with the following requirements:

- The field MUST be given with a non-:val:`null` value both at the highest level in the OPTIMADE Property Definition and all inner Property Definitions.
- If the property refers to a physical quantity that is dimensionless (often also referred to as having the dimension 1) or refers to a dimensionless count of something (e.g., the number of protons in a nucleus) the field MUST have the value :val:`dimensionless`.
- If the property refers to an entity for which the assignment of a unit would not make sense, e.g., a string representing a chemical formula or a serial number the field MUST have the value :val:`inapplicable`.

A standard set of unit symbols for OPTIMADE is taken from version 3.15 of the (separately versioned) unit database :val:`definitions.units` included with the `source distribution <http://ftp.gnu.org/gnu/units/>`__ of `GNU Units <https://www.gnu.org/software/units/>`__ version 2.22.
If the unit is available in this database, or if it can be expressed as a compound unit expression using these units, the value of :field:`x-optimade-unit` SHOULD use the corresponding (compound) string symbol and a corresponding definition referring to the same symbol be given in the field :field:`standard`.

A compound unit expression based on the GNU Units symbols is created by a sequence of unit symbols separated by a single multiplication :val:`*` symbol.
Each unit symbol can also be suffixed by a single :val:`^` symbol followed by a positive or negative integer to indicate the power of the preceding unit, e.g., :val:`m^3` for cubic meter, :val:`m^-3` for inverse cubic meter.
(Positive integers MUST NOT be preceded by a plus sign.)
The unit symbols MAY be prefixed by one (but not more than one) of the prefixes defined in the ``definitions.units`` file.
A prefix is indicated in the file by a trailing ``-``, but that trailing character MUST NOT be included when using it as a prefix.
If there are multiple prefixes in the file with the same meaning, an implementation SHOULD use the *shortest one* consisting of only lowercase letters a-z and underscores, but no other symbols.
If there are multiple ones with the same shortest length, then the first one of those SHOULD be used.
For example :val:`"km"` for kilometers.
Furthermore:

- No whitespace, parenthesis, or other symbols than specified above are permitted.
- If multiple string representations of the same unit exist in ``definitions.units``, the *first one* in that file consisting of only lowercase letters a-z and underscores, but no other symbols, SHOULD be used.
- The unit symbols MUST appear in alphabetical order.

The string in :field:`x-optimade-unit` MUST be defined in the :field:`unit-definitions` field inside the :field:`x-optimade-property` field in the outermost level of the Property Definition.

If provided, the :field:`unit-definitions` in :field:`x-optimade-property` MUST be a list of dictionaries, all adhering to the following format:

**REQUIRED keys:**

- :field:`symbol`: String.
  Specifies the symbol to be used in :field:`x-optimade-unit` to reference this unit.

- :field:`title`: String.
  A human-readable single-line string name for the unit.

- :field:`description`: String.
  A human-readable multiple-line detailed description of the unit.

- :field:`standard`: Dictionary.
  This field is used to define the unit symbol using a preexisting standard.
  The dictionary has the following format:

  **REQUIRED keys:**

  - :field:`name`: String.
    The abbreviated name of the standard being referenced.
    One of the following:

    - :val:`"gnu units"`: the symbol is a (compound) unit expression based on the symbols in the file ``definitions.units`` distributed with `GNU Units software <https://www.gnu.org/software/units/>`__, created according to the scheme described above.
    - :val:`"ucum"`: the symbol comes from `The Unified Code for Units of Measure <https://unitsofmeasure.org/ucum.html>`__ (UCUM) standard.
    - :val:`"qudt"`: the symbol comes from the `QUDT <http://qudt.org/>`__ standard.
      Not only symbols strictly defined within the standard are allowed, but also other compound unit expressions created according to the scheme for how new such symbols are formed in this standard.

  - :field:`version`: String.
    The version string of the referenced standard.

  - :field:`symbol`: String.
    The symbol to use from the referenced standard, expressed according to that standard.
    This field MAY be different from :field:`symbol` directly under :field:`unit-definitions`, meaning that the unit is referenced in :field:`x-optimade-unit` fields using a different symbol than the one used in the standard.
    However, the :field:`symbol` fields SHOULD be the same unless multiple units sharing the same symbol need to be referenced.


**OPTIONAL keys:**

- :field:`resource-uris`: List.
  A list of dictionaries that reference remote resources that describe the unit.
  The format of each dictionary is:

  **REQUIRED keys:**

  - :field:`relation`: String.
    A human-readable description of the relationship between the unit and the remote resource, e.g., a "natural language description".

  - :field:`uri`: String.
    A URI of the external resource (which MAY be a resolvable URL).

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
  - The entry of type `<type>` and ID `<id>` MUST be returned in response to a request for :endpoint:`/<type>/<id>` under the versioned or unversioned base URL serving the API.

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

database-provider-specific properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: Database providers are allowed to add database-provider-specific properties in the output of both standard entry types and database-provider-specific entry types.
  Similarly, an implementation MAY add keys with a database-provider-specific prefix to dictionary properties and their sub-dictionaries.
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
  - These MUST be prefixed by a database-provider-specific prefix (see appendix `Database-Provider-Specific Namespace Prefixes`_).
  - Implementations MUST add the properties to the list of :property:`properties` under the respective entry listing :endpoint:`info` endpoint (see `Entry Listing Info Endpoints`_).

- **Examples**: A few examples of valid database-provided-specific property names follows:

  - :property:`_exmpl_formula_sum`
  - :property:`_exmpl_band_gap`
  - :property:`_exmpl_supercell`
  - :property:`_exmpl_trajectory`
  - :property:`_exmpl_workflow_id`
