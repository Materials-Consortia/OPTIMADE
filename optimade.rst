==========================================
OPTiMaDe API specification v0.10.1-develop
==========================================

.. comment

   This document uses RST text roles on (almost) all literals to specify the context to which each literal belongs.
   This markup enables nicer formatting (e.g., HTML output can be formatted using CSS), as well as automated spell checks and testing.
   Below follows the definitions of the text roles used:

     # Filtering

     filter : full OPTiMaDe filter strings
     filter-fragment : segments of filter strings, or filter strings that uses, e.g., "..."
                       so they would not pass a validation.
     filter-op : operators and keywords in the filtering language
     ere : regex on ere form
     pcre : regex on pcre form

     # OPTiMaDe concepts

     entry : names of type of resources served via OPTiMaDe pertaining to data in a database.
     property : data item that pertains to an entry.
     val : value examples that properties can be.
           :val: is ONLY used when referencing values of actual properties, i.e., information that pertains to the database.

     # URL queries

     endpoint : specification of endpoints and endpoint names.
     query-param : URL query parameter names.
     query-string : strings that represent segments of URL query strings, with query parameters and values.
     query-url : full URLs, or relative starting with a '/' of URL queries.

     # HTTP

     http-header : an HTTP header name, or header + value.
     http-error : an HTTP error on form <number> <english text>.

     # Responses

     json : examples of JSON output.
     field : keys in key-value dictionaries in responses.
     field-val : value examples that fields can be set to.
                 Note that `null` sometimes refer to the OPTiMaDe concept of :val:`null`, and sometimes to the javascript constant :field-val:`null`, and the markup distinguishes these two cases.
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

The API specification described in this document builds on top of the `JSON API v1.0 specification <http://jsonapi.org/format/1.0>`__.
In particular, the JSON API specification is assumed to apply wherever it is stricter than what is formulated in this document.
Exceptions to this rule are stated explicitly (e.g. non-compliant responses are tolerated if a non-standard response format is explicitly requested).

Definition of Terms
===================

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in :RFC:`2119`.

**Database provider**
    A service that provides one or more databases with data desired to be made available using the OPTiMaDe API.

**Database-provider-specific prefix**
    Every database provider is designated a unique prefix.
    The prefix is used to separate the namespaces used by provider-specific extensions.
    The list of presently defined prefixes is maintained externally from this specification.
    For more information, see section `Database-Provider-Specific Namespace Prefixes`_.

**API implementation**
    A realization of the OPTiMaDe API that a database provider uses to serve data from one or more databases.

**Identifier**
    Names that MUST start with a lowercase letter ([a-z]) or an underscore ("\_") followed by any number of lowercase alphanumerics ([a-z0-9]) and underscores ("\_").

**Entry**
    A single instance of a specific type of resource served by the API implementation.
    For example, a :entry:`structures` entry is comprised by data that pertain to a single structure.

**Entry type**
    Entries are categorized into types, e.g., :entry:`structures`, :entry:`calculations`, :entry:`references`.
    Entry types MUST be named according to the rules for identifiers.

**Entry property**
    One data item which pertains to an entry, e.g., the chemical formula of a structure.

**Entry property name**
    The name of an entry property.
    Entry property names MUST follow the rules for identifiers and MUST NOT have the same name as any of the entry types.

**Relationship**
    Any entry can have one or more relationships with other entries.
    These are described in section `Relationships`_.
    Relationships describe links between entries rather than data that pertain to a single entry, and are thus regarded as distinct from the entry properties.

**Query filter**
    An expression used to influence the entries returned in the response to an URL query.
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

Base URL
--------

Each database provider will publish one or more base URL that serves the API.
An example could be: http://example.com/optimade/.
Every URL component that follows the base URL MUST behave as standardized in this API specification.

The client MAY include a version number in the base URL, prefixed with the letter "v", where the version number indicates the version of the API standard that the client requests.
The format is either vMAJOR or vMAJOR.MINOR where MAJOR is the major version number, and MINOR is the minor version number of the standard being referenced.
If the major version is 0, the minor version MUST also be included.
The database provider MAY support further levels of versioning separated from the major and minor version by a decimal point, e.g., patch version on the format vMAJOR.MINOR.PATCH. However, the client MUST NOT assume levels beyond the minor version are supported.

If the client does not include a version number in the base URL, the request is for the latest version of this standard that the database provider implements.
A query that includes a major and/or minor version is for the latest subversion of that major and/or minor version that the database provider implements.

A database provider MAY choose to only support a subset of possible versions.
The client can find out which versions are supported using the :field:`available_api_versions` field of the :field:`attributes` field from a query to the base URL :endpoint:`info` endpoint (see section `Base URL Info Endpoint`_).
The database provider SHOULD strive to implement the latest subversion of any major and minor version supported.
Specifically, the latest version of this standard SHOULD be supported.

Examples of valid base URLs:

- http://example.com/optimade/
- http://example.com/optimade/v0.9/
- http://example.com/
- http://example.com/some/path/

Examples of invalid base URLs:

- http://example.com/optimade/v0/
- http://example.com/optimade/0.9/

Note: The OPTiMaDe standard specifies the response from a number of endpoints under the base URLs.
However, the base URLs themselves are not considered to be a part of the API.
Hence, they are fully under the control of the API implementation.
It is RECOMMENDED that the implementation serves a human-readable HTML document on each base URL, and this document is used to explain that the URL is an OPTiMaDe base URL meant to be queried by an OPTiMaDe client.

Index Meta-Database
-------------------

A database provider MAY publish a special Index Meta-Database base URL. The main purpose of this base URL is to allow for automatic discoverability of all databases of the provider. Thus, it acts as a meta-database for the database provider's implementation(s).

The index meta-database MUST only provide the :endpoint:`info` and :endpoint:`links` endpoints, see sections `Info Endpoints`_ and `Links Endpoint`_.
It MUST NOT expose any entry listing endpoints (e.g., :endpoint:`structures`).

These endpoints do not need to be queryable, i.e., they MAY be provided as static JSON files.
However, they MUST return the correct and updated information on all currently provided implementations.

The :field:`index_base_url` field MUST be included in every response in the :field:`provider` field under the top-level :field:`meta` field (see section `JSON Response Schema: Common Fields`_).

The :field:`is_index` field under :field:`attributes` as well as the :field:`relationships` field, MUST be included in the :endpoint:`info` endpoint for the index meta-database (see section `Base URL Info Endpoint`_).
The value for :field:`is_index` MUST be :field-val:`true`.

    **Note**: A list of database providers acknowledged by the **Open Databases Integration for Materials Design** consortium is maintained externally from this specification and can be retrieved as described in section `Database-Provider-Specific Namespace Prefixes`_.
    This list is also machine-readable, optimizing the automatic discoverability.

Database-Provider-Specific Namespace Prefixes
---------------------------------------------

This standard refers to database-provider-specific prefixes and database providers.

A list of known providers and their assigned prefixes is published in the form of a statically hosted OPTiMaDe Index Meta-Database with base URL `https://www.optimade.org/providers/ <https://www.optimade.org/providers/>`__.
Visiting this URL in a web browser gives a human-readable description of how to retrieve the information in the form of a JSON file, and specifies the procedure for registration of new prefixes.

API implementations SHOULD NOT make up and use new prefixes without first getting them registered in the official list.

**Examples**: A database-provider-specific prefix: ``exmpl``. Used as a field name in a response: :field:`_exmpl_custom_field`.

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

In the default response format, relationships are encoded as `JSON API Relationships <https://jsonapi.org/format/1.0/#document-resource-object-relationships>`__, see section `Entry Listing JSON Response Schema`_.

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

The rationale for treating properties from other databases as unknown rather than triggering an error is for OPTiMaDe to support queries using database-specific properties that can be sent to multiple databases.

For example, the following query can be sent to API implementations `exmpl1` and `exmpl2` without generating any errors:

