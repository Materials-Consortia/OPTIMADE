# OPTiMaDe API specification v0.9.8-develop

[1. Introduction](#h.1)

[2. Term Definition](#h.2)

[3. General API Requirements and Conventions](#h.3)  
&nbsp;&nbsp;&nbsp;&nbsp;[3.1. Base URL](#h.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;[3.2. URL Encoding](#h.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[3.3. Responses](#h.3.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.1. Response Format](#h.3.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.2. JSON API Response Schema: Common Fields](#h.3.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.3. HTTP Response Status Codes](#h.3.3.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.4. Unset optional properties](#h.3.3.4)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.5. Warnings](#h.3.3.5)  
&nbsp;&nbsp;&nbsp;&nbsp;[3.4. Index Meta-Database](#h.3.4)  

[4. API endpoints](#h.4)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.1. Entry Listing Endpoints](#h.4.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.1.1. URL Query Parameters](#h.4.1.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.1.2. JSON API Response Schema](#h.4.1.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.2. Single Entry Endpoints](#h.4.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.1. URL Query Parameters](#h.4.2.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.2. JSON API Response Schema](#h.4.2.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.3. Info Endpoints](#h.4.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.1. Base URL Info Endpoint](#h.4.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2. Entry Listing Info Endpoints](#h.4.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.4. Links Endpoint](#h.4.4)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.4.1. JSON API Response Schema](#h.4.4.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.4.2. Parent and Child Objects](#h.4.4.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.4.3. Provider Objects](#h.4.4.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.4.4. Index Meta-Database Links Endpoint](#h.4.4.4)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.5. Custom Extension Endpoints](#h.4.5)  

[5. API Filtering Format Specification](#h.5)  
&nbsp;&nbsp;&nbsp;&nbsp;[5.1. Lexical Tokens](#h.5.1)  
&nbsp;&nbsp;&nbsp;&nbsp;[5.2. The Filter Language Syntax](#h.5.2)  

[6. Entry List](#h.6)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.1. Properties Used by Multiple Entry Types](#h.6.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.1.1. id](#h.6.1.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.1.2. type](#h.6.1.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.1.3. last\_modified](#h.6.1.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.1.4. database-provider-specific properties](#h.6.1.4)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.2. Structure Entries](#h.6.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.1. elements](#h.6.2.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.2. nelements](#h.6.2.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.3. chemical\_formula](#h.6.2.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.4. formula\_prototype](#h.6.2.4)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.5. dimension\_types](#h.6.2.5)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.6. lattice\_vectors](#h.6.2.6)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.7. cartesian\_site\_positions](#h.6.2.7)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.8. species\_at\_sites](#h.6.2.8)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.9. species](#h.6.2.9)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.10. assemblies](#h.6.2.10)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.2.11. structure\_features](#h.6.2.11)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.3. Calculation Entries](#h.6.3)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.4. Reference Entries](#h.6.4)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.5. Database-Provider-Specific Entry Types](#h.6.5)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.6. Relationships Used by Multiple Entry Types](#h.6.6)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.6.1. references](#h.6.6.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.6.2. calculations](#h.6.6.2)  

[Appendix 1: Database-Provider-Specific Namespace Prefixes](#h.app1)  
[Appendix 2: The Filter Language EBNF Grammar](#h.app2)  
[Appendix 3: The Regular Expressions to Check OPTiMaDe Number Syntax](#h.app3)

# <a name="h.1">1. Introduction</a>

As researchers create independent materials databases, much can be
gained from retrieving data from multiple databases. However, the
retrieval process is difficult if each database has a different
API. This document defines a standard API for retrieving data from
materials databases. This API was developed by the participants of the
workshop "Open Databases Integration for Materials Design", held at
the Lorentz Center in Leiden, Netherlands from 2016-10-24 to
2016-10-28.

It is the intent that the API in the present document adheres to the
[JSON API](http://jsonapi.org/format/1.0) v1.0 specification (with the exception that
non-conformant responses can be generated if an API user specifically
requests a non-standard response format). In cases where specific
restrictions are given in the JSON API specification that are stricter than what is
formulated in this document, they are expected to be upheld by API
implementations unless otherwise noted in this document.
(This may apply to, e.g., the format of Member Names and/or return codes.)

The full present version number of the specification is shown as part of the
top headline of this document.

# <a name="h.2">2. Term Definition</a>

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).

* **Database provider**: A service that provides one or more databases of materials information.
* **Database-provider-specific prefix**: This specification defines a set of
  database-provider-specific prefixes in [Appendix 1](#h.app1).
* **Implementation**: An instance serving the OPTiMaDe API.
* **Database**: An implementation that serves materials information.
* **Entry**: A type of resource, over which a query can be formulated using the API
  (e.g., structure or calculation).
* **Property**: Anything that can be in the filtering of results. MUST NOT
  match any of the entry names.
* **Field**: A property that can be requested as partial output from the API.
* **Resource object**: Represent resources. MUST contain at least the following top-level fields:
  `id`, `type`.
* **ID**: A unique identifier referencing a specific resource in the database.
  Together with **Entry**, the ID MUST uniquely identify the **Resource object**.
  IDs MUST be URL-safe; in particular, they MUST NOT contain commas.
  Reasonably short IDs are encouraged and SHOULD NOT be longer than 255 characters.
  It does not need to be immutable, and MUST NOT be a reserved word.
* **Immutable ID**: A unique identifier that specifies a specific resource in a
  database that MUST be immutable.
* **Reserved words**: The list of reserved words in this standard is:
  `info`.
* **Property Types**:
  * **string**, **integer**, **float**, **boolean**, **null value**: Base data
    types as defined in more detail in section [5.1. Lexical Tokens](#h.5.1).
  * **list**, **dictionary**: Collection of base types with the meaning they have in the JSON
    data-interchange format, i.e., an ordered list of elements
    (where each element can have a different type) or a hash table
    (with the limitation that the hash key MUST be a string), respectively.

# <a name="h.3">3. General API Requirements and Conventions</a>

## <a name="h.3.1">3.1. Base URL</a>

Each database provider will publish a base URL that serves the API. An
example could be: <http://example.com/optimade/>. Every URL component
that follows the base URL MUST behave as standardized in this API
specification.

The client MAY include a version number in the base URL, prefixed with
the letter "v", where the version number indicates the version of the
API standard that the client requests. The format is either
vMAJOR or vMAJOR.MINOR where MAJOR is the major version number, and
MINOR is the minor version number of the standard being referenced. If
the major version is 0, the minor version MUST also be included. The
database provider MAY support further levels of versioning separated
from the major and minor version by a decimal point, e.g., patch
version on the format vMAJOR.MINOR.PATCH. However, the client MUST NOT
assume levels beyond the minor version are supported.

If the client does not include a version number in the base URL, the
request is for the latest version of this standard that the database
provider implements. A query that includes a major and/or minor
version is for the latest subversion of that major and/or minor
version that the database provider implements.

A database provider MAY choose to only support a subset of possible
versions. The client can find out which versions are supported using
the `available_api_versions` field of the `attributes` field from a
query to the base URL `info` endpoint (see section
[4.3.1. Base URL Info Endpoint](#h.4.3.1)). The database
provider SHOULD strive to implement the latest subversion of any major
and minor version supported. Specifically, the latest version of this
standard SHOULD be supported.

Examples of valid base URLs:

* <http://example.com/optimade/>
* <http://example.com/optimade/v0.9/>
* <http://example.com/>
* <http://example.com/some/path/>

Examples of invalid base URLs:

* <http://example.com/optimade/v0/>
* <http://example.com/optimade/0.9/>

## <a name="h.3.2">3.2. URL Encoding</a>

Clients SHOULD encode URLs according to [RFC 3986](http://tools.ietf.org/html/rfc3986).
API implementations MUST decode URLs according to [RFC 3986](http://tools.ietf.org/html/rfc3986).

## <a name="h.3.3">3.3. Responses</a>

### <a name="h.3.3.1">3.3.1. Response Format</a>

API responses MUST be returned in the format specified in the
request. If no specific response format is specified in the request by
use of the `response_format` URL query parameter (see below), the default
response format is [JSON API v1.0](http://jsonapi.org/format/1.0) specification.
All endpoints MUST support at least the JSON API format.
Each endpoint MAY OPTIONALLY support multiple formats,
and declare these formats in their `info` endpoints
(see section [4.3.2. Entry Listing Info Endpoints](#h.4.3.2)).

An API implementation MAY return other formats than specified here.
These can be implemented and documented according to the database provider.
However, they MUST be prefixed by a database-provider-specific prefix as defined in
[Appendix 1](#h.app1).

Specifying a `response_format` URL query parameter different from JSON API,
allows the implementation to break conformance with the JSON API specification.
Not only in response format, but also in, e.g., how content negotiation is implemented.

### <a name="h.3.3.2">3.3.2. JSON API Response Schema: Common Fields</a>

Every response SHOULD contain the following fields, and MUST contain at least one:

* **meta**: a [JSON API meta member](https://jsonapi.org/format/1.0/#document-meta)
  that contains JSON API meta objects of non-standard meta-information.  
  It MUST be a dictionary with these fields:

  * **query**: information on the query that was requested.  
    It MUST be a dictionary with these fields:
    * **representation**: a string with the part of the URL following the base URL.

  * **api\_version**: a string containing the version of the API implementation.
  * **time\_stamp**: a string containing the date and time at which the query
    was executed, in [ISO 8601](https://www.iso.org/standard/40874.html)
    format.  Times MUST be timezone-aware (i.e., MUST NOT be local times),
    in one of the formats allowed by [ISO 8601](https://www.iso.org/standard/40874.html)
    (i.e., either be in UTC, and then end with a Z, or indicate explicitly
    the offset).
  * **data\_returned**: an integer containing the number of data objects returned for the query.
  * **more\_data\_available**: `false` if all data for this query has been
    returned, and `true` if not.
  * **provider**: information on the database provider of the implementation.  
  It MUST be a dictionary with these fields:
    * **name**: a short name for the database provider.
    * **description**: a longer description of the database provider.
    * **prefix**: database-provider-specific prefix as found in [Appendix 1](#h.app1).

    `provider` MAY OPTIONALLY include these fields:

    * **homepage**: a [JSON API links object](http://jsonapi.org/format/1.0/#document-links),
    pointing to the homepage of the database provider, either directly as a string,
    or as a link object which can contain the following fields:
      * **href**: a string containing the homepage URL.
      * **meta**: a meta object containing non-standard meta-information about the
      database provider's homepage.
    * **index\_base\_url**: a [JSON API links object](http://jsonapi.org/format/1.0/#document-links)
    pointing to the base URL for the `index` meta-database of the provider as specified in
    [Appendix 1](#h.app1), either directly as a string, or as a link object
    which can contain the following fields:
      * **href**: a string containing the base URL for the database provider's
      `index` meta-database.
      * **meta**: a meta object containing non-standard meta-information about this link.

      If the `index` meta-database (see section [3.4. Index Meta-Database](#h.3.4)) is implemented by the provider,
      the `index_base_url` field MUST be included.

  `meta` MAY OPTIONALLY also include these fields:

  * **data\_available**: an integer containing the total number of data objects
    available in the database.
  * **last\_id**: a string containing the last ID returned.
  * **response\_message**: response string from the server.
  * **implementation**: a dictionary describing the server implementation, containing
    the OPTIONAL fields:
    * **name**: name of the implementation.
    * **version**: version string of the current implementation.
    * **source_url**: URL of the implementation source, either downloadable archive
      or version control system.
    * **maintainer**: a dictionary providing details about the maintainer of the
      implementation, MUST contain the single field **email** with the maintainer's
      email address.
  * **warnings**: a list of warning resource objects representing non-critical errors or warnings.  
    A warning resource object is defined similarly to a [JSON API error object](http://jsonapi.org/format/1.0/#error-objects), but MUST also include the field `type`, which MUST have the value `"warning"`.
    The field `detail` MUST be present and SHOULD contain a non-critical message, e.g., reporting unrecognised search attributes or deprecated features.  
    The field `status`, representing a HTTP response status code, MUST NOT be present for a warning resource object.
    This is an exclusive field for error resource objects.

    Example:  
    For a deprecation warning

    ```jsonc
    {
      "id": "dep_chemical_formula_01",
      "type": "warning",
      "code": "_exmpl_dep_chemical_formula",
      "title": "Deprecation Warning",
      "detail": "chemical_formula is deprecated, use instead chemical_formula_hill"
    }
    ```

    **Note**: `id`s MUST NOT be trusted to identify the exceptional situations
    (i.e., they are not error codes, use instead the field `code` for this.
    `id`s can _only_ be trusted to be unique in the list of warning resource
    objects, i.e., together with the `type`.  
    General OPTiMaDe warning codes are specified in [3.3.5. Warnings](#h.3.3.5).  

  * Other OPTIONAL additional information _global to the query_ that is not specified
  in this document, MUST start with a database-provider-specific prefix as defined in
  [Appendix 1](#h.app1).

  * Example:  
    For a request made to <http://example.com/optimade/v0.9/structures/?filter=a=1> AND b=2

    ```jsonc
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
    ```

* **data**: The schema of this value varies by endpoint, it can be either a _single_
[JSON API resource object](http://jsonapi.org/format/1.0/#document-resource-objects)
or a _list_ of JSON API resource objects. Every resource object needs the `type` and `id` fields,
and its attributes (described in section [4. API Endpoints](#h.4))
need to be in a dictionary corresponding to the `attributes` field.

The response MAY OPTIONALLY also return resources related to the primary data in the field:

* **links**: a [JSON API links member](http://jsonapi.org/format/1.0/#document-links)
  containing the JSON API links objects:
  * **next**: is an URI that represents a suggested way to fetch the
    next set of results if not all were returned, either directly as a string,
    or as a link object. The field MUST be null or omitted if there is no additional
    data, or if there is no way to fetch additional data. The link object can contain
    the following members:
    * **href**: a string containing the link’s URL.
    * **meta**: a meta object containing non-standard meta-information about the link.

  * **base\_url**: a links object representing the base URL of the implementation. Example:

    ```jsonc
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
    ```

* **included**: a list of
[JSON API resource objects](http://jsonapi.org/format/1.0/#document-resource-objects)
related to the primary data contained in `data`.  
A response with related resources under `included` are in the JSON API known as
[compound documents](https://jsonapi.org/format/1.0/#document-compound-documents).

If there were errors in producing the response all other fields MAY be present, but the top-level `data` field MUST be skipped, and the following field MUST be present:

* **errors**: a list of [JSON API error objects](http://jsonapi.org/format/1.0/#error-objects), where the field `detail` MUST be present.
All other fields are OPTIONAL.


An example of a full response:

```jsonc
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
      "index_base_url": "http://example.com/optimade/index/"
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
```

### <a name="h.3.3.3">3.3.3. HTTP Response Status Codes</a>

All HTTP response status codes MUST conform to [RFC 7231: HTTP Semantics](http://tools.ietf.org/html/rfc7231).
The code registry is maintained by IANA and can be found [here](http://www.iana.org/assignments/http-status-codes).

See also the JSON API definitions of responses when [fetching](https://jsonapi.org/format/1.0/#fetching) data, i.e., sending a `GET` request.

**Important**:
If a client receives an unexpected 404 error when making a query to a base URL,
and is aware of the index meta-database that belongs to the database provider
(as described in [3.4. Index Meta-Database](#h.3.4)),
the next course of action SHOULD be to fetch the resource objects under the
`links` endpoint of the index meta-database and redirect the original query
to the corresponding database ID that was originally queried, using the object's
`base_url` value.

### <a name="h.3.3.4">3.3.4. Unset optional properties</a>

Unset optional properties in a database are properties that exist and have a specific value within a database for some materials entries, but are undefined for other entries, e.g. have the value `null` within a JSON file.

Unset properties MUST NOT be returned in the response, unless explicitly requested in the search query. 

Any comparisons involving unset properties MUST be evaluated as `false`,
i.e. by definition the value of `null` is outside of any defined search range.

If a property is explicitly requested in a search query without value range filters,
then all entries otherwise satisfying the query SHOULD be returned, including those with `null` values for this property.
These properties MUST be set to `null` in the response.

Entries with unset or set property values can be filtered out of the response using:
```
identifier IS KNOWN
identifier IS UNKNOWN
```
respectively, as specified in section [5.2. The Filter Language Syntax](#h.5.2). 

The text in this section describes how the API handles properties that are `null`. 
It does not regulate the handling of values inside property data structures that can be `null`. 
The use of `null` values inside property data structures are described in the definitions of those data structures elsewhere in the specification.

### <a name="h.3.3.5">3.3.5. Warnings</a>

Non-critical exceptional situations occurring in the implementation SHOULD be reported to the referrer as warnings.
Warnings MUST be expressed as a human-readable message, OPTIONALLY coupled with a warning code.

Warning codes starting with an alphanumeric character are reserved for general OPTiMaDe error codes (currently, none are specified).
For implementation-specific warnings, they MUST be start with `_` and the database-provider-specific prefix as defined in [Appendix 1](#h.app1).

## <a name="h.3.4">3.4. Index Meta-Database</a>

The main purpose of this "index" is to allow for automatic discoverability
of all databases of a given provider.
Thus, it acts as a meta-database for the database provider's implementation(s).

The index meta-database MUST only provide the `info` and `links` endpoints,
see sections [4.3. Info Endpoints](#h.4.3) and [4.4. Links Endpoint](#h.4.4).
It MUST not expose any entry listing endpoints (e.g., `structures`).

These endpoints do not need to be queryable, i.e., they MAY be provided as static JSON files.
However, they MUST return the correct and updated information on all currently provided implementations.

The `index_base_url` field MUST be included in every response in the `provider` field under the
top-level `meta` field (see section [3.3.2. JSON API Response Schema: Common Fields](#h.3.3.2)).

The `is_index` field under `attributes`, as well as the `relationships` field, MUST be included in the
`info` endpoint for the index meta-database (see section [4.3.1. Base URL Info Endpoint](#h.4.3.1)).
The value for `is_index` MUST be `true`.

> **Note**: A list of database providers acknowledged by the
> **Open Databases Integration for Materials Design** consortium can be found in [Appendix 1](#h.app1).
> This list is also machine-readable, optimizing the automatic discoverability.

# <a name="h.4">4. API Endpoints</a>

The URL component that follows the base URL MUST represent one of the
following endpoints:

* an "entry listing" endpoint
* a "single entry" endpoint
* an introspection `info` endpoint
* a `links` endpoint to discover related implementations
* a custom `extensions` endpoint prefix  

These endpoints are documented below.

## <a name="h.4.1">4.1. Entry Listing Endpoints</a>

Entry listing endpoints return a list of resource objects representing entries of a
specific type. For example, a list of structures, or a list of calculations.

Examples:

* <http://example.com/optimade/v0.9/structures>
* <http://example.com/optimade/calculations>

There MAY be multiple entry listing endpoints, depending on how many types of
entries an implementation provides. Specific standard entry types are specified in
section [6. Entry list](#h.6). The API implementation MAY provide other
entry types than the ones standardized in this specification, but such entry
types MUST be prefixed by a database-provider-specific prefix.

### <a name="h.4.1.1">4.1.1. URL Query Parameters</a>

The client MAY provide a set of URL query parameters in order to alter
the response and provide usage information. While these URL query
parameters are OPTIONAL for clients, API implementations MUST accept and
handle them. To adhere to the requirement on implementation-specific
URL query parameters of [JSON API v1.0](http://jsonapi.org/format/1.0), query
parameters that are not standardized by that specification have been
given names that consist of at least two words separated by an
underscore (a LOW LINE character '\_').

Standard OPTIONAL URL query parameters standardized by the JSON API specification:

* **filter**: a filter string, in the format described below in section
  [5. API Filtering Format Specification](#h.5).

Standard OPTIONAL URL query parameters not in the JSON API specification:

* **response\_format**: specifies which output format is requested. Specifically, the
  format string 'jsonapi' specifies the standard output format documented
  in this specification as the JSON API response format.  
  Example: <http://example.com/optimade/v0.9/structures?response_format=xml>
* **email\_address**: specifies an email address of the user making the request. The
  email SHOULD be that of a person and not an automatic system.  
  Example: <http://example.com/optimade/v0.9/structures?email_address=user@example.com>
* **response\_limit**: sets a numerical limit on the number of entries returned. The API
  implementation MUST return no more than the number specified. It MAY return
  less. The database MAY have a maximum limit and not accept larger numbers (in
  which case an error code MUST be returned). The default limit value is up
  to the API implementation to decide.  
  Example: <http://example.com/optimade/v0.9/structures?response_limit=100>
* **response\_fields**: specify a comma-delimited set of fields to be provided in the
  output. If provided, only these fields MUST be returned and no others.  
  Example: <http://example.com/optimade/v0.9/structures?response_fields=id,url>

Additional OPTIONAL URL query parameters not described above are not
considered to be part of this standard, and are instead considered to
be "custom URL query parameters". These custom URL query parameters
MUST be of the format "&lt;database-provider-specific
prefix&gt;&lt;url\_query\_parameter\_name&gt;".  These names adhere to
the requirements on implementation-specific query parameters of
[JSON API v1.0](http://jsonapi.org/format/1.0) since the database-provider-specific prefixes
contain at least two underscores (a LOW LINE character '\_').

Example uses of custom URL query parameters include providing an access token for the
request, to tell the database to increase verbosity in error output, or
providing a database-specific extended searching format.

Examples:

* <http://example.com/optimade/v0.9/structures?_exmpl_key=A3242DSFJFEJE>
* <http://example.com/optimade/v0.9/structures?_exmpl_warning_verbosity=10>
* http://example.com/optimade/v0.9/structures?_exmpl_filter="elements all in [Al, Si, Ga]"

> **Note**: the specification presently makes no attempt to standardize access
> control mechanisms. There are security concerns with access control based on
> URL tokens, and the above example is not to be taken as a recommendation for
> such a mechanism.

### <a name="h.4.1.2">4.1.2. JSON API Response Schema</a>

"Entry listing" endpoint response dictionaries MUST have a `data`
key. The value of this key MUST be a list containing dictionaries that
represent individual entries. In the JSON API format every dictionary
([resource object](http://jsonapi.org/format/1.0/#document-resource-objects))
MUST have the following fields:

* **type**: field containing the Entry type as defined in section [2. Term Definition](#h.2)
* **id**: field containing the ID of entry as defined in section [2. Term Definition](#h.2).
  This can be the local database ID.
* **attributes**: a dictionary, containing key-value pairs representing the
  entry's properties and the following fields:
  * **local\_id**: the entry's local database ID (having no OPTiMaDe requirements/conventions)
  * **last\_modified**: an [ISO 8601](https://www.iso.org/standard/40874.html)
    representing the entry's last modification time
  * **immutable\_id**: an OPTIONAL field containing the entry's immutable ID (e.g., an UUID).
  This is important for databases having preferred IDs that point to "the latest version" of a
  record, but still offer access to older variants. This ID maps to the version-specific record,
  in case it changes in the future.

  Database-provider-specific properties need to include the database-provider-specific prefix
  (see [Appendix 1](#h.app1)).

OPTIONALLY it can also contains the following fields:

* **links**: a [JSON API links object](http://jsonapi.org/format/1.0/#document-links) can OPTIONALLY
contain the field
  * **self**: the entry's URL
* **meta**: a [JSON API meta object](https://jsonapi.org/format/1.0/#document-meta) that contains
non-standard meta-information about the object
* **relationships**: a dictionary containing references to other resource objects as defined in
[6.6. Relationships Used by Multiple Entry Types](#h.6.6)

Example:

```jsonc
{
  "data": [
    {
      "type": "structure",
      "id": "example.db:structs:0001",
      "attributes": {
        "formula": "Es2 O3",
        "local_id": "example.db:structs:0001",
        "url": "http://example.db/structs/0001",
        "immutable_id": "http://example.db/structs/0001@123",
        "last_modified": "2007-04-05T14:30Z"
      }
    },
    {
      "type": "structure",
      "id": "example.db:structs:1234",
      "attributes": {
        "formula": "Es2",
        "local_id": "example.db:structs:1234",
        "url": "http://example.db/structs/1234",
        "immutable_id": "http://example.db/structs/1234@123",
        "last_modified": "2007-04-07T12:02Z"
      },
    },
    // ...
  ]
  // ...
}
```

## <a name="h.4.2">4.2. Single Entry Endpoints</a>

A client can request a specific entry by appending an ID component to the URL of an entry listing
endpoint. This will return properties for the entry with that ID.

If using the JSON API format, the ID component MUST be the content of the `id` field.

Note that entries cannot have an ID of `'info'`, as this would collide with the 'Info' endpoint
(described in section [4.4. Info Endpoints](#h.4.4)) for a given entry type.

Examples:

* <http://example.com/optimade/v0.9/structures/exmpl:struct_3232823>
* <http://example.com/optimade/v0.9/calculations/232132>

### <a name="h.4.2.1">4.2.1. URL Query Parameters</a>

The client MAY provide a set of additional URL query parameters for this endpoint type.
URL query parameters not recognized MUST be ignored. While the following URL query parameters
are OPTIONAL for clients, API implementations MUST accept and handle them:
**response\_format**, **email\_address**, **response\_fields**. The meaning of these URL query parameters are as defined above in section [4.1.1. URL Query Parameters](#h.4.1.1).

### <a name="h.4.2.2">4.2.2. JSON API Response Schema</a>

The response for a 'single entry' endpoint is the same as for 'entry listing'
endpoint responses, except that the value of the `data` field MUST have only one or zero entries.
If using the JSON API format, this means that the response type of the `data` field MUST be
a single response object or `null` if there is no response object to return.

Example:

```jsonc
{
  "data": {
    "type": "structure",
    "id": "example.db:structs:1234",
    "attributes": {
      "formula": "Es2",
      "local_id": "example.db:structs:1234",
      "url": "http://example.db/structs/1234",
      "immutable_id": "http://example.db/structs/1234@123",
      "last_modified": "2007-04-07T12:02Z"
    },
  },
  "meta": {
    "query": {
      "representation": "/structures/example.db:structs:1234?"
    },
    // ...
  }
  // ...
}
```

## <a name="h.4.3">4.3. Info Endpoints</a>

Info endpoints provide introspective information, either about the API implementation itself,
or about specific entry types.

Info endpoints are constructed by appending "**info**" to any of:

1. the base URL (e.g., <http://example.com/optimade/v0.9/info/>)
2. type-specific entry listing endpoints (e.g., <http://example.com/optimade/v0.9/structures/info/>)

The types and output content of these info endpoints are described in more detail in the subsections
below. Common for them all are that the `data` field SHOULD return only a single resource object.
If no resource object is provided, the value of the `data` field MUST be `null`.

### <a name="h.4.3.1">4.3.1. Base URL Info Endpoint</a>

The Info endpoint on the base URL or directly after the version number (e.g.
<http://example.com/optimade/v0.9/info>) returns information relating to the API
implementation.

The single resource object's response dictionary MUST include the following fields:

* **type**: `"info"`
* **id**: `"/"`
* **attributes**: Dictionary containing the following fields:
  * **api\_version**: Presently used version of the OPTiMaDe API.
  * **available\_api\_versions**: Dictionary where values are the base URLs for the versions of the
  API that are supported, and the keys are strings giving the full version number provided by that
  base URL. Provided base URLs MUST adhere to the rules in section [3.1. Base URL](#h.3.1).
  * **formats**: List of available output formats.
  * **entry\_types\_by\_format**: Available entry endpoints as a function of output formats.
  * **available\_endpoints**: List of available endpoints (i.e., the string to be appended to the
  base URL).

  `attributes` MAY also include the following OPTIONAL fields:

  * **is\_index**: if `true`, this is an index meta-database base URL (see section
  [3.4. Index Meta-Database](#h.3.4)).

    If this member is *not* provided, the client MUST assume this is **not** an index meta-database
    base URL (i.e., default: `"is_index": false`).

If this is an index meta-database base URL (see section [3.4. Index Meta-Database](#h.3.4)), then the
response dictionary MUST also include the field:

* **relationships**: Dictionary that MAY contain a single
[JSON API relationships object](https://jsonapi.org/format/1.0/#document-resource-object-relationships):
  * **default**: Reference to the `child` object under the `links` endpoint that the provider
  has chosen as their "default" OPTiMaDe API database. A client SHOULD present this database as the
  first choice when an end-user chooses this provider.
  This MUST include the field:
    * **data**: [JSON API resource linkage](http://jsonapi.org/format/1.0/#document-links).
    It MUST be either `null` or contain a single `child` identifier object with the fields:
      * **type**: `child`
      * **id**: ID of the provider's chosen default OPTiMaDe API database. MUST be equal to a valid
      `child` object's `id` under the `links` endpoint.

  Lastly, `is_index` MUST also be included in `attributes` and be `true`.

Example:

```jsonc
{
  "data": {
    "type": "info",
    "id": "/",
    "attributes": {
      "api_version": "v0.9",
      "available_api_versions": {
        "0.9.5": "http://db.example.com/optimade/v0.9/",
        "0.9.2": "http://db.example.com/optimade/v0.9.2/",
        "1.0.2": "http://db.example.com/optimade/v1.0/"
      },
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
  },
  // ...
}
```

Example for an index meta-database:

```jsonc
{
  "data": {
    "type": "info",
    "id": "/",
    "attributes": {
      "api_version": "v0.9.8",
      "available_api_versions": {
        "0.9.5": "http://example.com/optimade/v0.9/",
        "0.9.2": "http://example.com/optimade/v0.9.2/",
        "1.0.2": "http://example.com/optimade/v1.0/"
      },
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
  },
  // ...
}
```

### <a name="h.4.3.2">4.3.2. Entry Listing Info Endpoints</a>

Entry listing info endpoints are of the form "&lt;base\_url&gt;/&lt;entry\_type&gt;/info/"
(e.g., <http://example.com/optimade/v0.9/structures/info/>).  
The response for these endpoints MUST include the following information in the `data` field:

* **description**: Description of the entry.
* **properties**: A dictionary describing queryable properties for this entry type,
where each key is a property ID. Each value is a dictionary, with the *required* key `description`
and *optional* key `unit`.
* **formats**: List of output formats available for this type of entry.
* **output\_fields\_by\_format**: Dictionary of available output fields for this entry type,
where the keys are the values of the `formats` list and the values are the keys of the `properties`
dictionary.

Example:

```jsonc
{
  "data": {
    "description": "a structure",
    "properties": {
      "nelements": {
        "description": "Number of elements"
      },
      "lattice_vectors": {
        "description": "Unit cell lattice vectors",
        "unit": "Å"
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
  },
  // ...
}
```

## <a name="h.4.4">4.4. Links Endpoint</a>

This endpoint exposes information on other OPTiMaDe API implementations that are linked to the current
implementation. The endpoint MUST be provided at the path "&lt;base_url&gt;/links".

It may be considered an introspective endpoint, similar to the Info endpoint, but at a higher level:
that is, Info endpoints provide information on the given implementation, while the Links endpoint
provides information on the links between immediately related implementations (in particular, an array
of none or a single `"parent"` object and none or more `"child"` objects, see section [4.5.2 Parent and Child Objects](#h.4.4.2)).

For Links endpoints, the API implementation MAY ignore any provided query parameters.
Alternatively, it MAY optionally handle the parameters specified in section
[4.2.1. URL Query Parameters](#h.4.2.1) for single entry endpoints.

### <a name="h.4.4.1">4.4.1. JSON API Response Schema</a>

The resource objects' response dictionaries MUST include the following fields:

* **type**: MUST be either `"parent"`, `"child"`, or `"provider"`.  
  These objects are described in detail in sections [4.4.2. Parent and Child Objects](#h.4.4.2)
  and [4.4.3. Provider Objects](#h.4.4.3).
* **id**: MUST be unique.
* **attributes**: Dictionary that MUST contain the following fields:
  * **name**: Human-readable name for the OPTiMaDe API implementation a client may provide in a list
  to an end-user.
  * **description**: Human-readable description for the OPTiMaDe API implementation a client may
  provide in a list to an end-user.
  * **base\_url**: [JSON API links object](http://jsonapi.org/format/1.0/#document-links),
  pointing to the base URL for this implementation, either directly as a string, or as a links object,
  which can contain the following fields:
    * **href**: a string containing the OPTiMaDe base URL.
    * **meta**: a meta object containing non-standard meta-information about the implementation.

  `attributes` MAY also contain the following OPTIONAL members:

  * **local\_id**: String representing the provider's local ID for the implementation.
  This MAY be different from the `id` field's value.

Example:

```jsonc
{
  "data": [
    {
      "type": "parent",
      "id": "index",
      "attributes": {
        "name": "Index",
        "description": "Index for example's OPTiMaDe databases",
        "base_url": "http://example.com/optimade/index"
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
        "local_id": "catalytic_zeolites"
      }
    },
    {
      "type": "child",
      "id": "frameworks",
      "attributes": {
        "name": "Zeolitic Frameworks",
        "description": "",
        "base_url": "http://example.com/optimade/zeo_frameworks",
        "local_id": "zeo_frameworks"
      }
    },
    {
      "type": "provider",
      "id": "exmpl",
      "attributes": {
        "name": "Example provider",
        "description": "Provider used for examples, not to be assigned to a real database",
        "base_url": "http://example.com/optimade/index"
      }
    },
    // ... <other objects>
  ],
  // ...
}
```

### <a name="h.4.4.2">4.4.2. Parent and Child Objects</a>

Resource objects that MAY be present under the Links endpoint.

Either none or a single `"parent"` object MAY be present as part of the `data` array.
The `"parent"` object represents a "link" to the OPTiMaDe implementation exactly one layer **above**
the current implementation's layer.

Any number of `"child"` objects MAY be present as part of the `data` array. A `"child"` object
represents a "link" to an OPTiMaDe implementation exactly one layer **below** the current
implementation's layer.

> **Note**: The RECOMMENDED number of layers is two.

### <a name="h.4.4.3">4.4.3. Provider Objects</a>

`"provider"` objects are meant to indicate links to an "Index meta-database" hosted by database
providers. The intention is to be able to auto-discover all providers of OPTiMaDe implementations.

A known list of providers can be found in [Appendix 1](#h.app1).

> **Note**: If a provider wishes to be added to `"provider.json"`, please suggest a change to the OPTiMaDe main repository (make a pull request).
A link to the main repository may be found at the [OPTiMaDe homepage](http://www.optimade.org).

### <a name="h.4.4.4">4.4.4. Index Meta-Database Links Endpoint</a>

If the provider implements an "Index meta-database" (see section [3.4 Index Meta-Database](#h.3.4)),
it is RECOMMENDED to adopt a structure, where the index meta-database is the "parent" implementation
of the provider's other OPTiMaDe databases.

This will make all OPTiMaDe databases and implementations by the provider discoverable as `"child"`
objects under the Links endpoint of the "Index meta-database".

## <a name="h.4.5">4.5. Custom Extension Endpoints</a>

API implementors can provide custom endpoints under the Extensions endpoint.
They should have the form "&lt;base\_url&gt;/extensions/&lt;custom paths&gt;".

# <a name="h.5">5. API Filtering Format Specification</a>

An OPTiMaDe filter expression is passed in the parameter `filter`
as an URL query parameter as 
[specified by JSON API](https://jsonapi.org/format/1.0/#fetching-filtering).
The filter expression allows desired properties to be compared against search
values; several such comparisons can be combined using the logical
conjunctions AND, OR, NOT, and parentheses, with their usual
semantics.

When provided as an URL query parameter, the contents of the
`filter` parameter is URL-encoded by the client in the HTTP GET
request, and then URL-decoded by the API implementation before any
further parsing takes place. In particular, this means the client MUST
escape special characters in string values as described below in the
section "String values" before the URL encoding, and the API
implementation MUST first URL-decode the `filter` parameter before
reversing the escaping of string tokens.

Examples of syntactically correct query strings embedded in queries:

* `http://example.org/optimade/v0.9/structures?filter=_exmpl_melting_point%3C300+AND+ nelements=4+AND+elements="Si,O2"&response_format=xml`

Or, fully URL encoded :

* `http://example.org/optimade/v0.9/structures?filter=_exmpl_melting_point%3C300+AND+nelements%3D4+AND+elements%3D%22Si%2CO2%22&response_format=xml`

## <a name="h.5.1">5.1. Lexical Tokens</a>

The following tokens are used in the filter query component:

* **Property names** (see section [6. Entry List](#h.6)): the first
  character MUST be a lowercase letter, the subsequent symbols MUST be
  composed of lowercase letters or digits; the underscore ("\_", ASCII
  95 dec (0x5F)) is considered to be a lower-case letter when defining
  identifiers.  The length of the identifiers is not limited, except
  that when passed as a URL query parameter the whole query SHOULD NOT
  be longer than the limits imposed by the URI specification. This
  definition is similar to one used in most widespread programming
  languages, execpt that OPTiMaDe limits allowed letter set to
  lowercase letters only. This allows to tell OPTiMaDe identifiers and
  operator keywords apart unambiguously without consulting and
  reserved word tables and to encode this disinction consicely in the
  EBNF Filter Language grammar.

  Examples of valid property names:

  * `band_gap`
  * `cell_length_a`
  * `cell_volume`

  Examples of incorrect property names:

  * `0_kvak` (starts with a number);
  * `"foo bar"` (contains space; contains quotes)
  * `"BadLuck"` (contains upper-case letters)

  Identifiers that start with an underscore are specific to a database provider,
  and MUST be on the format of a database-provider-specific prefix as defined in [Appendix 1](#h.app1).


  Examples:

    * `_exmpl_formula_sum` (a property specific to that database)
    * `_exmpl_band_gap`
    * `_exmpl_supercell`
    * `_exmpl_trajectory`
    * `_exmpl_workflow_id`  

* **Nested property names** MUST contain at least two property names joined by
  periods (`.`). When query is performed on relationships, the entrypoint name
  of the relationship is used as the name of the first property.

  Nested property names are similar to
  [JSONPaths](https://goessner.net/articles/JsonPath/) in a sense that they are
  used to access nested JSON data structures. A nested property name MUST be
  resolved starting either from `attributes` dictionary of an entry or from
  `relationships`, depending on where the first part of the path is found.
  When reached, every list is flattened, and the resolution continues for every
  list member.

  Examples:

    * `authors.name`
    * `references.authors.name` (`references` is an entrypoint name)

* **String values** MUST be enclosed in double quotes ("", ASCII symbol 92
    dec, 0x5C hex). The quote and other special characters within the double
    quotes MUST be escaped using C/JSON/Perl/Python convention: a double quote
    which is a part of the value, not a delimiter, MUST be prepended with a
    backslash character ("\\", ASCII symbol), and the backslash character
    itself, when taken literally, MUST be preceded by another
    backslash. An example of the escaped string value is given below:
  
      * "A double quote character (""", ASCII symbol 92 dec) MUST be prepended by
        a backslash ("\\", ASCII symbol 92 dec) when it is a part of the value and
        not a delimiter; the backslash character "\\" itself MUST be preceded by
        another backslash, forming a double backslash: \\\\"

    (Note that at the end of the string value above the four final backslashes
    represent the two terminal backslashes in the value, and the final double
    quote is a terminator, it is not escaped).

* **Numeric values** are represented as decimal integers or in scientific
  notation, using the usual programming language conventions. 
    A regular expression giving the number syntax is given below as a [POSIX Extended
  Regular Expression (ERE)](https://en.wikipedia.org/w/index.php?title=Regular_expression&oldid=786659796#Standards)
  or as a [Perl-Compatible Regular Expression (PCRE)](http://www.pcre.org):

      * ERE: `[-+]?([0-9]+(\.[0-9]\*)?|\.[0-9]+)([eE][-+]?[0-9]+)?`
      * PCRE: `[-+]?(?:\d+(\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?`

  An implementation of the search filter MAY reject numbers that are outside
  the machine representation of the underlying hardware; in such case it MUST
  return the error `501 Not Implemented` with an appropriate error message
  that indicates the cause of the error and an acceptable number range.

  * Examples of valid numbers:

    * 12345, +12, -34, 1.2, .2E7, -.2E+7, +10.01E-10, 6.03e23, .1E1, -.1e1, 1.e-12, -.1e-12,
    1000000000.E1000000000, 1., .1

  * Examples of _invalid_ numbers (although they MAY contain correct numbers as substrings):

    * 1.234D12, .e1, -.E1, +.E2, 1.23E+++, +-123

  * **Note**: this number representation is more general than the number representation
    in JSON (for instance, `1.` is a valid numeric value for the filtering language
    specified here, but is not a valid float number in JSON, where one must write `1.0` instead).

  While the filtering language supports tests for equality between
  properties of floating point type and decimal numbers given in the
  filter string, such comparisons come with the usual caveats for
  testing for equality of floating point numbers. Normally, a client
  cannot rely on that a floating point number stored in a database
  takes on a representation that exactly matches the one obtained
  for a number given in the filtering string as a decimal number or
  as an integer. However, testing for equality to zero MUST be supported.

  More examples of the number tokens and machine-readable definitions and tests can be found in the
  [Materials-Consortia API Git repository](https://github.com/Materials-Consortia/API/)
  (files
  [integers.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/integers.lst),
  [not-numbers.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/not-numbers.lst),
  [numbers.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/numbers.lst),
  and
  [reals.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/reals.lst)).

* **Operator tokens** are represented by usual mathematical relation symbols or by
  case-sensitive keywords. Currently the following operators are supported: `=`,
  `!=`, `<=`, `>=`, `<`, `>` for tests of number or string (lexicographical) equality,
  inequality, less-than, more-than, less, and more relations; `AND`, `OR`, `NOT` for
  logical conjunctions, and a number of keyword operators discussed in the next
  section.

  In future extensions, operator tokens that are words MUST contain
  only upper-case letters. This requirement guarantees that no
  operator token will ever clash with a property name.

## <a name="h.5.2">5.2. The Filter Language Syntax</a>

All filtering expressions MUST follow the
[EBNF](http://standards.iso.org/ittf/PubliclyAvailableStandards/s026153_ISO_IEC_14977_1996(E).zip)
grammar of [Appendix 2](#h.app2) of this specification. The appendix
contains a complete machine-readable EBNF, including the definition
of the lexical tokens described above in [section '5.1. Lexical
tokens'](#h.5.1). The EBNF is enclosed in special strings constructed
as `BEGIN` and `END`, both followed by `EBNF GRAMMAR Filter`, to enable automatic
extraction.

### Basic boolean operations

The filter language supports conjunctions of comparisons using the
boolean algebra operators "AND", "OR", and "NOT" and parentheses to
group conjunctions. A comparison clause prefixed by NOT matches
entries for which the comparison is false.

Examples:

* `NOT ( chemical_formula = "Al" AND prototype_formula = "A" OR prototype_formula = "H2O" AND NOT chemical_formula = "Ti" )`

### Numeric and String comparisons

Comparisons involving Numeric and String properties can be expressed
using the usual comparison operators: '<', '>', '<=', '>=', '=', '!='.
Implementations MUST support comparisons on the form:
```
identifier <operator> constant
constant <operator> identifier
```
Where 'identifier' is a property name and 'constant' is either a
numerical or string type constant. However, implementations MAY
OPTIONALLY support comparisons with identifiers also on both sides,
and comparisons with values on both sides, i.e., on the forms:
```
identifier <operator> identifier
constant <operator> constant
```

Examples:

* `nelements > 3`
* `chemical_formula = "H2O" AND prototype_formula != "AB"`
* `_exmpl_aax <= +.1e8 OR nelements >= 10 AND NOT ( _exmpl_x != "Some string" OR NOT _exmpl_a = 7)`
* `_exmpl_spacegroup="P2"`
* `_exmpl_cell_volume<100.0`
* `_exmpl_bandgap > 5.0 AND _exmpl_molecular_weight < 350`
* `_exmpl_melting_point<300 AND nelements=4 AND elements="Si,O2"`
* `_exmpl_some_string_property = 42` (This is syntactically allowed without putting 42 in quotation marks, see the notes about comparisons of values of different types below.)
* `5 < _exmpl_a`
* OPTIONAL: `((NOT (_exmpl_a>_exmpl_b)) AND _exmpl_x>0)`
* OPTIONAL: `5 < 7`

### Substring comparisons

In addition to the standard equality and inequality operators, matching of partial strings is provided by keyword operators:

* `identifier CONTAINS x`: Is true if the substring value x is found anywhere within the property.

* `identifier STARTS WITH x`: Is true if the property starts with the substring value x. The `WITH` keyword may be omitted.

* `identifier ENDS WITH x`: Is true if the property ends with the substring value x. The `WITH` keyword may be omitted.

OPTIONAL features: 

* Support for x to be an identifier, rather than a string is OPTIONAL.

Examples:

* `prototype_formula CONTAINS "C2" AND prototype_formula STARTS WITH "A2"` 
* `prototype_formula STARTS "B2" AND prototype_formula ENDS WITH "D2"`

### Comparisons of multi-valued properties

Multi-valued properties can be thought of as lists or sets of strings or numbers. 
In the following, a set of `values` is one or more strings or numbers separated by a comma (",").
An implementation MAY OPTIONALLY also support identifiers in the value set.

The following constructs MUST be supported:

* `identifier HAS value`: matches if the given value is present in the multi-valued property (i.e., set operator IN).
* `identifier HAS ALL values`: matches when all the values given are present in the multi-valued property (i.e., set operator >=).
* `identifier HAS, EXACTLY values`: matches when the property contains all the values given and none other (i.e., set operator =).
* `identifier HAS ANY values`: matches when any one of the values given are present in the property (i.e., equivalent with a number of HAS separated by OR).
* `LENGTH identifier <operator> value`: applies the numeric comparison operator for the number of items in the multi-valued property. 

The following construct may OPTIONALLY be supported:

* `identifier HAS ONLY values`: matches when the property only contains items from the given values (i.e., set operator <=)

This construct is optional as it may be difficult to realize in some
underlying database implementations. However, if the desired search is
over a property that can only take on a finite set of values (e.g.,
chemical elements) a client can formulate an equivalent search by inverting
the list of values into `inverse` and express the filter as `NOT identifier HAS
inverse`.

Furthermore, there is a set of OPTIONAL constructs that allows
searches to be formulated over the values in correlated positions in
multiple multi-valued properties. This type of filter may be useful if
one, e.g., has one multi-valued property of elements and another of an
element count.

* `id1:id2:... HAS val1:val2:...`
* `id1:id2:... HAS ALL val1:val2:...`
* `id1:id2:... HAS, EXACTLY val1:val2:...`
* `id1:id2:... HAS ANY val1:val2:...`
* `id1:id2:... HAS ONLY val1:val2:...`

Finally, all the above constructs that allow a value or lists of
values on the right-hand side may OPTIONALLY allow `<operator> value`
in each place a value can appear. In that case, a match requires that
the equality or inequality is fulfilled. For example:

* `identifier HAS < 3`: matches all entries for which "identifier" contains at least one element that is less than three.
* `identifier HAS ALL < 3, > 3`: matches only those entries for which "identifier" simultaneously 
   contains at least one element less than three and one element greater than three.

Examples:

* `elements HAS "H" AND elements HAS ALL "H","He","Ga","Ta" AND elements HAS EXACTLY "H","He","Ga","Ta" AND elements HAS ANY "H", "He", "Ga", "Ta"`
* OPTIONAL: `elements HAS ONLY "H","He","Ga","Ta"`
* OPTIONAL: `elements:_exmpl_element_counts HAS "H":6 AND elements:_exmpl_element_counts HAS ALL "H":6,"He":7 AND elements:_exmpl_element_counts HAS EXACTLY "H":6 AND elements:_exmpl_element_counts HAS ANY "H":6,"He":7 AND elements:_exmpl_element_counts HAS ONLY "H":6,"He":7`
* OPTIONAL: `_exmpl_element_counts HAS < 3 AND _exmpl_element_counts HAS ANY > 3, = 6, 4, != 8` (note: specifying the = operator after HAS ANY is redundant here, if no operator is given, the test is for equality.)
* OPTIONAL: `elements:_exmpl_element_counts:_exmpl_element_weights HAS ANY > 3:"He":>55.3 , = 6:>"Ti":<37.6 , 8:<"Ga":0`

### Properties that can be unset

The filter language can match properties that are not set. In the underlying data
representation, this usually means data is missing or is set to a 'null' value.
The format is as follows:
```
identifier IS KNOWN
identifier IS UNKNOWN
```
Which matches when the property is set, and unset, respectively.

Examples:

* `chemical_formula IS KNOWN AND NOT prototype_formula IS UNKNOWN`

### Precedence

The precedence (priority) of the operators MUST be as indicated in the list
below:

1.  Comparison and keyword operators (`<`, `<=`, `=`, `HAS`, `STARTS`, etc.) -- highest priority;
2.  `NOT`
3.  `AND`
4.  `OR` -- lowest priority.

Examples:

* `NOT a > b OR c = 100 AND f = "C2 H6"`: this is interpreted as `(NOT (a > b)) OR ( (c = 100) AND (f = "C2 H6") )` when fully braced.
* `a >= 0 AND NOT b < c OR c = 0`: this is interpreted as `((a >= 0) AND (NOT (b < c))) OR (c = 0)` when fully braced.

### Type handling and conversions in comparisons

The definitions of specific properties in this standard define
their types. Similarly, for database-provider-specific properties,
the database provider decides their types. In the syntactic
constructs that can accommodate values of more than one type, 
the semantics of the comparisons are controlled by the
types of the participating properties. Specifically:

* In a comparison of a property with a constant of a type that does
not match the type of the property, it is RECOMMENDED that the
implementation makes a best-effort to convert the constant to match
the property type. For example, `x > "0.0"` where x is a coordinate
would be treated as numeric filter `x > 0`, and `s = 0` for a String
parameter "s" would perform string comparison as in `s = "0"`.
Strings are converted to numbers using the token syntax specified in
[section '5.1. Lexical tokens'](#h.5.1), p. "Numeric values"; numbers
SHOULD be converted to strings using the libc "%g" format. If a
conversion is performed, the API implementation SHOULD supply a
warning in the response and specify the actual search values that were
used. Alternatively, the implementation MAY instead respond with error
`501 Not Implemented` with an explanation that specifies which
comparison generated the type mismatch. The implementation MUST either
make a conversion or respond with an error. It may not, e.g., silently
treat such comparisons as always non-matching.

* If a comparison is provided between only numerical constants of
incompatible types, e.g., `5 < "13"`, the implementation MUST respond
with an error. The same applies for comparisons of two properties, e.g.
`nelements > chemical_formula`.

### Optional filter features

Some features of the filtering language are marked OPTIONAL. An
implementation that encounters an optional feature that it does not
support MUST respond with error `501 Not Implemented` with an
explanation of which optional construct the error refers to.

# <a name="h.6">6. Entry List</a>

This section defines standard entry types and their properties.

## <a name="h.6.1">6.1. Properties Used by Multiple Entry Types</a>

### <a name="h.6.1.1">6.1.1. id</a>

* **Description**: An entry's ID as defined in section [2. Term Definition](#h.2).
* **Requirements/Conventions**:
  * See section [2. Term Definition](#h.2).
* **Examples**:
  * `"db/1234567"`
  * `"cod/2000000"`
  * `"cod/2000000@1234567"`
  * `"nomad/L1234567890"`
  * `"42"`

### <a name="h.6.1.2">6.1.2. type</a>

* **Description**: the type of an entry.
* **Requirements/Conventions**: MUST be an existing entry type.
* **Example**: `"structure"`

### <a name="h.6.1.3">6.1.3. last\_modified</a>

* **Description**: Date representing when the entry was last modified.
* **Requirements/Conventions**: String with [ISO 8601](https://www.iso.org/standard/40874.html) format.
* **Example**: `"2007-04-05T14:30Z"`
* **Querying**: Date-time queries are permitted ([RFC 3339](http://tools.ietf.org/html/rfc3339)).

### <a name="h.6.1.4">6.1.4. database-provider-specific properties</a>

* **Description**: Database providers are allowed to insert database-provider-specific entries
  in the output of both standard entry types and database-provider-specific entry types.
* **Requirements/Conventions**: These MUST be prefixed by a database-provider-specific prefix as
  defined in [Appendix 1](#h.app1).
* **Examples**:
  * \_exmpl\_formula\_sum
  * \_exmpl\_band\_gap
  * \_exmpl\_supercell
  * \_exmpl\_trajectory
  * \_exmpl\_workflow\_id

## <a name="h.6.2">6.2. Structure Entries</a>

`"structure"` entries (or objects) have the properties described above in section
[6.1. Properties Used by Multiple Entry Types](#h.6.1), as well as the following properties:

### <a name="h.6.2.1">6.2.1. elements</a>

* **Description**: Names of elements found in the structure. 
* **Requirements/Conventions**: String of chemical symbols of elements as strings as a multi-valued property.
* **Examples**:
  * `["Si"]`
  * `["Si","Al","O"]`
* **Querying**: e.g., all records pertaining to
  materials containing Si, Al **and** O, and possibly other elements can be
	obtained using the filter `elements HAS Si, Al, O`. To specify exactly
	these three elements, use `elements HAS EXACTLY Si, Al, O` or alternatively
	add `LENGTH elements = 3`.

### <a name="h.6.2.2">6.2.2. nelements</a>

* **Description**: Number of elements found in a structure.
* **Requirements/Conventions**: Integer value.
* **Example**: `3`
* **Querying**: queries on this property can equivalently be formulated using `LENGTH elements`.
  Examples:
  * return only entities that have exactly 4 elements: `"nelements=4"`
  * query for structures that have between 2 and 7 elements: `"nelements>=2+AND+nelements<=7"`

### <a name="h.6.2.3">6.2.3. chemical\_formula</a>

* **Description**: The chemical formula for a structure.
* **Requirements/Conventions**:
  * The formula MUST be **reduced**.
  * Element names MUST be with proper capitalization (e.g., `"Si"`, not `"SI"` for "silicon").
  * The order in which elements are specified SHOULD NOT be significant (e.g., "O2Si" is equivalent
    to "SiO2").
  * No spaces or separators are allowed.

### <a name="h.6.2.4">6.2.4. formula\_prototype</a>

* **Description**: The formula prototype obtained by sorting elements by the occurrence number in the
  **reduced** chemical formula and replace them with subsequent alphabet letters A, B, C, and so on.

### <a name="h.6.2.5">6.2.5. dimension\_types</a>

* **Description**: List of three integers. For each of the three directions indicated by the three
lattice vectors (see property [6.2.6. `lattice_vectors`](#h.6.2.6)). This list indicates if the
direction is periodic (value `1`) or non-periodic (value `0`). Note: the elements in this list each
refer to the direction of the corresponding entry in [6.2.6. `lattice_vectors`](#h.6.2.6) and *not*
the Cartesian x, y, z directions.
* **Requirements/Conventions**:
  * This property is REQUIRED.
  * It MUST be a list of length 3.
  * Each element MUST be an integer and MUST assume only the value `0` or `1`.
* **Examples**:
  * For a molecule: `[0, 0, 0]`
  * For a wire along the direction specified by the third lattice vector: `[0, 0, 1]`
  * For a 2D surface/slab, periodic on the plane defined by the first and third
    lattice vectors: `[1, 0, 1]`
  * For a bulk 3D system: `[1, 1, 1]`

### <a name="h.6.2.6">6.2.6. lattice\_vectors</a>

* **Description**: The three lattice vectors in Cartesian coordinates, in ångström (Å).
* **Requirements/Conventions**:
  * This property is REQUIRED, except when [6.2.5. `dimension_types`](#h.6.2.5) is equal to
  `[0, 0, 0]` (in this case it is OPTIONAL).
  * It MUST be a list of three vectors *a*, *b*, and *c*, where each of the vectors MUST BE a list of
  the vector's coordinates along the x, y, and z Cartesian coordinates. (Therefore, the first index
  runs over the three lattice vectors and the second index runs over the x, y, z Cartesian
  coordinates).
  * For databases that do not define an absolute Cartesian system (e.g., only defining the length and
  angles between vectors), the first lattice vector SHOULD be set along `x` and the second on the `xy`
  plane.
  * This property MUST be an array of dimensions 3 times 3 regardless of the elements of
  [6.2.5. `dimension_types`](#h.6.2.5). The vectors SHOULD by convention be chosen so the determinant
  of the `lattice_vectors` matrix is different from zero. The vectors in the non-periodic directions
  have no significance beyond fulfilling these requirements.
* **Examples**:
  * `[[4.0,0.0,0.0],[0.0,4.0,0.0],[0.0,1.0,4.0]]` represents a cell, where the first vector is
  `(4, 0, 0)`, i.e., a vector aligned along the `x` axis of length 4 Å; the second vector is
  `(0, 4, 0)`; and the third vector is `(0, 1, 4)`.

### <a name="h.6.2.7">6.2.7. cartesian\_site\_positions</a>

* **Description**: Cartesian positions of each site. A site is an atom, a site potentially occupied by
an atom, or a placeholder for a virtual mixture of atoms (e.g., in a virtual crystal approximation).
* **Requirements/Conventions**:
  * This property is REQUIRED.
  * It MUST be a list of length N times 3, where N is the number of sites in the structure.
  * An entry MAY have multiple sites at the same Cartesian position (for a relevant use of this, see
    e.g., the [6.2.10.`assemblies`](#h.6.2.10) property).
  * If a component of the position is unknown, the `null` value should be provided instead. 
    Otherwise, it should be a float value, expressed in angstrom. Note that if at least one
    of the coordinates is unknown, the correct flag MUST be set
    in the list `structure_features` (see section [6.2.11 `structure_features`](#h.6.2.11)).
* **Notes**: (for implementers) While this is unrelated to this OPTiMaDe specification:
  if you decide to store internally the `cartesian_site_positions` as a float array,
  you might want to replace `null` values with `NaN` values, the latter being valid float numbers
  in the IEEE 754 standard in [IEEE 754-1985](https://doi.org/10.1109/IEEESTD.1985.82928) and in the updated
  version [IEEE 754-2008](https://doi.org/10.1109/IEEESTD.2008.4610935).
* **Examples**:
  * `[[0,0,0],[0,0,2]]` indicates a structure with two sites, one sitting at the origin and one along
  the (positive) `z` axis, 2 Å away from the origin.

### <a name="h.6.2.8">6.2.8. species\_at\_sites</a>

* **Description**: Name of the species at each site (where values for sites are specified with the
same order of the [6.2.7. `cartesian_site_positions`](#h.6.2.7) property). The properties of the
species are found in the [6.2.9. `species`](#h.6.2.9) property.
* **Requirements/Conventions**:
  * This property is REQUIRED.
  * It MUST be a list of strings, which MUST have length equal to the number of sites in the structure
    (first dimension of the [6.2.7. `cartesian_site_positions`](#h.6.2.7) list).
  * Each string MUST be a valid key of the dictionary specified by the [6.2.9. `species`](#h.6.2.9)
    property. The requirements on this string are the same as for property names, i.e., it can be of any
    length, may use upper and lower case letters, underscore, and digits 0-9, but MUST NOT begin with a
    digit.
  * Each site MUST be associated only to a single species.  
    **Note**: However, species can represent mixtures of atoms, and multiple species MAY be defined
    for the same chemical element. This latter case is useful when different atoms of the same type
    need to be grouped or distinguished, for instance in simulation codes to assign different initial
    spin states).
* **Examples**:
  * `["Ti","O2"]` indicates that the first site is hosting a species labeled `"Ti"` and the second a
  species labeled `"O2"`.

### <a name="h.6.2.9">6.2.9. species</a>

* **Description**: Dictionary describing the species of the sites of this structure. Species can be
pure chemical elements, or virtual-crystal atoms representing a statistical occupation of a given site
by multiple chemical elements.
* **Requirements/Conventions**:
  * This property is REQUIRED.
  * It MUST be a dictionary, where keys represent the species' name, and values are themselves
  dictionaries with the following keys:
    * **chemical\_symbols**: REQUIRED; MUST be a list of strings of all chemical elements composing this species.
      * It MUST be one of the following:
        * a valid chemical-element name, or
        * the special value `"X"` to represent a non-chemical element, or
        * the special value `"vacancy"` to represent that this site has a non-zero probability of having
        a vacancy (the respective probability is indicated in the `concentration` list, see below).
      * If any one entry in the `species` list has a `chemical_symbols` list that 
        is longer than 1 element, the correct flag MUST be set
        in the list `structure_features` (see section [6.2.11 `structure_features`](#h.6.2.11)).
  

    * **concentration**: REQUIRED; MUST be a list of floats, with same length as `chemical_symbols`.
    The numbers represent the relative concentration of the corresponding chemical symbol in this
    species. The numbers SHOULD sum to one. Cases in which the numbers do not sum to one typically
    fall only in the following two categories:
      * Numerical errors when representing float numbers in fixed precision. E.g. for two chemical
      symbols with concentration `1/3` and `2/3`, the concentration might look something like
      `[0.33333333333, 0.66666666666]`. If the client is aware that the sum is not one because of
      numerical precision, it can renormalize the values so that the sum is exactly one.
      * Experimental errors in the data present in the database. In this case, it is the
      responsibility of the client to decide how to process the data.

      Note that concentrations are uncorrelated between different sites (even of the same species).

    * **mass**: OPTIONAL. If present MUST be a float expressed in a.m.u.
    * **original_name**: OPTIONAL. Can be any valid unicode string, and SHOULD contain (if specified)
    the name of the species that is used internally in the source database.  
    Note: With regards to "source database", we refer to the immediate source being queried via the
    OPTiMaDe API implemention. The main use of this field is for source databases that use species
    names, containing characters that are not allowed (see description of the
    [6.2.8. `species_at_sites`](#h.6.2.8) list).

  * For systems that have only species formed by a single chemical symbol, and that have at most one
  species per chemical symbol, SHOULD use the chemical symbol as species name (e.g., `"Ti"` for
  titanium, `"O"` for oxygen, etc.) However, note that this is OPTIONAL, and client implementations
  MUST NOT assume that the key corresponds to a chemical symbol, nor assume that if the species name
  is a valid chemical symbol, that it represents a species with that chemical symbol. This means that
  a species `"C": {"chemical_symbols": ["Ti"], "concentration": [1.0]}` is valid and represents a
  titanium species (and *not* a carbon species).
  * It is NOT RECOMMENDED that a structure includes species that do not have at least one
  corresponding site.
* **Examples**:
  * `"Ti": {"chemical_symbols": ["Ti"], "concentration": [1.0]}`: any site with this species is
  occupied by a Ti atom.
  * `"Ti": {"chemical_symbols": ["Ti", "vacancy"], "concentration": [0.9, 0.1]}`: any site with this
  species is occupied by a Ti atom with 90 % probability, and has a vacancy with 10 % probability.
  * `"BaCa": {"chemical_symbols": ["vacancy", "Ba", "Ca"], "concentration": [0.05, 0.45, 0.5], "mass": 88.5}`: any site with this species is occupied by a Ba atom with 45 % probability, a Ca atom with
  50 % probability, and by a vacancy with 5 % probability. The mass of this site is (on average) 88.5
  a.m.u.
  * `"C12": {"chemical_symbols": ["C"], "concentration": [1.0], "mass": 12.0}`: any site with this
  species is occupied by a carbon isotope with mass 12.
  * `"C13": {"chemical_symbols": ["C"], "concentration": [1.0], "mass": 13.0}`: any site with this
  species is occupied by a carbon isotope with mass 13.

### <a name="h.6.2.10">6.2.10. assemblies</a>

* **Description**: A description of groups of sites that are statistically correlated.
* **Requirements/Conventions**:
  * This key is OPTIONAL (it is absent if there are no partial occupancies).
  * If present, the correct flag MUST be set
    in the list `structure_features` (see section [6.2.11 `structure_features`](#h.6.2.11)).
  * Client implementations MUST check its presence (as its presence changes the
    interpretation of the structure).
  * If present, it MUST be a list of dictionaries, each of which represents an assembly and MUST have
  the following two keys:
    * **sites\_in\_groups**: Index of the sites (0-based) that belong to each group for each assembly.  
    Example: `[[1], [2]]`: two groups, one with the second site, one with the third.  
    Example: `[[1,2], [3]]`: one group with the second and third site, one with the fourth.
    * **group\_probabilities**: Statistical probability of each group. It MUST have the same length of
    `sites_in_groups`. It SHOULD sum to one. See below for examples of how to specify the probability
    of the occurrence of a vacancy. The possible reasons for the values not to sum to one are the same
    as already specified above for the `concentration` of each `species`, see section
    [6.2.9. `species`](#h.6.2.9).
  * If a site is not present in any group, it means that is is present with 100 % probability (as if
  no assembly was specified).
  * A site MUST NOT appear in more than one group.
* **Examples** (for each entry of the assemblies list):
  * `{"sites_in_groups": [[0], [1]], "group_probabilities: [0.3, 0.7]}`: the first site and the second
  site never occur at the same time in the unit cell. Statistically, 30 % of the times the first site
  is present, while 70 % of the times the second site is present.
  * `{"sites_in_groups": [[1,2], [3]], "group_probabilities: [0.3, 0.7]}`: The second and third site
  are either present together or not present; they form the first group of atoms for this assembly.
  The second group is formed by the fourth site. Sites of the first group (the second and the third)
  are never present at the same time as the fourth site. 30 % of times sites 1 and 2 are present (and
  site 3 is absent); 70 % of times site 3 is present (and sites 1 and 2 are absent).
* **Notes**:
  * Assemblies are essential to represent, for instance, the situation where an atom can statistically
  occupy two different positions (sites).
  * By defining groups, it is possible to represent, e.g., the case where a functional molecule (and
  not just one atom) is either present or absent (or the case where it it is present in two
  conformations)
  * Considerations on virtual alloys and on vacancies:  
  In the special case of a virtual alloy, these specifications allow two different, equivalent ways of
  specifying them. For instance, for a site at the origin with 30 % probability of being occupied by
  Si, 50 % probability of being occupied by Ge, and 20 % of being a vacancy, the following two
  representations are possible:
    * Using a single species:

      ```jsonc
      {
        "cartesian_site_positions": [[0,0,0]],
        "species_at_sites": ["SiGe-vac"],
        "species": {
          "SiGe-vac": {
            "chemical_symbols": ["Si", "Ge", "vacancy"],
            "concentration": [0.3, 0.5, 0.2]
          }
        }
        // ...
      }
      ```

    * Using multiple species and the assemblies:

      ```jsonc
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
      ```

  * It is up to the database provider to decide which representation to use, typically depending on
  the internal format in which the structure is stored. However, given a structure identified by a
  unique ID, the API implementation MUST always provide the same representation for it.
  * The probabilities of occurrence of different assemblies are uncorrelated. So, for instance in the following case with two assemblies:

    ```jsonc
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
    ```

    Site 0 is present with a probability of 20 % and site 1 with a probability of 80 %. These two
    sites are correlated (either site 0 or 1 is present). Similarly, site 2 is present with
    a probability of 30 % and site 3 with a probability of 70 %. These two sites are correlated
    (either site 2 or 3 is present).  
    However, the presence or absence of sites 0 and 1 is not correlated with the presence or absence
    of sites 2 and 3 (in the specific example, the pair of sites (0, 2) can occur with 0.2\*0.3 = 6 %
    probability; the pair (0, 3) with 0.2\*0.7 = 14 % probability; the pair (1, 2) with
    0.8\*0.3 = 24 % probability; and the pair (1, 3) with 0.8\*0.7 = 56 % probability).

### <a name="h.6.2.11">6.2.11. structure\_features</a>
* **Description**: A list of strings, flagging which special features are used by
  the structure.
* **Requirements/Conventions**: 
  * This property is REQUIRED.
  * This property MUST be returned as an empty list if no special features are used.
  * This list MUST be sorted alphabetically.  
  * If a special feature listed below is used, the corresponding string MUST be set.
  * If a special feature listed below is not used, the corresponding string MUST NOT be set. 
* **List of special structure features**:
  * `disorder`: This flag MUST be present if any one entry in the `species` list has a 
    `chemical_symbols` list that is longer than 1 element.
  * `unknown_positions`: This flag MUST be present if at least one component of the
    `cartesian_site_positions` list of lists has value `null`.
  * `assemblies`: This flag MUST be present if the [`assemblies`](#h.6.2.10)
    list is present.  
* **Querying**: This property MUST be queryable.
* **Examples**: A structure having unknown positions and using assemblies:

  ```jsonc
  ["assemblies", "unknown_positions"]
  ```

## <a name="h.6.3">6.3. Calculation Entries</a>

`"calculation"` entries have the properties described above in section
[6.1. Properties Used by Multiple Entry Types](#h.6.1).

## <a name="h.6.4">6.4. Reference Entries</a>

`"reference"` entries describe bibliographic references. The following properties
are used to provide the bibliographic details:
* **address**, **annote**, **booktitle**, **chapter**, **crossref**,
  **edition**, **howpublished**, **institution**, **journal**, **key**,
  **month**, **note**, **number**, **organization**, **pages**, **publisher**,
  **school**, **series**, **title**, **type**, **volume**, **year**: meanings
  of these properties match the
  [BibTeX specification](http://bibtexml.sourceforge.net/btxdoc.pdf), values
  are strings;
* **authors** and **editors**: lists of *person objects* which are dictionaries
  with the following fields:
  * **name**: full name of the person, REQUIRED.
  * **firstname**, **lastname**: parts of the person's name, OPTIONAL.
* **doi** and **url**: values are strings.

At least one of the aforementioned properties is REQUIRED.

Example:

```jsonc
{
  "data": {
    "type": "reference",
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
```

## <a name="h.6.5">6.5. Database-Provider-Specific Entry Types</a>

Names of database-provider-specific entry types MUST start with
database-provider-specific namespace prefix as given in [Appendix 1](#h.app1).
Database-provider-specific entry types MUST have all properties described above
in section [6.1. Properties Used by Multiple Entry Types](#h.6.1).

## <a name="h.6.6">6.6. Relationships Used by Multiple Entry Types</a>

[JSON API Relationships](https://jsonapi.org/format/1.0/#document-resource-object-relationships)
MAY be used to describe the relations between entries. A human-readable description
of a relationship MAY be provided using the `"description"` field inside the
`"meta"` dictionary of a relationship.

### <a name="h.6.6.1">6.6.1. References</a>

The `"references"` relationship is used to provide bibliographic references for any
of the entry types. It relates an entry with any number of `"reference"` entries.
Entries of type `"reference"`, if mentioned in the returned JSON document,
SHOULD be included in the top-level `"included"` field as per the
[JSON API 1.0 specification](https://jsonapi.org/format/1.0/#fetching-includes).

Example:

```jsonc
{
  "data": {
    "type": "structure",
    "id": "example.db:structs:1234",
    "attributes": {
      "formula": "Es2",
      "local_id": "example.db:structs:1234",
      "url": "http://example.db/structs/1234",
      "immutable_id": "http://example.db/structs/1234@123",
      "last_modified": "2007-04-07T12:02Z"
    },
    "relationships": {
      "references": {
        "data": [
          { "type": "reference", "id": "Dijkstra1968" },
          {
            "type": "reference",
            "id": "1234",
            "meta": {
              "description": "This article has been retracted"
            }
          }
        ]
      }
    },
  },
  "included": [
    {
      "type": "reference",
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
      "type": "reference",
      "id": "1234",
      "attributes": {
        "doi": "10.1234/1234"
      }
    }
  ]
}
```

### <a name="h.6.6.2">6.6.2. Calculations</a>

Relationships with calculations MAY be used to indicate provenance where a structure
is either an input to or an output of calculations.

> **Note**: We intend to implement in a future version of this API a
> standardized mechanism to differentiate these two cases, thus allowing
> databases a common way of exposing the full provenance tree with inputs
> and outputs between structures and calculations.
> 
> At the moment the database providers are suggested to extend their API the
> way they choose, always using their database-provider-specific prefix in
> non-standardized fields.

## <a name="h.app1">Appendix 1: Database-Provider-Specific Namespace Prefixes</a>

This standard refers to database-provider-specific prefixes.
These are assigned and included in this standard in the file `providers.json`.

API implementations SHOULD NOT make up and use new prefixes not included in this standard,
but SHOULD rather work to get such prefixes included in a future revision of this API specification.

**Example**:  
Database-provder-specific prefix: `"exmpl"`  
Use as a field name in a response: `_exmpl_custom_field`

The initial underscore indicates an identifier that is under a separate namespace under the ownership
of that organisation. Identifiers prefixed with underscores will not be used for standardized names.

The database-provider-specific prefixes currently assigned are listed in the `providers.json` file
provided in the main repository. This file serves as a machine-readable list of OPTiMaDe providers.

The content of the `providers.json` file follows the same JSON API specifications as the rest of the
API, in particular the resource objects under the top-level `data` field are defined to be valid
resource objects for the Links endpoint, see section [4.4.3. Provider Objects](#h.4.4.3).

> **Note**: If a provider wishes to be added to `providers.json`, please suggest a change to this
repository (make a PR).

## <a name="h.app2">Appendix 2: The Filter Language EBNF Grammar.</a>

```EBNF
(* BEGIN EBNF GRAMMAR Filter *)
(* The top-level 'filter' rule: *)

Filter = [Spaces], Expression ;

(* Values *)

Constant = String | Number ;

Value = String | Number | Identifier ;
(* Note: support for Identifier in Value is OPTIONAL *)

ValueList = [ Operator ], Value, { Comma, [ Operator ], Value } ;
(* Support for Operator in ValueList is OPTIONAL *)

ValueZip = [ Operator ], Value, Colon, [ Operator ], Value, {Colon, [ Operator ], Value} ;
(* Support for the optional Operator in ValueZip is OPTIONAL *)

ValueZipList = ValueZip, { Comma, ValueZip } ;

(* Expressions *)

Expression = ExpressionClause, [ OR, Expression ] ;

ExpressionClause = ExpressionPhrase, [ AND, ExpressionClause ] ;

ExpressionPhrase = [ NOT ], ( Comparison | PredicateComparison | OpeningBrace, Expression, ClosingBrace );

Comparison = ConstantFirstComparison |
             IdentifierFirstComparison ;
(* Note: support for ConstantFirstComparison is OPTIONAL *)

IdentifierFirstComparison = Identifier, ( 
                ValueOpRhs |
                KnownOpRhs |
                FuzzyStringOpRhs |
                SetOpRhs | 
                SetZipOpRhs );
(* Note: support for SetZipOpRhs in Comparison is OPTIONAL *)

ConstantFirstComparison = Constant, ValueOpRhs ;
				
PredicateComparison = LengthComparison ;

ValueOpRhs = Operator, Value ;

KnownOpRhs = IS, ( KNOWN | UNKNOWN ) ; 

FuzzyStringOpRhs = CONTAINS, String | STARTS, [ WITH ], String | ENDS, [ WITH ], String ;

SetOpRhs = HAS, ( [ Operator ], Value | ALL, ValueList | EXACTLY, ValueList | ANY, ValueList | ONLY, ValueList ) ;
(* Note: support for ONLY in SetOpRhs is OPTIONAL *)
(* Note: support for [ Operator ] in SetOpRhs is OPTIONAL *)

SetZipOpRhs = IdentifierZipAddon, HAS, ( ValueZip | ONLY, ValueZipList | ALL, ValueZipList | EXACTLY, ValueZipList | ANY, ValueZipList ) ;

LengthComparison = LENGTH, Identifier, Operator, Value ;

IdentifierZipAddon = Colon, Identifier, {Colon, Identifier} ;

(* TOKENS *)

(* Separators: *)

OpeningBrace = '(', [Spaces] ;
ClosingBrace = ')', [Spaces] ;

Comma = ',', [Spaces] ;
Colon = ':', [Spaces] ;

(* Boolean relations: *)

AND = 'A', 'N', 'D', [Spaces] ;
NOT = 'N', 'O', 'T', [Spaces] ;
OR = 'O', 'R', [Spaces] ;

IS = 'I', 'S', [Spaces] ;
KNOWN = 'K', 'N', 'O', 'W', 'N', [Spaces] ;
UNKNOWN = 'U', 'N', 'K', 'N', 'O', 'W', 'N', [Spaces] ;

CONTAINS = 'C', 'O', 'N', 'T', 'A', 'I', 'N', 'S', [Spaces] ;
STARTS = 'S', 'T', 'A', 'R', 'T', 'S', [Spaces] ;
ENDS = 'E', 'N', 'D', 'S', [Spaces] ;
WITH = 'W', 'I', 'T', 'H', [Spaces] ;

LENGTH = 'L', 'E', 'N', 'G', 'T', 'H', [Spaces] ;
HAS = 'H', 'A', 'S', [Spaces] ;
ALL = 'A', 'L', 'L', [Spaces] ;
ONLY = 'O', 'N', 'L', 'Y', [Spaces] ;
EXACTLY = 'E', 'X', 'A', 'C', 'T', 'L', 'Y', [Spaces] ;
ANY = 'A', 'N', 'Y', [Spaces] ;

(* OperatorComparison operator tokens: *)

Operator = ( '<', [ '=' ] | '>', [ '=' ] | '=' | '!', '=' ), [Spaces] ;

(* Identifier syntax *)

IdentifierComponent = LowercaseLetter, { LowercaseLetter | Digit } ;

Identifier = IdentifierComponent, { '.', IdentifierComponent }, [Spaces] ;

Letter = UppercaseLetter | LowercaseLetter ;

UppercaseLetter =
    'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' |
    'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' |
    'Y' | 'Z'
;

LowercaseLetter =
    'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 
    'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' |
    'y' | 'z' | '_'
;

(* Strings: *)

String = '"', { EscapedChar }, '"', [Spaces] ;

EscapedChar = UnescapedChar | '\', '"' | '\', '\' ;

UnescapedChar = Letter | Digit | Space | Punctuator | UnicodeHighChar ;

Punctuator =
    '!' | '#' | '$' | '%' | '&' | "'" | '(' | ')' | '*' | '+' | ',' |
    '-' | '.' | '/' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | '[' |
    ']' | '^' | '`' | '{' | '|' | '}' | '~'
;

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

(* The 'UnicodeHighChar' specifies all Unicode characters above 0x7F;
   the syntax used is the onw compatible with Grammatica: *)

UnicodeHighChar = ? [^\x00-\x7F] ? ;
 
(* END EBNF GRAMMAR Number *)
(* END EBNF GRAMMAR Filter *)
```

Note: when implementing a parser according this grammar, the
implementers MAY choose to construct a lexer that ignores all
whitespace (space, tabs, newlines, vertical tabulation and form feed
characters, as described in the grammar 'Space' definition), and use
such a lexer to recognize language elements that are described in the
`(* TOKENS *)` section of the grammar. In that case, the '[Spaces]'
element should probably be removed from the `Filter = [Spaces],
Expression` definition as well, and the remaining grammar rules could
then be used as a parser generator (like yacc, bison, antlr) input.

## <a name="h.app3">Appendix 3. Regular Expressions for OPTiMaDe Filter Tokens.</a>
The string below contains Perl-Compatible Regular Expressions to recognise
identifiers, number, and string values as specified in this specification.

```
#BEGIN PCRE identifiers
[a-z_][a-z_0-9]*(\.[a-z_][a-z_0-9]*)*
#END PCRE identifiers

#BEGIN PCRE numbers
[-+]?(?:\d+(\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?
#END PCRE numbers

#BEGIN PCRE strings
"([^\\"]|\\.)*"
#END PCRE strings
```

The strings below contain Extended Regular Expressions (EREs) to recognize identifiers, number, and string values
as specified in this specification.

```
#BEGIN ERE identifiers
[a-z_][a-z_0-9]*(\.[a-z_][a-z_0-9]*)*
#END ERE identifiers

#BEGIN ERE numbers
[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?
#END ERE numbers

#BEGIN ERE strings
"([^\"]|\\.)*"
#END ERE strings
```
