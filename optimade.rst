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