:filter:`filter=_exmpl1_bandgap<2.0 OR _exmpl2_bandgap<2.5`

Responses
=========

Response Format
---------------

This section defines a JSON response format that complies with the `JSON API v1.0 <http://jsonapi.org/format/1.0>`__ specification.
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

Every response SHOULD contain the following fields, and MUST contain at least one:

- **meta**: a `JSON API meta member <https://jsonapi.org/format/1.0/#document-meta>`__ that contains JSON API meta objects of non-standard meta-information.
  It MUST be a dictionary with these fields:

  - **query**: information on the query that was requested.
    It MUST be a dictionary with these fields:

    - **representation**: a string with the part of the URL following the base URL.

  - **api\_version**: a string containing the version of the API implementation.
  - **time\_stamp**: a timestamp containing the date and time at which the query was executed.
  - **data\_returned**: an integer containing the total number of data resource objects returned for the current :query-param:`filter` query, independent of pagination.
  - **more\_data\_available**: :field-val:`false` if all data resource objects for this :query-param:`filter` query have been returned in the response or if it is the last page of a paginated response, and :field-val:`true` otherwise.
  - **provider**: information on the database provider of the implementation.
    It MUST be a dictionary with these fields:

    - **name**: a short name for the database provider.
    - **description**: a longer description of the database provider.
    - **prefix**: database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

    :field:`provider` MAY include these fields:

    - **homepage**: a `JSON API links object <http://jsonapi.org/format/1.0/#document-links>`__, pointing to the homepage of the database provider, either directly as a string, or as a link object which can contain the following fields:

      - **href**: a string containing the homepage URL.
      - **meta**: a meta object containing non-standard meta-information about the database provider's homepage.

    - **index\_base\_url**: a `JSON API links object <http://jsonapi.org/format/1.0/#document-links>`__ pointing to the base URL for the index meta-database of the provider as specified in the list of providers (see section `Database-Provider-Specific Namespace Prefixes`_).
      It is specified either directly as a string, or as a link object, which can contain the following fields:

      - **href**: a string containing the base URL for the database provider's index meta-database.
      - **meta**: a meta object containing non-standard meta-information about this link.

      If the index meta-database (see section `Index Meta-Database`_) is implemented by the provider, the :field:`index_base_url` field MUST be included.

  :field:`meta` MAY also include these fields:

  - **data\_available**: an integer containing the total number of data resource objects available in the database for the endpoint.
  - **last\_id**: a string containing the last ID returned.
  - **response\_message**: response string from the server.
  - **implementation**: a dictionary describing the server implementation, containing the OPTIONAL fields:

    - **name**: name of the implementation.
    - **version**: version string of the current implementation.
    - **source\_url**: URL of the implementation source, either downloadable archive or version control system.
    - **maintainer**: a dictionary providing details about the maintainer of the implementation, MUST contain the single field:

      - **email** with the maintainer's email address.

  - **warnings**: a list of warning resource objects representing non-critical errors or warnings.
    A warning resource object is defined similarly to a `JSON API error object <http://jsonapi.org/format/1.0/#error-objects>`__, but MUST also include the field :field:`type`, which MUST have the value :field-val:`"warning"`.
    The field :field:`detail` MUST be present and SHOULD contain a non-critical message, e.g., reporting unrecognized search attributes or deprecated features.
    The field :field:`status`, representing a HTTP response status code, MUST NOT be present for a warning resource object.
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

    **Note**: warning :field:`id`\ s MUST NOT be trusted to identify the exceptional situations (i.e., they are not error codes, use instead the field :field:`code` for this.
    Warning :field:`id`\ s can *only* be trusted to be unique in the list of warning resource objects, i.e., together with the :field:`type`.

    General OPTiMaDe warning codes are specified in section `Warnings`_.

  - Other OPTIONAL additional information *global to the query* that is not specified in this document, MUST start with a database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

  - Example for a request made to :query-url:`http://example.com/optimade/v0.9/structures/?filter=a=1 AND b=2`:

    .. code:: jsonc

       {
	 "meta": {
	   "query": {
	     "representation": "/structures/?filter=a=1 AND b=2",
	   },
	   "api_version": "v0.9",
	   "time_stamp": "2007-04-05T14:30Z",
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
	     }
	   }
	 }
	 // ...
       }

- **data**: The schema of this value varies by endpoint, it can be either a *single* `JSON API resource object <http://jsonapi.org/format/1.0/#document-resource-objects>`__ or a *list* of JSON API resource objects.
  Every resource object needs the :field:`type` and :field:`id` fields, and its attributes (described in section `API Endpoints`_) need to be in a dictionary corresponding to the :field:`attributes` field.

The response MAY also return resources related to the primary data in the field:

- **links**: `JSON API links <http://jsonapi.org/format/1.0/#document-links>`__ is MANDATORY for implementing pagination.
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
            "href": "http://example.com/optimade/v0.9/",
            "meta": {
              "_exmpl_db_version": "3.2.1"
            }
          }
          // ...
        }
        // ...
      }

  The following fields are REQUIRED for implementing pagination:

  - **next**: represents a link to fetch the next set of results.
    When the current response is the last page of data, this field MUST be either omitted or :field-val:`null`\ -valued.

  An implementation MAY also use the following reserved fields for pagination.
  They represent links in a similar way as for :field:`next`.

  - **prev**: the previous page of data. :field-val:`null` or omitted when the current response is the first page of data.
  - **last**: the last page of data.
  - **first**: the first page of data.

- **included**: a list of `JSON API resource objects <http://jsonapi.org/format/1.0/#document-resource-objects>`__ related to the primary data contained in :field:`data`.
  Responses that contain related resources under :field:`included` are known as `compound documents <https://jsonapi.org/format/1.0/#document-compound-documents>`__ in the JSON API.

  The definition of this field is found in the `JSON API specification <http://jsonapi.org/format/1.0/#fetching-includes>`__.
  Specifically, if the query parameter :query-param:`include` is included in the request, :field:`included` MUST NOT include unrequested resource objects.
  For further information on the parameter :query-param:`include`, see section `Entry Listing URL Query Parameters`_.

  This value MUST be either an empty array or an array of related resource objects.

If there were errors in producing the response all other fields MAY be present, but the top-level :field:`data` field MUST be skipped, and the following field MUST be present:

- **errors**: a list of `JSON API error objects <http://jsonapi.org/format/1.0/#error-objects>`__, where the field :field:`detail` MUST be present.
  All other fields are OPTIONAL.

An example of a full response:

.. code:: jsonc

     {
       "links": {
	 "next": null,
	 "base_url": {
	   "href": "http://example.com/optimade/v0.9/",
	   "meta": {
	      "_exmpl_db_version": "3.2.1"
	   }
	 }
       },
       "meta": {
	 "query": {
	   "representation": "/structures?filter=a=1 AND b=2"
	 },
	 "api_version": "v0.9",
	 "time_stamp": "2007-04-05T14:30Z",
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
	   },
	   "index_base_url": "http://example.com/optimade"
	 },
	 "response_message": "OK"
	 // <OPTIONAL implementation- or database-provider-specific metadata, global to the query>
       },
       "data": [
	 // ...
       ],
       "included": [
	 // ...
       ],
     }

HTTP Response Status Codes
--------------------------

All HTTP response status codes MUST conform to `RFC 7231: HTTP Semantics <http://tools.ietf.org/html/rfc7231>`__.
The code registry is maintained by IANA and can be found `here <http://www.iana.org/assignments/http-status-codes>`__.

See also the JSON API definitions of responses when `fetching <https://jsonapi.org/format/1.0/#fetching>`__ data, i.e., sending a HTTP GET request.

**Important**: If a client receives an unexpected 404 error when making a query to a base URL, and is aware of the index meta-database that belongs to the database provider (as described in section `Index Meta-Database`_), the next course of action SHOULD be to fetch the resource objects under the :endpoint:`links` endpoint of the index meta-database and redirect the original query to the corresponding database ID that was originally queried, using the object's :field:`base_url` value.

HTTP Response Headers
---------------------

There are relevant use-cases for allowing data served via OPTiMaDe to be accessed from in-browser JavaScript, e.g. to enable server-less data aggregation.
For such use, many browsers need the server to include the header :http-header:`Access-Control-Allow-Origin: *` in its responses, which indicates that in-browser JavaScript access is allowed from any site.

Warnings
--------

Non-critical exceptional situations occurring in the implementation SHOULD be reported to the referrer as warnings.
Warnings MUST be expressed as a human-readable message, OPTIONALLY coupled with a warning code.

Warning codes starting with an alphanumeric character are reserved for general OPTiMaDe error codes (currently, none are specified).
For implementation-specific warnings, they MUST start with ``_`` and the database-provider-specific prefix of the implementation (see section `Database-Provider-Specific Namespace Prefixes`_).

API Endpoints
=============

The URL component that follows the base URL MUST represent one of the following endpoints:

- an "entry listing" endpoint
- a "single entry" endpoint
- an introspection :endpoint:`info` endpoint
- an "entry listing" introspection :endpoint:`info` endpoint
- a :endpoint:`links` endpoint to discover related implementations
- a custom :endpoint:`extensions` endpoint prefix

These endpoints are documented below.

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
   One can think of these properties as consituting a default value for :query-param:`response_fields` when that parameter is omitted.

3. Properties not marked as REQUIRED in any case, MUST be included only if explicitly requested in the query parameter :query-param:`response_fields`.
   Otherwise they SHOULD NOT be included.

Examples of valid entry listing endpoint URLs:

- http://example.com/optimade/v0.9/structures
- http://example.com/optimade/calculations

There MAY be multiple entry listing endpoints, depending on how many types of entries an implementation provides.
Specific standard entry types are specified in section `Entry list`_.
The API implementation MAY provide other entry types than the ones standardized in this specification, but such entry types MUST be prefixed by a database-provider-specific prefix.

Entry Listing URL Query Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The client MAY provide a set of URL query parameters in order to alter the response and provide usage information. While these URL query parameters are OPTIONAL for clients, API implementations MUST accept and handle them.
To adhere to the requirement on implementation-specific URL query parameters of `JSON API v1.0 <http://jsonapi.org/format/1.0>`__, query parameters that are not standardized by that specification have been given names that consist of at least two words separated by an underscore (a LOW LINE character '\_').

Standard OPTIONAL URL query parameters standardized by the JSON API specification:

- **filter**: a filter string, in the format described below in section `API Filtering Format Specification`_.

- **page\_limit**: sets a numerical limit on the number of entries returned.
  See `JSON API 1.0 <https://jsonapi.org/format/1.0/#fetching-pagination>`__.
  The API implementation MUST return no more than the number specified.
  It MAY return fewer.
  The database MAY have a maximum limit and not accept larger numbers (in which case an error code -- 403 Forbidden -- MUST be returned).
  The default limit value is up to the API implementation to decide.

Example: http://example.com/optimade/v0.9/structures?page_limit=100

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

- **sort**: If supporting sortable queries, an implementation MUST use the :query-param:`sort` query parameter with format as specified by `JSON API 1.0 <https://jsonapi.org/format/1.0/#fetching-sorting>`__.

  An implementation MAY support multiple sort fields for a single query.
  If it does, it again MUST conform to the JSON API 1.0 specification.

  If an implementation supports sorting for an `entry listing endpoint <Entry Listing Endpoints_>`_, then the :endpoint:`/info/<entries>` endpoint MUST include, for each field name :field:`<fieldname>` in its :field:`data.properties.<fieldname>` response value that can be used for sorting, the key :field:`sortable` with value :field-val:`true`.
  If a field name under an entry listing endpoint supporting sorting cannot be used for sorting, the server MUST either leave out the :field:`sortable` key or set it equal to :field-val:`false` for the specific field name.
  The set of field names, with :field:`sortable` equal to :field-val:`true` are allowed to be used in the "sort fields" list according to its definition in the JSON API 1.0 specification.
  The field :field:`sortable` is in addition to each property description (and the OPTIONAL field :field:`unit`).
  An example is shown in section `Entry Listing Info Endpoints`_.

- **include**: A server MAY implement the JSON API concept of returning `compound documents <https://jsonapi.org/format/1.0/#document-compound-documents>`__ by utilizing the :query-param:`include` query parameter as specified by `JSON API 1.0 <https://jsonapi.org/format/1.0/#fetching-includes>`__.

  All related resource objects MUST be returned as part of an array value for the top-level :field:`included` field, see section `JSON Response Schema: Common Fields`_.

  The value of :query-param:`include` MUST be a comma-separated list of "relationship paths", as defined in the `JSON API <https://jsonapi.org/format/1.0/#fetching-includes>`__.
  If relationship paths are not supported, or a server is unable to identify a relationship path a :http-error:`400 Bad Request` response MUST be made.

  The **default value** for :query-param:`include` is :query-val:`references`.
  This means :entry:`references` entries MUST always be included under the top-level field :field:`included` as default, since a server assumes if :query-param:`include` is not specified by a client in the request, it is still specified as :query-string:`include=references`.
  Note, if a client explicitly specifies :query-param:`include` and leaves out :query-val:`references`, :entry:`references` resource objects MUST NOT be included under the top-level field :field:`included`, as per the definition of :field:`included`, see section `JSON Response Schema: Common Fields`_.

    **Note**: A query with the parameter :query-param:`include` set to the empty string means no related resource objects are to be returned under the top-level field :field:`included`.

Standard OPTIONAL URL query parameters not in the JSON API specification:

- **response\_format**: the output format requested (see section `Response Format`_).
  Defaults to the format string 'json', which specifies the standard output format described in this specification.
  Example: http://example.com/optimade/v0.9/structures?response_format=xml
- **email\_address**: an email address of the user making the request.
  The email SHOULD be that of a person and not an automatic system.
  Example: http://example.com/optimade/v0.9/structures?email_address=user@example.com
- **response\_fields**: a comma-delimited set of fields to be provided in the output.
  If provided, these fields MUST be returned along with the REQUIRED fields.
  Other OPTIONAL fields MUST NOT be returned when this parameter is present.
  Example: http://example.com/optimade/v0.9/structures?response_fields=last_modified,nsites

Additional OPTIONAL URL query parameters not described above are not considered to be part of this standard, and are instead considered to be "custom URL query parameters".
These custom URL query parameters MUST be of the format "<database-provider-specific prefix><url\_query\_parameter\_name>".
These names adhere to the requirements on implementation-specific query parameters of `JSON API v1.0 <http://jsonapi.org/format/1.0>`__ since the database-provider-specific prefixes contain at least two underscores (a LOW LINE character '\_').

Example uses of custom URL query parameters include providing an access token for the request, to tell the database to increase verbosity in error output, or providing a database-specific extended searching format.

Examples:

- :query-url:`http://example.com/optimade/v0.9/structures?_exmpl_key=A3242DSFJFEJE`
- :query-url:`http://example.com/optimade/v0.9/structures?_exmpl_warning_verbosity=10`
- :query-url:`http://example.com/optimade/v0.9/structures?\_exmpl\_filter="elements all in [Al, Si, Ga]"`

    **Note**: the specification presently makes no attempt to standardize access control mechanisms.
    There are security concerns with access control based on URL tokens, and the above example is not to be taken as a recommendation for such a mechanism.

Entry Listing JSON Response Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"Entry listing" endpoint response dictionaries MUST have a :field:`data` key.
The value of this key MUST be a list containing dictionaries that represent individual entries.
In the default JSON response format every dictionary (`resource object <http://jsonapi.org/format/1.0/#document-resource-objects>`__) MUST have the following fields:

- **type**: field containing the Entry type as defined in section `Definition of Terms`_
- **id**: field containing the ID of entry as defined in section `Definition of Terms`_. This can be the local database ID.
- **attributes**: a dictionary, containing key-value pairs representing the entry's properties, except for type and id.

  Database-provider-specific properties need to include the database-provider-specific prefix (see section `Database-Provider-Specific Namespace Prefixes`_).

OPTIONALLY it can also contains the following fields:

- **links**: a `JSON API links object <http://jsonapi.org/format/1.0/#document-links>`__ can OPTIONALLY contain the field

  - **self**: the entry's URL

- **meta**: a `JSON API meta object <https://jsonapi.org/format/1.0/#document-meta>`__ that contains non-standard meta-information about the object.

- **relationships**: a dictionary containing references to other entries according to the description in section `Relationships`_ encoded as `JSON API Relationships <https://jsonapi.org/format/1.0/#document-resource-object-relationships>`__.
  The OPTIONAL human-readable description of the relationship MAY be provided in the :field:`description` field inside the :field:`meta` dictionary of the JSON API resource identifier object.

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
	     "last_modified": "2007-04-05T14:30Z"
	   }
	 },
	 {
	   "type": "structures",
	   "id": "example.db:structs:1234",
	   "attributes": {
	     "chemical_formula_descriptive": "Es2",
	     "url": "http://example.db/structs/1234",
	     "immutable_id": "http://example.db/structs/1234@123",
	     "last_modified": "2007-04-07T12:02Z"
	   }
	 }
	 // ...
       ]
       // ...
     }

Single Entry Endpoints
----------------------

A client can request a specific entry by appending an URL-encoded ID component to the URL of an entry listing endpoint. This will return properties for the entry with that ID.

In the default JSON response format, the ID component MUST be the content of the :field:`id` field.

Examples:

- :query-url:`http://example.com/optimade/v0.9/structures/exmpl%3Astruct_3232823`
- :query-url:`http://example.com/optimade/v0.9/calculations/232132`

The rules for which properties are to be present for an entry in the response are the same as defined in section `Entry Listing Endpoints`_.

Single Entry URL Query Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The client MAY provide a set of additional URL query parameters for this endpoint type.
URL query parameters not recognized MUST be ignored.
While the following URL query parameters are OPTIONAL for clients, API implementations MUST accept and handle them: **response\_format**, **email\_address**, **response\_fields**.
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
	   "last_modified": "2007-04-07T12:02Z"
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

1. the base URL (e.g., http://example.com/optimade/v0.9/info)
2. type-specific entry listing endpoints (e.g.,
   http://example.com/optimade/v0.9/info/structures)

The types and output content of these info endpoints are described in more detail in the subsections below.
Common for them all are that the :field:`data` field SHOULD return only a single resource object.
If no resource object is provided, the value of the :field:`data` field MUST be :field-val:`null`.

Base URL Info Endpoint
~~~~~~~~~~~~~~~~~~~~~~

The Info endpoint on the base URL or directly after the version number (e.g. http://example.com/optimade/v0.9/info) returns information relating to the API implementation.

The single resource object's response dictionary MUST include the following fields:

- **type**: :field-val:`"info"`
- **id**: :field-val:`"/"`
- **attributes**: Dictionary containing the following fields:

  - **api\_version**: Presently used version of the OPTiMaDe API.
  - **available\_api\_versions**: MUST be a list of dictionaries, each containing the fields:

    - **url**: a string specifying a base URL that MUST adhere to the rules in section `Base URL`_
    - **version**: a string containing the full version number of the API served at that base URL. The version number string MUST NOT be prefixed by, e.g., "v".

  - **formats**: List of available output formats.
  - **entry\_types\_by\_format**: Available entry endpoints as a function of output formats.
  - **available\_endpoints**: List of available endpoints (i.e., the string to be appended to the base URL).

  :field:`attributes` MAY also include the following OPTIONAL fields:

  - **is\_index**: if :field-val:`true`, this is an index meta-database base URL (see section `Index Meta-Database`_).

    If this member is *not* provided, the client MUST assume this is **not** an index meta-database base URL (i.e., the default is for :field:`is_index` to be :field-val:`false`).

If this is an index meta-database base URL (see section `Index Meta-Database`_), then the response dictionary MUST also include the field:

- **relationships**: Dictionary that MAY contain a single `JSON API relationships object <https://jsonapi.org/format/1.0/#document-resource-object-relationships>`__:

  - **default**: Reference to the child identifier object under the :endpoint:`links` endpoint that the provider has chosen as their "default" OPTiMaDe API database.
    A client SHOULD present this database as the first choice when an end-user chooses this provider. This MUST include the field:

    - **data**: `JSON API resource linkage <http://jsonapi.org/format/1.0/#document-links>`__.
      It MUST be either :field-val:`null` or contain a single child identifier object with the fields:

      - **type**: :field-val:`child`
      - **id**: ID of the provider's chosen default OPTiMaDe API database.
        MUST be equal to a valid child object's :field:`id` under the :field:`links` endpoint.

  Lastly, :field:`is_index` MUST also be included in :field:`attributes` and be :field-val:`true`.

Example:

.. code:: jsonc

     {
       "data": {
	 "type": "info",
	 "id": "/",
	 "attributes": {
	   "api_version": "v0.9",
	   "available_api_versions": [
	     {"url": "http://db.example.com/optimade/v0.9/", "version": "0.9.5"},
	     {"url": "http://db.example.com/optimade/v1.0/", "version": "1.0.2"},
	     {"url": "http://db.example.com/optimade/v0.9.2/", "version": "0.9.2"},
	     {"url": "http://db.example.com/optimade/v0.9.5/", "version": "0.9.5"}
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
	   "api_version": "v0.9.8",
	   "available_api_versions": [
	     {"url": "http://db.example.com/optimade/v0.9/", "version": "0.9.5"},
	     {"url": "http://db.example.com/optimade/v0.9.2/", "version": "0.9.2"},
	     {"url": "http://db.example.com/optimade/v1.0/", "version": "1.0.2"}
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
	     "data": { "type": "child", "id": "perovskites" }
	   }
	 }
       }
       // ...
     }

Entry Listing Info Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Entry listing info endpoints are of the form :endpoint:`<base_url>/info/<entry_type>` (e.g., http://example.com/optimade/v0.9/info/structures).
The response for these endpoints MUST include the following information in the :field:`data` field:

- **description**: Description of the entry.
- **properties**: A dictionary describing queryable properties for this entry type, where each key is a property name.
  Each value is a dictionary, with the REQUIRED key :field:`description` and OPTIONAL keys :field:`unit` and :field:`sortable` (see `Entry Listing URL Query Parameters`_ for more information on :field:`sortable`).
- **formats**: List of output formats available for this type of entry.
- **output\_fields\_by\_format**: Dictionary of available output fields for this entry type, where the keys are the values of the :field:`formats` list and the values are the keys of the :field:`properties` dictionary.

Example:

.. code:: jsonc

    {
      "data": {
        "description": "a structures entry",
        "properties": {
          "nelements": {
            "description": "Number of elements",
            "sortable": true
          },
          "lattice_vectors": {
            "description": "Unit cell lattice vectors",
            "unit": "Å",
            "sortable": false
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

This endpoint exposes information on other OPTiMaDe API implementations that are linked to the current implementation.
The endpoint MUST be provided at the path :endpoint:`<base_url>/links`.

It can be considered an introspective endpoint, similar to the Info endpoint, but at a higher level: that is, Info endpoints provide information on the given implementation, while the Links endpoint provides information on the links between immediately related implementations (in particular, an array of none or a single :object:`parent` object and none or more child-type objects, see section `Parent and Child Objects`_).

For Links endpoints, the API implementation MAY ignore any provided query parameters.
Alternatively, it MAY handle the parameters specified in section `Single Entry URL Query Parameters`_ for single entry endpoints.

Links Endpoint JSON Response Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The resource objects' response dictionaries MUST include the following fields:

- **type**: MUST be either :field-val:`"parent"`, :field-val:`"child"`, or :field-val:`"provider"`.
  These objects are described in detail in sections `Parent and Child Objects`_ and `Provider Objects`_.
- **id**: MUST be unique.
- **attributes**: Dictionary that MUST contain the following fields:

  - **name**: Human-readable name for the OPTiMaDe API implementation, e.g., for use in clients to show the name to the end-user.
  - **description**: Human-readable description for the OPTiMaDe API implementation, e.g., for use in clients to show a description to the end-user.
  - **base\_url**: `JSON API links object <http://jsonapi.org/format/1.0/#document-links>`__, pointing to the base URL for this implementation, either directly as a string, or as a links object, which can contain the following fields:

    - **href**: a string containing the OPTiMaDe base URL.
    - **meta**: a meta object containing non-standard meta-information about the implementation.

  - **homepage**: `JSON API links object <http://jsonapi.org/format/1.0/#document-links>`__, pointing to a homepage URL for this implementation, either directly as a string, or as a links object, which can contain the following fields:

    - **href**: a string containing the implementation homepage URL.
    - **meta**: a meta object containing non-standard meta-information about the homepage.

Example:

.. code:: jsonc

     {
       "data": [
	 {
	   "type": "parent",
	   "id": "index",
	   "attributes": {
	     "name": "Index",
	     "description": "Index for example's OPTiMaDe databases",
	     "base_url": "http://example.com/optimade",
	     "homepage": "http://example.com"
	   }
	 },
	 {
	   "type": "child",
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
	     "homepage": "http://example.com"
	   }
	 },
	 {
	   "type": "child",
	   "id": "frameworks",
	   "attributes": {
	     "name": "Zeolitic Frameworks",
	     "description": "",
	     "base_url": "http://example.com/zeo_frameworks/optimade",
	     "homepage": "http://example.com"
	   }
	 },
	 {
	   "type": "provider",
	   "id": "exmpl",
	   "attributes": {
	     "name": "Example provider",
	     "description": "Provider used for examples, not to be assigned to a real database",
	     "base_url": "http://example.com/optimade",
	     "homepage": "http://example.com"
	   }
	 }
	 // ... <other objects>
       ]
       // ...
     }

Parent and Child Objects
~~~~~~~~~~~~~~~~~~~~~~~~

Resource objects that MAY be present under the Links endpoint.

Either none or a single :object:`parent` object MAY be present as part of the :field:`data` array.
The :object:`parent` object represents a "link" to the OPTiMaDe implementation exactly one layer **above** the current implementation's layer.

Any number of :object:`child` objects MAY be present as part of the :field:`data` array.
A :object:`child` object represents a "link" to an OPTiMaDe implementation exactly one layer **below** the current implementation's layer.

    **Note**: The RECOMMENDED number of layers is two.

Provider Objects
~~~~~~~~~~~~~~~~

The :object:`provider` objects are meant to indicate links to an "Index meta-database" hosted by database providers.
The intention is to be able to auto-discover all providers of OPTiMaDe implementations.

A list of known providers can be retrieved as described in section `Database-Provider-Specific Namespace Prefixes`_.
This section also describes where to find information for how a provider can be added to this list.

Index Meta-Database Links Endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the provider implements an "Index meta-database" (see section `Index Meta-Database`_), it is RECOMMENDED to adopt a structure, where the index meta-database is the "parent" implementation of the provider's other OPTiMaDe databases.

This will make all OPTiMaDe databases and implementations by the provider discoverable as :object:`child` objects under the Links endpoint of the "Index meta-database".

Custom Extension Endpoints
--------------------------

API implementations MAY provide custom endpoints under the Extensions endpoint.
These endpoints MUST be on the form "<base\_url>/extensions/<custom paths>".

API Filtering Format Specification
==================================

An OPTiMaDe filter expression is passed in the parameter :query-param:`filter` as an URL query parameter as `specified by JSON
API <https://jsonapi.org/format/1.0/#fetching-filtering>`__.
The filter expression allows desired properties to be compared against search values; several such comparisons can be combined using the logical conjunctions AND, OR, NOT, and parentheses, with their usual semantics.

All properties marked as REQUIRED in section `Entry list`_ MUST be queryable with all mandatory filter features.
The level of query support REQUIRED for other properties is described in `Entry list`_.

When provided as an URL query parameter, the contents of the :query-param:`filter` parameter is URL-encoded by the client in the HTTP GET request, and then URL-decoded by the API implementation before any further parsing takes place.
In particular, this means the client MUST escape special characters in string values as described below for `String values`_ before the URL encoding, and the API implementation MUST first URL-decode the :query-param:`filter` parameter before reversing the escaping of string tokens.

Examples of syntactically correct query strings embedded in queries:

-  :query-url:`http://example.org/optimade/v0.9/structures?filter=_exmpl_melting_point%3C300+AND+ nelements=4+AND+elements="Si,O2"&response_format=xml`

Or, fully URL encoded :

-  :query-url:`http://example.org/optimade/v0.9/structures?filter=_exmpl_melting_point%3C300+AND+nelements%3D4+AND+elements%3D%22Si%2CO2%22&response_format=xml`

Lexical Tokens
--------------

The following tokens are used in the filter query component:

- **Property names**: the first character MUST be a lowercase letter, the subsequent symbols MUST be composed of lowercase letters or digits; the underscore ("\_", ASCII 95 dec (0x5F)) is considered to  be a lower-case letter when defining identifiers.
  The length of the identifiers is not limited, except that when passed as a URL query parameter the whole query SHOULD NOT be longer than the limits imposed by the URI specification.
  This definition is similar to one used in most widespread programming languages, except that OPTiMaDe limits allowed letter set to lowercase letters only.
  This allows to tell OPTiMaDe identifiers and operator keywords apart unambiguously without consulting a reserved word table and to encode this distinction concisely in the EBNF Filter Language grammar.

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

- **Numeric values** are represented as decimal integers or is scientific notation, using the usual programming language conventions.
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

    **Note:** The motivation to exclude the form :filter-fragment:`constant <operator> constant` for strings is that filter language strings can refer to data of different data types (e.g., strings and timestamps), and thus this construct is not unambigous.
    The OPTiMaDe specification will strive to address this issue in a future version.

Examples:

- :filter:`nelements > 3`
- :filter:`chemical_formula_hill = "H2O" AND chemical_formula_anonymous != "AB"`
- :filter:`_exmpl_aax <= +.1e8 OR nelements >= 10 AND NOT ( _exmpl_x != "Some string" OR NOT _exmpl_a = 7)`
- :filter:`_exmpl_spacegroup="P2"`
- :filter:`_exmpl_cell_volume<100.0`
- :filter:`_exmpl_bandgap > 5.0 AND _exmpl_molecular_weight < 350`
- :filter:`_exmpl_melting_point<300 AND nelements=4 AND elements="Si,O2"`
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
- :filter:`chemical_formula_anonymous STARTS "B2" AND chemical_formula_anonymous ENDS WITH "D2"`

Comparisons of list properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the following, :property:`list` is a list-type property, and :filter-fragment:`values` is one or more :filter-fragment:`value` separated by commas (","), i.e., strings or numbers.
An implementation MAY also support property names and nested property names in :filter-fragment:`values`.

The following constructs MUST be supported:

- :filter:`list HAS value`: matches if at least one element in :filter-fragment:`list` is equal to filter-fragment:`value`. (If :filter-fragment:`list` has no duplicate elements, this implements the set operator IN.)
- :filter:`list HAS ALL values`: matches if, for each :filter-fragment:`value`, there is at least one element in :filter-fragment:`list` equal to that value. (If both :filter-fragment:`list` and :filter-fragment:`values` do not contain duplicate values, this implements the set operator >=.)
- :filter:`list HAS ANY values`: matches if at least one element in :filter-fragment:`list` is equal to at least one :filter-fragment:`value`. (This is equivalent to a number of HAS statements separated by OR.)
- :filter:`list LENGTH value`: matches if the number of items in the :filter-fragment:`list` property is equal to :filter-fragment:`value`.

The following construct MAY be supported:

- :filter:`list HAS ONLY values`: matches if all elements in :filter-fragment:`list` are equal to at least one :filter-fragment:`value`.
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

- :filter:`list HAS < 3`: matches all entries for which :filter-fragment:`list` contains at least one element that is less than three.
- :filter:`list HAS ALL < 3, > 3`: matches only those entries for which :filter-fragment:`list` simultaneously contains at least one element less than three and one element greater than three.

An implementation MAY support combining the operator syntax with the syntax for correlated lists in particularly on a list correlated with itself. For example:

- :filter:`list:list HAS >=2:<=5`: matches all entries for which :filter-fragment:`list` contains at least one element that is between the values 2 and 5.

Further examples of various comparisons of list properties:

- :filter:`elements HAS "H" AND elements HAS ALL "H","He","Ga","Ta" AND elements HAS ONLY "H","He","Ga","Ta" AND elements HAS ANY "H", "He", "Ga", "Ta"`
- OPTIONAL: :filter:`elements HAS ONLY "H","He","Ga","Ta"`
- OPTIONAL: :filter:`elements:_exmpl_element_counts HAS "H":6 AND elements:_exmpl_element_counts HAS ALL "H":6,"He":7 AND elements:_exmpl_element_counts HAS ONLY "H":6 AND elements:_exmpl_element_counts HAS ANY "H":6,"He":7 AND elements:_exmpl_element_counts HAS ONLY "H":6,"He":7`
- OPTIONAL: :filter:`_exmpl_element_counts HAS < 3 AND _exmpl_element_counts HAS ANY > 3, = 6, 4, != 8`
  (note: specifying the = operator after HAS ANY is redundant here, if no operator is given, the test is for equality.)
- OPTIONAL: :filter:`elements:_exmpl_element_counts:_exmpl_element_weights HAS ANY > 3:"He":>55.3 , = 6:>"Ti":<37.6 , 8:<"Ga":0`

Nested property names
~~~~~~~~~~~~~~~~~~~~~

Everywhere in a filter string where a property name is accepted, the API implementation MAY accept nested property names as described in section `Lexical Tokens`_, consisting of identifiers separated by periods ('.').
A filter on a nested property name consisting of two identifiers :filter-fragment:`identifier1.identifierd2` matches if either one of these points are true:

- :filter-fragment:`identifier1` references a dictionary-type property that contains as an identifier :filter-fragment:`identifier2` and the filter matches for the content of :filter-fragment:`identifier2`.

- :filter-fragment:`identifier1` references a list of dictionaries that contain as an identifier :filter-fragment:`identifier2` and the filter matches for a flat list containing only the contents of :filter-fragment:`identifier2` for every dictionary in the list.
  E.g., if :filter-fragment:`identifier1` is the list :filter-fragment:`[{"identifier2":42, "identifier3":36}, {"identifier2":96, "identifier3":66}]`, then :filter-fragment:`identifier1.identifier2` is understood in the filter as the list :filter-fragment:`[42, 96]`.

The API implementation MAY allow this notation to generalize to arbitary depth.
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
    For example, to find all structures with bibliographic references where one of the authors has the last name "Schmit" is performed by the following two steps:

    - Query the :endpoint:`references` endpoint with a filter :filter:`authors.lastname HAS "Schmit"` and store the :filter-fragment:`id` values of the returned entries.
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
Similarly, for database-provider-specific properties, the database provider decides their types.
In the syntactic constructs that can accommodate values of more than one type, types of all participating values are REQUIRED to match, with a single exception of timestamps (see below).
Different types of values MUST be reported as :http-error:`501 Not Implemented` errors, meaning that type conversion is not implemented in the specification.

As the filter language syntax does not define a lexical token for timestamps, values of this type are expressed using string tokens in `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__.
In a comparison with a timestamp property, a string token represents a timestamp value that would result from parsing the string according to RFC 3339 Internet Date/Time Format.
Interpretation failures MUST be reported with error :http-error:`400 Bad Request`.

Optional filter features
~~~~~~~~~~~~~~~~~~~~~~~~

Some features of the filtering language are marked OPTIONAL.
An implementation that encounters an OPTIONAL feature that it does not support MUST respond with error ``501 Not Implemented`` with an explanation of which OPTIONAL construct the error refers to.

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

- **Description**: The name of the type of an entry. Any entry MUST be able to be fetched using the `base URL <Base URL_>`_ type and ID at the URL :endpoint:`<base URL>/<type>/<id>`.
- **Type**: string.
- **Requirements/Conventions**:

  - **Support**: MUST be supported by all implementations, MUST NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - **Response**: REQUIRED in the response.
  - MUST be an existing entry type.

- **Example**: :val:`"structures"`

immutable\_id
~~~~~~~~~~~~~

- **Description**: The entry's immutable ID (e.g., an UUID). This is important for databases having preferred IDs that point to "the latest version" of a record, but still offer access to older variants. This ID maps to the version-specific record, in case it changes in the future.
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

- **Example**:

  - As part of JSON response format: :VAL:`"2007-04-05T14:30Z"` (i.e., encoded as an `RFC 3339 Internet Date/Time Format <https://tools.ietf.org/html/rfc3339#section-5.6>`__ string.)

database-provider-specific properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: Database providers are allowed to insert database-provider-specific entries in the output of both standard entry types and database-provider-specific entry types.
- **Type**: Decided by the API implementation.
- **Requirements/Conventions**:

  - **Support**: Support for database-provider-specific properties is fully OPTIONAL.
  - **Query**: Support for queries on these properties are OPTIONAL.
    If supported, only a subset of the filter features MAY be supported.
  - **Response**: API implementations are free to choose whether database-provider-specific properties are only included when requested using the query parameter :query-param:`response_fields`, or if they are included also when :query-param:`response_fields` is not present.
    Implementations are thus allowed to decide that some of these properties are part of what can be seen as the default value of :query-param:`response_fields` when that query parameter is omitted.
    Implementations SHOULD NOT include database-provider-specific properties when the query parameter :query-param:`response_fields` is present but does not list them.
  - These MUST be prefixed by a database-provider-specific prefix (see appendix `Database-Provider-Specific Namespace Prefixes`_).

- **Examples**: A few examples of valid database-provided-specific property names follows:

  - \_exmpl\_formula\_sum
  - \_exmpl\_band\_gap
  - \_exmpl\_supercell
  - \_exmpl\_trajectory
  - \_exmpl\_workflow\_id

Structures Entries
------------------

:entry:`structures` entries (or objects) have the properties described above in section `Properties Used by Multiple Entry Types`_, as well as the following properties:

elements
~~~~~~~~

- **Description**: Names of the different elements present in the structure.
- **Type**: list of strings.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.
  - The strings are the chemical symbols, i.e., either a single uppercase letter or an uppercase letter followed by a number of lowercase letters.
  - The order MUST be alphabetical.
  - Note: This property SHOULD NOT contain the string "X" to indicate non-chemical elements or "vacancy" to indicate vacancies (in contrast to the field :field:`chemical_symbols` for the :property:`species` property).

- **Examples**:

  - :val:`["Si"]`
  - :val:`["Al","O","Si"]`

- **Query examples**:
  - A filter that matches all records of structures that contain Si, Al **and** O, and possibly other elements: :filter:`elements HAS ALL "Si", "Al", "O"`.
  - To match structures with exactly these three elements, use :filter:`elements HAS ALL "Si", "Al", "O" AND elements LENGTH 3`.

nelements
~~~~~~~~~

- **Description**: Number of different elements in the structure as an integer.
- **Type**: integer
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property with support for all mandatory filter features.

- **Example**: :val:`3`
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

- **Examples**:

  - :val:`[1.0]`
  - :val:`[0.3333333333333333, 0.2222222222222222, 0.4444444444444444]`

- **Query examples**:

  - Note: Useful filters can be formulated using the set operator syntax for correlated values.
    However, since the values are floating point values, the use of equality comparisons is generally inadvisable.
  - A filter that matches structures where approximately 1/3 of the atoms in the structure are the element Al is: :filter:`elements:elements_ratios HAS ALL "Al":>0.3333, "Al":<0.3334`.

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
  - Element names MUST have proper capitalization (e.g., :val:`"Si"`, not :VAL:`"SI"` for "silicon").
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
  - Element names MUST have proper capitalization (e.g., :val:`"Si"`, not :VAL:`"SI"` for "silicon").
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
  - **Query**: MUST be a queryable property. However, support for filters using partial string matching with this property is OPTIONAL (i.e., BEGINS WITH, ENDS WITH, and CONTAINS).

- **Examples**:

  - :val:`"A2B"`
  - :val:`"A42B42C16D12E10F9G5"`

- **Querying**:
  - A filter that matches an exactly given formula is :filter:`chemical_formula_anonymous="A2B"`.

dimension\_types
~~~~~~~~~~~~~~~~

- **Description**: List of three integers.
  For each of the three directions indicated by the three lattice vectors (see property `lattice_vectors`_).
  This list indicates if the direction is periodic (value :val:`1`) or non-periodic (value :val:`0`).
  Note: the elements in this list each refer to the direction of the corresponding entry in property `lattice_vectors`_ and *not* the Cartesian x, y, z directions.
- **Type**: list of integers.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: MUST be a queryable property. Support for equality comparison is REQUIRED, support for other comparison operators are OPTIONAL.
  - MUST be a list of length 3.
  - Each integer element MUST assume only the value 0 or 1.

- **Examples**:

  - For a molecule: :val:`[0, 0, 0]`
  - For a wire along the direction specified by the third lattice vector: :val:`[0, 0, 1]`
  - For a 2D surface/slab, periodic on the plane defined by the first and third lattice vectors: :val:`[1, 0, 1]`
  - For a bulk 3D system: :val:`[1, 1, 1]`

lattice\_vectors
~~~~~~~~~~~~~~~~

- **Description**: The three lattice vectors in Cartesian coordinates, in ångström (Å).
- **Type**: list of list of floats.
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - MUST be a list of three vectors *a*, *b*, and *c*, where each of the vectors MUST BE a list of the vector's coordinates along the x, y, and z Cartesian coordinates.
    (Therefore, the first index runs over the three lattice vectors and the second index runs over the x, y, z Cartesian coordinates).
  - For databases that do not define an absolute Cartesian system (e.g., only defining the length and angles between vectors), the first lattice vector SHOULD be set along *x* and the second on the *xy*-plane.
  - This property MUST be an array of dimensions 3 times 3 regardless of the elements of :property:`dimension\_types`.
    The vectors SHOULD by convention be chosen so the determinant of the :property:`lattice_vectors` matrix is different from zero.
    The vectors in the non-periodic directions have no significance beyond fulfilling these requirements.
  - All three elements of the inner lists of floats MAY be :val:`null` for non-periodic dimensions, i.e., those dimensions for which :property:`dimension\_types` is :val:`0`.

- **Examples**:

  - :val:`[[4.0,0.0,0.0],[0.0,4.0,0.0],[0.0,1.0,4.0]]` represents a cell, where the first vector is :val:`(4, 0, 0)`, i.e., a vector aligned along the :val:`x` axis of length 4 Å; the second vector is :val:`(0, 4, 0)`; and the third vector is :val:`(0, 1, 4)`.

cartesian\_site\_positions
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: Cartesian positions of each site. A site is an atom, a site potentially occupied by an atom, or a placeholder for a virtual mixture of atoms (e.g., in a virtual crystal approximation).
- **Type**: list of list of floats and/or unknown values
- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - It MUST be a list of length equal to the number of sites in the structure where every element is a list of the three Cartesian coordinates of a site.
  - An entry MAY have multiple sites at the same Cartesian position (for a relevant use of this, see e.g., the property `assemblies`_).
  - If a component of the position is unknown, the :val:`null` value SHOULD be provided instead (see section `Properties with an unknown value`_).
    Otherwise, it SHOULD be a float value, expressed in angstrom (Å).
    If at least one of the coordinates is unknown, the correct flag in the list property `structure_features`_ MUST be set.
  - **Notes**: (for implementers) While this is unrelated to this OPTiMaDe specification: If you decide to store internally the :property:`cartesian_site_positions` as a float array, you might want to represent :val:`null` values with :field-val:`NaN` values.
    The latter being valid float numbers in the IEEE 754 standard in `IEEE 754-1985 <https://doi.org/10.1109/IEEESTD.1985.82928>`__ and in the updated version `IEEE 754-2008 <https://doi.org/10.1109/IEEESTD.2008.4610935>`__.

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
  - :val:`["Ac", "Ac", "Ag", "Ir"]` indicating the first two sites contains the :val:`"Ac"` species, while the third and fourth sites contain the :val:`"Ag"` and :val:`"Ir"` species, respectively.

species
~~~~~~~

- **Description**: A list describing the species of the sites of this structure. Species can be pure chemical elements, or virtual-crystal atoms representing a statistical occupation of a given site by multiple chemical elements.
- **Type**: list of dictionary with keys:

  - :property:`name`: string (REQUIRED)
  - :property:`chemical_symbols`: list of strings (REQUIRED)
  - :property:`concentration`: list of float (REQUIRED)
  - :property:`mass`: float (OPTIONAL)
  - :property:`original_name`: string (OPTIONAL).

- **Requirements/Conventions**:

  - **Support**: SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.
  - **Query**: Support for queries on this property is OPTIONAL.
    If supported, filters MAY support only a subset of comparison operators.
  - Each list member MUST be a dictionary with the following keys:

    - **name**: REQUIRED; gives the name of the species; the **name** value MUST be unique in the :property:`species` list;

    - **chemical\_symbols**: REQUIRED; MUST be a list of strings of all chemical elements composing this species. Each item of the list MUST be one of the following:

      - a valid chemical-element name, or
      - the special value :val:`"X"` to represent a non-chemical element, or
      - the special value :val:`"vacancy"` to represent that this site has a non-zero probability of having a vacancy (the respective probability is indicated in the :property:`concentration` list, see below).

      If any one entry in the :property:`species` list has a :property:`chemical_symbols` list that is longer than 1 element, the correct flag MUST be set in the list :property:`structure_features` (see property `structure_features`_).

    - **concentration**: REQUIRED; MUST be a list of floats, with same length as :property:`chemical_symbols`. The numbers represent the relative concentration of the corresponding chemical symbol in this species.
      The numbers SHOULD sum to one. Cases in which the numbers do not sum to one typically fall only in the following two categories:

      - Numerical errors when representing float numbers in fixed precision, e.g. for two chemical symbols with concentrations :val:`1/3` and :val:`2/3`, the concentration might look something like :val:`[0.33333333333, 0.66666666666]`. If the client is aware that the sum is not one because of numerical precision, it can renormalize the values so that the sum is exactly one.
      - Experimental errors in the data present in the database. In this case, it is the responsibility of the client to decide how to process the data.

      Note that concentrations are uncorrelated between different site (even of the same species).

    - **mass**: OPTIONAL. If present MUST be a float expressed in a.m.u.
    - **original\_name**: OPTIONAL. Can be any valid Unicode string, and SHOULD contain (if specified) the name of the species that is used internally in the source database.

          Note: With regards to "source database", we refer to the immediate source being queried via the OPTiMaDe API implementation.
	  The main use of this field is for source databases that use species names, containing characters that are not allowed (see description of the list property `species_at_sites`_).

  - For systems that have only species formed by a single chemical symbol, and that have at most one species per chemical symbol, SHOULD use the chemical symbol as species name (e.g., :val:`"Ti"` for titanium, :val:`"O"` for oxygen, etc.)
    However, note that this is OPTIONAL, and client implementations MUST NOT assume that the key corresponds to a chemical symbol, nor assume that if the species name is a valid chemical symbol, that it represents a species with that chemical symbol.
    This means that a species :val:`{"name": "C", "chemical_symbols": ["Ti"], "concentration": [1.0]}` is valid and represents a titanium species (and *not* a carbon species).
  - It is NOT RECOMMENDED that a structure includes species that do not have at least one corresponding site.

- **Examples**:

  - :val:`[ {"name": "Ti", "chemical_symbols": ["Ti"], "concentration": [1.0]} ]`: any site with this species is occupied by a Ti atom.
  - :val:`[ {"name": "Ti", "chemical_symbols": ["Ti", "vacancy"], "concentration": [0.9, 0.1]} ]`: any site with this species is occupied by a Ti atom with 90 % probability, and has a vacancy with 10 % probability.
  - :val:`[ {"name": "BaCa", "chemical_symbols": ["vacancy", "Ba", "Ca"], "concentration": [0.05, 0.45, 0.5], "mass": 88.5} ]`: any site with this species is occupied by a Ba atom with 45 % probability, a Ca atom with 50 % probability, and by a vacancy with 5 % probability. The mass of this site is (on average) 88.5 a.m.u.
  - :val:`[ {"name": "C12", "chemical_symbols": ["C"], "concentration": [1.0], "mass": 12.0} ]`: any site with this species is occupied by a carbon isotope with mass 12.
  - :val:`[ {"name": "C13", "chemical_symbols": ["C"], "concentration": [1.0], "mass": 13.0} ]`: any site with this species is occupied by a carbon isotope with mass 13.

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

  - :val:`{"sites_in_groups": [[0], [1]], "group_probabilities: [0.3, 0.7]}`: the first site and the second site never occur at the same time in the unit cell.
    Statistically, 30 % of the times the first site is present, while 70 % of the times the second site is present.
  - :val:`{"sites_in_groups": [[1,2], [3]], "group_probabilities: [0.3, 0.7]}`: the second and third site are either present together or not present; they form the first group of atoms for this assembly.
    The second group is formed by the fourth site.
    Sites of the first group (the second and the third) are never present at the same time as the fourth site.
    30 % of times sites 1 and 2 are present (and site 3 is absent); 70 % of times site 3 is present (and sites 1 and 2 are absent).

- **Notes**:

  - Assemblies are essential to represent, for instance, the situation where an atom can statistically occupy two different positions (sites).
  - By defining groups, it is possible to represent, e.g., the case where a functional molecule (and not just one atom) is either present or absent (or the case where it it is present in two conformations)
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
	     "species": {
	       "Si": { "chemical_symbols": ["Si"], "concentration": [1.0] },
	       "Ge": { "chemical_symbols": ["Ge"], "concentration": [1.0] },
	       "vac": { "chemical_symbols": ["vacancy"], "concentration": [1.0] }
	     },
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
	       "group_probabilities": [0.2, 0.8],
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
  - **Query**: MUST be a queryable property. Filters on the list MUST support all mandatory HAS-type queries. Filter operators for comparisons on the string components MUST support equality, support for other comparison operators are OPTIONAL.
  - MUST be an empty list if no special features are used.
  - MUST be sorted alphabetically.
  - If a special feature listed below is used, the list MUST contain the corresponding string.
  - If a special feature listed below is not used, the list MUST NOT contain the corresponding string.
  - **List of strings used to indicate special structure features**:

    - :val:`disorder`: This flag MUST be present if any one entry in the :property:`species` list has a :property:`chemical_symbols` list that is longer than 1 element.
    - :val:`unknown_positions`: This flag MUST be present if at least one component of the :property:`cartesian_site_positions` list of lists has value :val:`null`.
    - :val:`assemblies`: This flag MUST be present if the property `assemblies`_ is present.

-  **Examples**: A structure having unknown positions and using assemblies: :val:`["assemblies", "unknown_positions"]`

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

Database-Provider-Specific Entry Types
--------------------------------------

Names of database-provider-specific entry types MUST start with database-provider-specific namespace prefix (see appendix `Database-Provider-Specific Namespace Prefixes`_).
Database-provider-specific entry types MUST have all properties described above in section `Properties Used by Multiple Entry Types`_.

- **Requirements/Conventions for properties in database-provider-specific entry types**:

  - **Support**: Support for any properties in database-provider-specific entry types is fully OPTIONAL.
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

For example, for the JSON response format, the top-level :field:`included` field SHOULD be used as per the `JSON API 1.0 specification <https://jsonapi.org/format/1.0/#fetching-includes>`__:

.. code:: jsonc

    {
      "data": {
        "type": "structures",
        "id": "example.db:structs:1234",
        "attributes": {
          "formula": "Es2",
          "url": "http://example.db/structs/1234",
          "immutable_id": "http://example.db/structs/1234@123",
          "last_modified": "2007-04-07T12:02Z"
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

Appendices
==========

The Filter Language EBNF Grammar
--------------------------------

.. code:: ebnf

    (* BEGIN EBNF GRAMMAR Filter *)
    (* The top-level 'filter' rule: *)

    Filter = [Spaces], Expression ;

    (* Values *)

    Constant = String | Number ;

    Value = String | Number | Property ;
    (* Note: support for Property in Value is OPTIONAL *)

    ValueList = [ Operator ], Value, { Comma, [ Operator ], Value } ;
    (* Support for Operator in ValueList is OPTIONAL *)

    ValueZip = [ Operator ], Value, Colon, [ Operator ], Value, {Colon, [ Operator ], Value } ;
    (* Support for Operator in ValueZip is OPTIONAL *)

    ValueZipList = ValueZip, { Comma, ValueZip } ;

    (* Expressions *)

    Expression = ExpressionClause, [ OR, Expression ] ;

    ExpressionClause = ExpressionPhrase, [ AND, ExpressionClause ] ;

    ExpressionPhrase = [ NOT ], ( Comparison | OpeningBrace, Expression, ClosingBrace ) ;

    Comparison = ConstantFirstComparison
               | PropertyFirstComparison ;
    (* Note: support for ConstantFirstComparison is OPTIONAL *)

    ConstantFirstComparison = Constant, ValueOpRhs ;

    PropertyFirstComparison = Property, ( ValueOpRhs
                                        | KnownOpRhs
                                        | FuzzyStringOpRhs
                                        | SetOpRhs
                                        | SetZipOpRhs
                                        | LengthOpRhs ) ;
    (* Note: support for SetZipOpRhs in Comparison is OPTIONAL *)

    ValueOpRhs = Operator, Value ;

    KnownOpRhs = IS, ( KNOWN | UNKNOWN ) ;

    FuzzyStringOpRhs = CONTAINS, Value
                     | STARTS, [ WITH ], Value
                     | ENDS, [ WITH ], Value ;

    SetOpRhs = HAS, ( [ Operator ], Value | ALL, ValueList | ANY, ValueList | ONLY, ValueList ) ;
    (* Note: support for ONLY in SetOpRhs is OPTIONAL *)
    (* Note: support for [ Operator ] in SetOpRhs is OPTIONAL *)

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

    Operator = ( '<', [ '=' ] | '>', [ '=' ] | [ '!' ], '=' ), [Spaces] ;

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

Regular Expressions for OPTiMaDe Filter Tokens
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
