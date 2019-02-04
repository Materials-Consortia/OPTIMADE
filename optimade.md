# OPTIMADE API specification v0.9.7-develop

[1. Introduction](#h.1)

[2. Term definition](#h.2)

[3. General API requirements and conventions](#h.3)  
&nbsp;&nbsp;&nbsp;&nbsp;[3.1. Base URL](#h.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;[3.2. URL encoding](#h.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[3.3. Responses](#h.3.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.1. Response format](#h.3.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.2. JSON API response schema: common fields](#h.3.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3.3. HTTP response status codes](#h.3.3.3)  

[4. API endpoints](#h.4)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.1. Entry listing endpoints](#h.4.1.)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.1.1. URL Query Parameters](#h.4.1.1.)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.1.2. Response schema](#h.4.1.2.)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.2. Single entry endpoints](#h.4.2.)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.1. URL Query Parameters](#h.4.2.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.2. JSON API response schema](#h.4.2.3)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.3. General entry listing 'All' endpoint](#h.4.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.1. URL Query Parameters](#h.4.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2. Response schema](#h.4.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.4. Info endpoints](#h.4.4)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.4.1. Base URL info endpoint](#h.4.4.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.4.2. Entry listing info endpoints](#h.4.4.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[4.5. Custom extension endpoints](#h.4.5)  
[5. API Filtering Format Specification](#h.5)  
&nbsp;&nbsp;&nbsp;&nbsp;[5.1. Lexical tokens](#h.5.1)  
&nbsp;&nbsp;&nbsp;&nbsp;[5.2. The filter language syntax](#h.5.2)  

[6. Entry list](#h.6)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.1. Properties Used by Multiple Entry Types](#h.6.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.1.1. id](#h.6.1.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6.1.2. modification\_date](#h.6.1.2)  
&nbsp;&nbsp;&nbsp;&nbsp;[6.2. 'Structure' Entries](#h.6.2)  
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

&nbsp;&nbsp;&nbsp;&nbsp;[6.3. 'Calculation' entries](#h.6.3)  

[Appendix 1: Database provider-specific namespace prefixes](#h.app1)  
[Appendix 2: The Filter language EBNF grammar](#h.app2)  
[Appendix 3: The regular expressions to check OPTiMaDe number syntax](#h.app3)

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
[JSON API](http://jsonapi.org) specification (with the exception that
non-conformant responses can be generated if an API user specifically
requests a non-standard response format.) In cases where specific
restrictions are given in the JSON API specification (e.g., on format
of Member Names, on return codes) that are stricter than what is
formulated in this document, they are expected to be upheld by API
implementations unless otherwise noted in this document.

The full present version number of the specification is shown as part of the
top headline of this document.

# <a name="h.2">2. Term definition</a>

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).

* Database provider: A service that provides one or more databases of materials information.
* Database provider-specific prefix: This specification defines a set of
  database provider-specific prefixes in [Appendix 1](#h.app1).
* Entry: a type of resource over which a query can be formulated using the API
  (structure, calculations).
* Property: anything that can be in the filtering of results.
* Field: an entity that can be requested as partial output from the API.
* ID: a unique identifier that specifies a specific resource in a database,
  that does not necessarily need to be immutable. It MUST NOT be a reserved
  word.
* Immutable ID: a unique identifier that specifies a specific resource in a
  database that MUST be immutable.
* Reserved words: the list of reserved words in this standard is: info.
* Property Types :
    * **string**, **integer**, **float**, **boolean**, **null value**: base data
      types as defined in more detail in [section '5.1. Lexical
      tokens'](#h.5.1).
    * **list**, **dictionary**: with the meaning they have in the JSON
      data-interchange format, i.e., respectively, an ordered list of elements
      (where each element can have a different type), or a hash table
      (with the limitation that the hash key MUST be a string).

# <a name="h.3">3. General API requirements and conventions</a>

## <a name="h.3.1">3.1. Base URL</a>

Each database provider will publish a base URL that serves the API. An
example could be: http://example.com/optimade/. Every URL component
that follows the base URL MUST behave as standardized in this API
specification.

The client MAY include a version number in the base URL prefixed with
the letter 'v', where the version number indicates the version of the
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
the 'available_api_versions' field of the 'attributes' field from a
query to the base URL info endpoint (see
[section '4.4.1. Base URL info endpoint'](#h.4.4.1)). The database
provider SHOULD strive to implement the latest subversion of any major
and minor version supported. Specifically, the latest version of this
standard SHOULD be supported.

Examples of valid base URLs:

* http://example.com/optimade/
* http://example.com/optimade/v0.9/
* http://example.com/
* http://example.com/some/path/

Examples of invalid base URLs:

* http://example.com/optimade/v0/
* http://example.com/optimade/0.9/

## <a name="h.3.2">3.2. URL encoding</a>

Clients SHOULD encode URLs according to
[RFC 3986](http://tools.ietf.org/html/rfc3986). API implementations
MUST decode URLs according to
[RFC 3986](http://tools.ietf.org/html/rfc3986).

## <a name="h.3.3">3.3. Responses</a>

### <a name="h.3.3.1">3.3.1. Response format</a>

API responses MUST be returned in the format specified in the
request. If no specific response format is specified in the request by
use of the **response_format** URL query parameter (see below), the default
response format is JSON API, which is compliant to the
response format described by the [JSON API](http://jsonapi.org)
specification. All endpoints MUST support at least the JSON API
format. Each endpoint MAY OPTIONALLY support multiple formats, and
declare these formats in their 'info' endpoints.

An API implementation MAY return other formats than as specified here.
These can be implemented and documented however the implementor chooses.
However, they MUST be prefixed by a database provider-specific prefix as defined in
[Appendix 1](#h.app1).

Specifying a **response_format** URL query parameter that selects a
response format different from JSON API allows the API specification
to break conformance with the [JSON API](http://jsonapi.org)
specification. Not only in response format, but also in, e.g.,
how content negotiation is implemented.

### <a name="h.3.3.2">3.3.2. JSON API response schema: common fields</a>

Every response MUST contain the following fields:

* **links**: a [JSON API links object](http://jsonapi.org/format/#document-links).
  Where,
    * **next**: is an URI that represents a suggested way to fetch the
      next set of results if not all were returned, either directly as string, or as link object which can contain the following members:
        * `href`: a string containing the link’s URL.
        * `meta`: a meta object containing non-standard meta-information about the link.

        The **next** field MUST be null or omitted if there is no additional data, or if there is no way to fetch additional data.
      
    The links object can OPTIONALLY contain the field

    * **base\_url**: the URL of the api endpoint 

        ```
        "resource": {
          "base_url": "http://example.com/optimade/v0.9/",
          "_example.com_db_version": "3.2.1"
        }, 
        ``` 
* **meta**:
    * **query**: information on the query that was requested.
        * It MUST be a dictionary with these items:
            * **representation**: a string with the part of the URL that follows the base
            URL.
    * **api\_version**: a string containing the version of the API .
    * **time\_stamp**: a string containing the date and time at which the query
      was executed, in [ISO 8601](https://www.iso.org/standard/40874.html)
      format.  Times MUST be timezone-aware (i.e. MUST NOT be local times),
      in one of the formats allowed by [ISO 8601](https://www.iso.org/standard/40874.html)
      (i.e. either be in UTC, and then end with a Z, or indicate explicitly
      the offset).
    * **data\_returned**: an integer containing the number of data returned for the query.
    * **more\_data\_available**: 'False' if all data for this query has been
      returned, and 'True' if not.
    * The dictionary MAY also include these OPTIONAL items:
        * **data\_available**: an integer containing the total number of data
          available in the database. 
        * **last\_id**: a string containing the last ID returned.        
        * **response\_message**: OPTIONAL response string from the server.
        * Other OPTIONAL additional information _global to the query_ that is not specified
          in this document, MUST start with a database provider-specific prefix as defined in [Appendix 1](#h.app1).
    * Example:  
        For a request made to http://example.com/optimade/v0.9/structures/?filter=a=1 AND b=2

        ```
        {
          "meta": {
            "query": {
              "representation": "/structures/?filter=a=1 AND b=2",
            },
            "api_version": "v0.9",
            "time_stamp": "2007-04-05T14:30Z",
            "data_returned": 10,
            "data_available": 10,
            "more_data_available": false
          }
          ...
          <additional response items>
        }
        ```
* **data**: The schema of this value varies by endpoint, it can be either a [JSON API Resource Object](http://jsonapi.org/format/#document-resource-objects) or a list or JSON API Resource Objects.
  Every resource object need the `type` and `id` fields, and its attributes (described in [section '4. API endpoints'](#h.4) of this document) need to be in a dictionary corresponding to the **attributes** field.

The response MAY also return resources related to the primary data in the OPTIONAL field:

* **include**: a list of [JSON API Resource Objects](http://jsonapi.org/format/#document-resource-objects) related to the primary data contained in `data` that are included in this document.

If there were errors in producing the response all other fields can be skipped, and the following field MUST be present

* **errors**: a list of [JSON API Error Objects](http://jsonapi.org/format/#error-objects)

An example of a full response:

```
{
  "links": {
    "next": null,
    "base_url": {
      "href": "http://example.com/optimade/v0.9/",
      "meta": {
         "_example.com_db_version": "3.2.1"
      }
    }
  },
  "resource": {
  },  
  "data": [...],
  "meta": {  
    "query": {
      "representation": "/structures?a=1&b=2"
    }
    "api_version": "v0.9",  
    "time_stamp": "2007-04-05T14:30Z",  
    "data_returned": 10,
    "data_available": 10,
    "last_id": "xy10",
    "more_data_available": false
  },
  "response_message": "OK",
  <OPTIONAL DB-specific meta_data, global to the query>
}
```


### 3.3.4. HTTP response status codes

| Code | Message                                                               |
|:----:|:--------------------------------------------------------------------- |
| 200  | OK (Successful operation)                                             |
| 400  | Bad request (e.g., mistyped URL)                                      |
| 401  | User does not have permission                                         |
| 403  | Forbidden (the request was understood but not authorized)             |
| 404  | Not found (e.g., database not found)                                  |
| 408  | Request timeout because it is taking too long to process the query    |
| 410  | The database has been moved                                           |
| 413  | The response is too large                                             |
| 414  | The request URI contains more than 2048 characters                    |
| 418  | Asked for a non-existent keyword                                      |
| 422  | Database returned (200) but the translator failed                     |

# <a name="h.4">4. API endpoints</a>

The URL component that follows the base URL MUST represent one of the
following endpoints:

* an 'entry listing' endpoint
* a 'single entry' endpoint
* a general filtering 'all' endpoint that can search all entry types
* an introspection 'info' endpoint
* a custom 'extensions' endpoint prefix  

These endpoints are documented below.

## <a name="h.4.1">4.1. Entry listing endpoints</a>

Entry listing endpoints return a list of documents representing entries of a
specific type. For example, a list of structures, or a list of calculations.

Examples:

* http://example.com/optimade/v0.9/structures
* http://example.com/optimade/v0.9/calculations

There MAY be multiple entry listing endpoints, depending on how many types of
entries a database provides. Specific standard entry types are specified in a
later section of this specification. The API implementation MAY provide other
entry types than the ones standardized in this specification, but such entry
types MUST be prefixed by a database-specific prefix.

### <a name="h.4.1.1">4.1.1. URL Query Parameters</a>

The client MAY provide a set of URL query parameters in order to alter
the response and provide usage information. While these URL query
parameters are OPTIONAL for clients, API implementers MUST accept and
handle them. To adhere to the requirement on implementation-specific
URL query parameters of [JSON API](http://jsonapi.org), query
parameters that are not standardized by that specification have been
given names that consist of at least two words separated by an
underscore (a LOW LINE character '_').

Standard OPTIONAL URL query parameters standardized by the JSON API specification:

* **filter**: a filter string, in the format described below in [section '5. API Filtering
  Format Specification'](#h.5).

Standard OPTIONAL URL query parameters not in the JSON API specification:

* **response_format**: specifies which output format is requested. Specifically, the
  format string 'jsonapi' specifies the standard output format documented
  in this specification as the JSON API response format.  
  Example: http://example.com/optimade/v0.9/structures/?response_format=xml
* **email_address**: specifies an email address of the user making the request. The
  email SHOULD be that of a person and not an automatic system.  
  Example: http://example.com/optimade/v0.9/structures/?email_address=user@example.com
* **response_limit**: sets a numerical limit on the number of entries returned. The API
  implementation MUST return no more than the number specified. It MAY return
  less. The database MAY have a maximum limit and not accept larger numbers (in
  which case an error code MUST be returned). The default limit value is up
  to the API implementation to decide.  
  Example: http://example.com/optimade/v0.9/structures/?response_limit=100
* **response_fields**: specify a comma-delimited set of fields to be provided in the
  output. If provided, only these fields MUST be returned and no others.  
  Example: http://example.com/optimade/v0.9/structures/?response_fields=id,url

Additional OPTIONAL URL query parameters not described above are not
considered to be part of this standard, and are instead considered to
be 'custom URL query parameters'. These custom URL query parameters
MUST be of the format "&lt;database-specific
prefix&gt;&lt;url\_query\_parameter\_name&gt;".  These names adhere to
the requirements on implementation-specific query parameters of
[JSON API](http://jsonapi.org) since the database-specific prefixes
contain an underscore (a LOW LINE character '_').

Example uses of custom URL query parameters include providing an access token for the
request or to tell the database to increase verbosity in error output, or
providing a database specific extended searching format.

Examples:

* http://example.com/optimade/v0.9/structures/?\_exmpl\_key=A3242DSFJFEJE
* http://example.com/optimade/v0.9/structures/?\_exmpl\_warning\_verbosity=10
* http://example.com/optimade/v0.9/structures/?\_exmpl\_filter="elements all in [Al, Si, Ga]"

Note: the specification presently makes no attempt to standardize access
control mechanisms. There are security concerns with access control based on
URL tokens, and the above example is not to be taken as a recommendation for
such a mechanism.

### <a name="h.4.1.2">4.1.2 JSON API response schema</a>

'Entry Listing' endpoint response dictionaries MUST have a "data"
key. The value of this key MUST be a list containing dictionaries that
represent individual entries. In the JSON API format every dictionary
([Resource Object](http://jsonapi.org/format/#document-resource-objects))
needs the following fields

* **type**: field containing the type of the entry
* **id**: a string which together with the type uniquely identifies the object, this can be the local database ID
* **attributes**: a dictionary, containing key-value pairs representing the
  entries properties, and the following fields:
    * **local\_id**: the entry's local database ID
    * **last\_modified**: an [ISO 8601](https://www.iso.org/standard/40874.html)
      representing the entry's last modification time
    * **immutable\_id**: an OPTIONAL field containing the entry's immutable ID

  Database-specific properties need to include the database-specific prefix.

OPTIONALLY it can also contains the following fields:

* **links**: a [JSON API links object](http://jsonapi.org/format/#document-links) can OPTIONALLY contain the field
    * **self**: the entry's URL
* **meta**: a meta object that contains non-standard meta-information about the object
* **relationships**: a dictionary containing references to other Resource Objects as defined in [JSON API Relationships Object](http://jsonapi.org/format/#document-resource-object-relationships)

Example:

```
{
  ... <other response items> ...
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
    ...
    {
      "type": "structure",
      "attributes": {
        "formula": "Es2"
        "local_id": "example.db:structs:1234",
        "url": "http://example.db/structs/1234",
        "immutable_id": "http://example.db/structs/1234@123",
        "last_modified": "2007-04-07T12:02Z"
      },
    },
  ]
}
```

## <a name="h.4.2">4.2. Single entry endpoints</a>

A client can request a specific entry by appending an ID component to the URL
of an entry listing endpoint. This will return properties for the entry with
that ID.

If using the JSON API format, the ID component MUST be the content of the id field.

Note that entries cannot have an ID of 'info', as this would collide with the
'Info' endpoint (described in [section '4.4. Info endpoints'](#h.4.4)) for a given entry type.

Examples:

* http://example.com/optimade/v0.9/structures/exmpl:struct/3232823
* http://example.com/optimade/v0.9/calculations/exmpl:calc/232132

### <a name="h.4.2.1">4.2.1. URL Query Parameters</a>

The client MAY provide a set of additional URL query parameters also for this endpoint
type. URL query parameters not recognized MUST be ignored. While the following URL query parameters
are OPTIONAL for clients, API endpoints MUST accept and handle them:
**response_format**, **email_address**, **response_fields**. The meaning of these URL query parameters are as
defined above in [section '4.1.1. URL Query Parameters'](#h.4.1.1).

### <a name="h.4.2.2">4.2.2. Response schema</a>

The response for a 'single entry' endpoint is the same as for 'entry listing'
endpoint responses, except that the value of the "data" key MUST have only one
entry.

## <a name="h.4.3">4.3. General entry listing 'All' endpoint</a>

The 'general entry listing endpoint' returns a list of entries representing all
entries a database provides, regardless of type. This endpoint MUST be provided
at the path "&lt;base\_url&gt;/all" . The purpose of this endpoint is to allow more
general searches across entry types. The general entry listing endpoint MUST
accept both GET and a POST-type requests, with provided POST-type URL query parameters
overriding duplicate URL query parameters provided as GET URL query parameters.

### <a name="h.4.3.1">4.3.1. URL Query Parameters</a>

The following URL query parameters MUST be recognized and handled: **filter**, **response_fields**,
**response_format**, **response_limit**, **email_address**. The meaning of these URL query parameters are as defined
above in [section '4.1.1. URL Query Parameters'](#h.4.1.1). Furthermore,
custom OPTIONAL URL query parameters, also described above, are also allowed.

Example: http://example.com/optimade/v0.9/all/?response\_fields=id,url&response\_format=jsonapi

### <a name="h.4.3.2">4.3.2. Response schema</a>

The response for a general entry 'all' endpoint is the same as for 'entry
listing' endpoint responses.

## <a name="h.4.4">4.4. Info endpoints</a>

Info endpoints provide introspective information, either about the API itself,
or about specific entry types.

Info endpoints are constructed by appending "**info**" to any of:

1. the base URL (e.g., http://example.com/optimade/v0.9/info/)
2. type-specific entry listing endpoints (e.g., 
http://example.com/optimade/v0.9/structures/info/)
3. the general entry listing endpoint (e.g., http://example.com/optimade/v0.9/all/info/)

These types and output content of these info endpoints are described in more
detail in the subsections below.

### <a name="h.4.4.1">4.4.1. Base URL info endpoint</a>

The Info endpoint on the base URL or directly after the version number (e.g.,
http://example.com/optimade/v0.9/info) returns information relating to the API
implementation.

The response dictionary MUST include the following fields

* **type**: MUST be "info"
* **id**: "/"
* **attributes**: a dictionary containing the following fields:
    * **api\_version**: Presently used version of the API.
    * **available\_api\_versions**: a dictionary where values are the base URLs for the versions of the API that are supported, 
	    and the keys are strings giving the full version number provided by that base URL. Provided base urls MUST
		adhere to the rules in [section '3.1. Base URL'](#h.3.1).
    * **formats**: a list of available output formats.
    * **entry\_types\_by\_format**: Available entry endpoints as a function of output formats.

Example:

```
{
  ... <other response items> ...
  "data": [
    {
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
            "structure",
            "calculation"
          ],
          "xml": [
            "structure"
          ]
        },
        "available_endpoints": [
          "entry",
          "all",
          "info"
        ]
      }
    }
  ]
}
```

### <a name="h.4.4.2">4.4.2. Entry listing info endpoints</a>

Entry listing info endpoints are of the form
"&lt;base\_url&gt;/&lt;entry\_type&gt;/info/" (e.g., 
http://example.com/optimade/v0.9/structures/info/). The response for these endpoints
MUST include the following information in the "data" field:

* **description**: Description of the entry.
* **properties**: A dictionary describing queryable properties for this entry
  type, where each key is a property ID.
  Each value is a dictionary, with the required key 'description' and optional
key 'unit'.
* **formats**: Output formats available for this type of entry.
* **output\_fields\_by\_format**: Available output fields for this entry type as
  function of output format.

Example:

```
{
  ... <other response items> ...
  "data": [
    {
      "description": "a structure",
      "properties": {
        "nelements": {
          "description": "number of elements",
          "unit": "MPa"
        },
        ... <other property descriptions>
      },
      "formats": ["json", "xml"],
      "output_fields_by_format": {
        "json": ["nelements", ... ],
        "xml": ["nelements"]
      }
    }
  ]
}
```

## <a name="h.4.5">4.5. Custom extension endpoints</a>

API implementors can provide custom endpoints, in this form
"&lt;base\_url&gt;/extensions/&lt;custom paths&gt;".

# <a name="h.5">5. API Filtering Format Specification</a>

A filter language will be used in the 'filter=' component of the query string.
The 'filter=' component can be used to select a subset of records to
be returned for a specific query. The value of the 'filter=' component MUST
follow the filter language syntax described below.

The filter language MUST support at least the following features:

* flat filters with one level of "AND" and "OR" conjunctions.

## <a name="h.5.1">5.1. Lexical tokens</a>

The following tokens are used in the filter query component:

* **Property names** (see [section '6. Entry list'](#h.6)): are to follow the identifier
  syntax of programming languages -- the first character MUST be a letter, the
  subsequent symbols MUST be alphanumeric; the underscore ("\_", ASCII 95 dec
  (0x5F)) is considered to be a letter. Identifiers are case-sensitive. The
  length of the identifiers is not limited, except that the whole query SHOULD
  NOT be longer than the limits imposed by the URI specification.

    Examples of valid property names:

    * band\_gap
    * cell\_length\_a
    * cell\_volume

    Examples of incorrect property names:

    * 0\_kvak (starts with a number);
    * "foo bar" (contains space; contains quotes)
    
    Identifiers that start with an underscore are specific to a database and its
    provider, and MUST be on the format of a database provider-specific prefix as
    defined in [Appendix 1](#h.app1).

    Examples:

    * \_exmpl\_formula\_sum (a property specific to that database)
    * \_exmpl\_band\_gap
    * \_exmpl\_supercell
    * \_exmpl\_trajectory
    * \_exmpl\_workflow\_id  
    &nbsp;

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
  notation, using the usual programming language conventions. A regular
  expression giving the number syntax is given below as a [POSIX Extended
  Regular Expression (ERE)](https://en.wikipedia.org/w/index.php?title=Regular_expression&oldid=786659796#Standards)
  or as a [Perl-Compatible Regular Expression (PCRE)](http://www.pcre.org):
    * ERE: [-+]?([0-9]+(\\.[0-9]\*)?|\\.[0-9]+)([eE][-+]?[0-9]+)?
    * PCRE: [-+]?(?:\\d+(\\.\\d*)?|\\.\\d+)(?:[eE][-+]?\\d+)?
* An implementation of the search filter MAY reject numbers that are outside
  the machine representation of the underlying hardware; in such case it MUST
  return an appropriate error message, indicating the cause of the error and an
  acceptable number range.
* Examples of valid numbers:
    * 12345, +12, -34, 1.2, .2E7, -.2E+7, +10.01E-10, 6.03e23, .1E1, -.1e1,
      1.e-12, -.1e-12, 1000000000.E1000000000
* **A comma-separated list of** _incorrect_ number examples (although they MAY
  contain correct numbers as substrings):
    * 1.234D12, .e1 , -.E1 , +.E2, 1.23E+++, +-123


More examples of the number tokens and machine-readable definitions and tests
can be found in the [Materials-Consortia API Git repository](https://github.com/Materials-Consortia/API/)
(files
[integers.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/integers.lst),
[not-numbers.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/not-numbers.lst),
[numbers.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/numbers.lst),
and
[reals.lst](https://github.com/Materials-Consortia/API/blob/master/tests/inputs/reals.lst)).


* **Operator tokens** are represented by usual mathematical relation symbols or by
  case-sensitive keywords. Currently the following operators are supported: =,
  !=, <=, >=, <, > for tests of number or string (lexicographical) equality,
  inequality, less-than, more-than, less, and more relations; AND, OR, NOT for
  logical conjunctions. The mathematical relations have higher priority than
  logical relations; relation NOT has higher priority than AND; relation AND has
  higher priority than OR. Thus, the expression 'a >= 0 AND NOT b < c OR c = 0'
  is interpreted as '((a >= 0) AND (NOT (b &lt; c))) OR (c = 0)' if the
  expression was fully braced.


* The current API supports only one level of braces (no nested braces) : the
  expression 'a > b AND (a > 0 OR b > 0)' MUST be supported to allow changing
  of the priority of the logical operations.

## <a name="h.5.2">5.2. The filter language syntax</a>

Filtering expressions MUST follow the following [EBNF](http://standards.iso.org/ittf/PubliclyAvailableStandards/s026153_ISO_IEC_14977_1996(E).zip) grammar (fig 1.). Briefly,
the filtering expression consists of the prefixing keyword 'filter=' that
distinguishes it from other query string components that is followed by a
Boolean expression on the search criteria. In the expression, desired
properties are compared against search values; several such comparisons can be
combined using AND, OR and NOT logical conjunctions with their usual
semantics. Examples of the comparisons and logical expressions:

* spacegroup="P2"
* \_exmpl\_cell\_volume<100.0
* \_exmpl\_bandgap > 5.0 AND \_exmpl\_molecular\_weight < 350

The precedence (priority) of the operators MUST be as indicated in the list
below:

1.  The comparison operators ('<', '<=', '=', etc.) -- highest priority;
2.  NOT
3.  AND
4.  OR -- lowest priority.

Thus, the expression 'NOT a > b OR c = 100 AND f = "C2 H6"' is interpreted as

'(NOT (a > b)) OR ( (c = 100) AND (f = "C2 H6") )' when fully braced.

Fig. 1 The top-level rules of the Filter language grammar.

```
(* The top-level 'filter' rule: *)
Filter = Keyword, Expression;
(* Keywords *)
Keyword = "filter=" ;
(* Values *)
Value = Identifier | Number | String ;
(* The white-space: *)
Space = ' ' | '\t' ;
Spaces = Space, { Space } ;
(* Boolean relations: *)
AND = "AND" ; (* a short-hand for: AND = 'A', 'N', 'D' *)
NOT = "NOT" ;
OR = "OR" ;
(* Expressions *)
Expression = Term, [Spaces], [ OR, [Spaces], Expression ] ;
Term = Atom, [Spaces], [ AND, [Spaces], Term ] ;
Atom = [ NOT, [Spaces] ], ( Comparison |
           '(', [Spaces], AndComparison,
                [Spaces], { OR,
                [Spaces], AndComparison, [Spaces] }, ')' );
AndComparison = [ NOT, [Spaces] ], Comparison,
                [Spaces], { AND,
                [Spaces], [ NOT, [Spaces] ], Comparison, [Spaces] } ;
(* Comparison operator tokens: *)
Operator = '<', [ '=' ] | '>', [ '=' ] | '=' | '!', '=' ;
Comparison = Value, [Spaces], Operator, [Spaces], Value ;
```

The structure of tokens 'Identifier', 'Number', 'String' and 'Operator' are
described above in [section '5.1. Lexical tokens'](#h.5.1) and omitted here for brevity;
a full length machine readable version of the grammar, including the definition
of the lexical tokens, is available in the [Materials-Consortia API Git repository](https://github.com/Materials-Consortia/API)
(file 
[grammars/flat-filters.ebnf](https://github.com/Materials-Consortia/API/blob/master/grammars/flat-filters.ebnf)).

Since the usual arithmetic expression syntax used for specifying filter
expressions can contain characters that are not URL transparent, they MUST be
URL-encoded before their use in a GET query. The specified order of escaping
and encoding of the Filter language statements is the following:

1. special characters in string values MUST be escaped first as described
   above in the section "String values";
2. the resulting expression MUST be URL-encoded.

The extraction flow is obviously the opposite -- first the Filter string MUST
be first URL-decoded, and after that string tokens MUST be unescaped to get
values for comparisons.

When comparisons are performed, comparison operators '<', '<=', '=', '!=' and
so on are interpreted either as numeric value comparisons or as string
comparisons, depending on the type of the search parameter. The literal string
value MUST be converted to the type of the search parameter (e.g., 'x > "0.0"'
where x is a coordinate MUST treat this expression as numeric filter 'x > 0',
and 's = 0' search against text parameter 's' MUST perform string comparison as
in 's = "0"'). Strings are converted to numbers using the token syntax specified
in [section '5.1. Lexical tokens'](#h.5.1), p. "Numeric values"; numbers SHOULD be converted to strings using
the libc '%g' format. In all cases the application MUST return a warning when
conversion was performed and specify the actual search values that were used.

For comparisons of two parameters (e.g. 'x > y') or two constants (1 = 1) both
compared values MUST be of the same type (i.e. both MUST be either numeric or
string values); implementation MUST return error code if this is not the case.

Examples of syntactically correct filter strings:

* filter=\_exmpl\_melting\_point<300 AND nelements=4 AND elements="Si,O2"

Examples of syntactically correct query strings embedded in queries:

* http://example.org/optimade/v0.9/structures?filter=\_exmpl\_melting\_point%3C300+AND+ nelements=4+AND+elements="Si,O2"&response_format=xml

Or, fully URL encoded :

* http://example.org/optimade/v0.9/structures?filter=\_exmpl\_melting\_point%3C300+AND+nelements%3D4+AND+elements%3D%22Si%2CO2%22&response_format=xml

# <a name="h.6">6. Entry list</a>

This section defines standard entry types and their properties.

## <a name="h.6.1">6.1. Properties Used by Multiple Entry Types</a>

### <a name="h.6.1.1">6.1.1. id</a>

* Description: An entry's ID.
* Requirements/Conventions:
    * IDs MUST be URL-safe; in particular, they MUST NOT contain commas.
    * Reasonably short IDs are encouraged and SHOULD NOT be longer than 255 characters.
* Examples:
    * db/1234567
    * cod/2000000
    * cod/2000000@1234567
    * nomad/L1234567890

### <a name="h.6.1.2">6.1.2. modification\_date</a>

* Description: A date representing when the entry was last modified.
* Requirements/Conventions: [ISO 8601](https://www.iso.org/standard/40874.html) format
* Example:
    * 2007-04-05T14:30Z
* Querying: Date-time queries are permitted ([RFC 3339](http://tools.ietf.org/html/rfc3339)).

### <a name="h.6.1.3">6.1.3. database provider-specific properties</a>
* Description: Database providers are allowed to insert database-specific entries in the output of both standard entry types, and database-specific entry types.
* Requirements/Conventions: these MUST be prefixed by a database provider-specific prefix as defined in [Appendix 1](#h.app1).
* Examples:
    * \_exmpl\_formula\_sum 
    * \_exmpl\_band\_gap
    * \_exmpl\_supercell
    * \_exmpl\_trajectory
    * \_exmpl\_workflow\_id  

## <a name="h.6.2">6.2. 'Structure' Entries</a>

Structure entries have the properties described above in "Properties Used by
Multiple Entry Types", as well as the following properties:

### <a name="h.6.2.1">6.2.1. elements</a>

* Description: names of elements found in the structure.
* Requirements/Conventions: chemical symbols of elements joined by commas.
* Examples:
    * "Si"
    * "Si,Al,O"
* Querying: the conjunction means "AND", i.e., all records pertaining to
  materials containing Si, Al **and** O, and possibly other elements, MUST be
  returned; use 'nelements=3' to specify **exactly** 3 elements; (element="Si,Al,O"
  means you want structures with at least the 3 elements, and it MUST contain
  Si, Al AND O).

### <a name="h.6.2.2">6.2.2. nelements</a>

* Description: The number of elements found in a structure.
* Requirements/Conventions: an integer
* Example: 1
* Querying: Use numerical operators, as defined in the filtering section above.
    * Examples:
        * return only entities that have exactly 4 elements: " nelements=4"
        * query for structures that have between 2 and 7 elements:
          "nelements>=2 AND nelements<=7"

### <a name="h.6.2.3">6.2.3. chemical\_formula</a>

* Description: The chemical formula for a structure.
* Requirements/Conventions:
    * The formula MUST be **reduced**.
    * Element names MUST be with proper capitalization (Si, not SI for "silicon").
    * The order in which elements are specified SHOULD NOT be significant (e.g.,
      "O2Si" is equivalent to "SiO2").
    * No spaces or separators are allowed.

### <a name="h.6.2.4">6.2.4. formula\_prototype</a>

* Description: The formula prototype obtained by sorting elements by the
  occurrence number in the **reduced** chemical formula and replace them with
  subsequent alphabet letters A, B, C and so on.

### <a name="h.6.2.5">6.2.5. dimension\_types</a>

* Description: a list of three integers. For each of the three 
  directions indicated by the three lattice vectors (see property `lattice_vectors`) this list indicates if that direction is periodic (value 1) or non-periodic (value 0). Note: the elements in this list each refer to the direction of the corresponding entry in `lattice_vectors` and *not* the Cartesian x, y, z directions.
* Requirements: 
  * This property is REQUIRED.
  * it MUST be a list of length 3.
  * each element MUST be an integer and MUST assume only the value 0 or 1.
* Examples:
  * For a molecule: `[0, 0, 0]`
  * For a wire along the direction specified by the third lattice vector: `[0, 0, 1]`
  * For a 2D surface/slab, periodic on the plane defined by the first and third
    lattice vector: `[1, 0, 1]`
  * For a bulk 3D system: `[1, 1, 1]`

### <a name="h.6.2.6">6.2.6. lattice\_vectors</a>

* Description: The three lattice vectors in Cartesian coordinates, in angstrom
* Requirements/convention: 
  * This property is REQUIRED, except when `dimension_types` is equal to `[0, 0, 0]` (in this case it is OPTIONAL).
  * It MUST be a list of three vectors *a*, *b* and *c*, where each of the vectors MUST BE a list of vector's coordinates along the x, y and z Cartesian coordinates. (Therefore, the first index runs over the three lattice vectors and the second index runs over the x, y, z Cartesian coordinates.)
  * For databases that do not define an absolute Cartesian
    system (but e.g. define only the length and angles between
    vectors), the first lattice vector SHOULD be
    set along `x` and the second on the `xy` plane.
  * This property MUST be an array of dimensions 3 times 3 regardless of the elements of `dimension_types`. The vectors SHOULD by convention be chosen so the determinant of the `lattice_vectors` matrix is different from zero. The vectors in the non-periodic directions have no significance beyond fulfilling these requirements.
* Examples:
  * `[[4., 0., 0.], [0., 4., 0.], [0., 1., 4.]]` represents
    a cell where the first vector is `(4, 0, 0)`,
    i.e. a vector aligned along the `x` axis of length 4 angstrom; the second
    vector is `(0,4,0)` and the third vector `(0,1,4)`.

### <a name="h.6.2.7">6.2.7. cartesian\_site\_positions</a>

* Description: Cartesian positions of each site. A site is 
  an atom, a site potentially occupied by an atom, or a placeholder 
  for a virtual mixture of atoms
  (e.g. in a virtual crystal approximation).
* Requirements: 
  * This property is REQUIRED.
  * It MUST be a list of length N times 3, where
    N is the number of sites in the structure.
  * An entry MAY have multiple sites at the same Cartesian position
    (for a relevant use of this, see, e.g., the `assemblies` property).
* Examples:
  * `[[0,0,0], [0,0,2]]` indicates a structure with two sites,
    one sitting at the origin and one along the (positive) `z` axis, 
    two angstrom away from the origin.


### <a name="h.6.2.8">6.2.8. species\_at\_sites</a>

* Description: Name of the species at each site (where values 
  for sites are specified with the same order of the 
  `cartesian_site_positions` property). The properties of 
  the species are found in the `species` property. 
* Requirements: 
  * This property is REQUIRED.
  * It MUST be a list of strings. It MUST have 
    length equal to the number of sites in the structure (first dimension of the `cartesian_site_positions` list). 
  * Each string MUST be a 
    valid key of the dictionary specified by the `species` property.
    The requirements on this string are the same as for property names, 
    i.e., it can be of any length, may use upper and lower case letters, 
    the underscore, and the digits 0-9, but cannot begin with a digit.    
* Note: 
  - each site MUST be associated only to a single species.  
    However, species can represent mixtures of atoms, and 
    multiple species MAY be defined for the same chemical element. This latter case is useful when different atoms of 
    the same type need to be grouped or distinguished, for instance in simulation codes to assign different initial 
    spin states).
* Examples:
  * `["Ti", "O2"]` indicates that the first site is 
    hosting a species labeled `Ti` and the second
    a species labeled `O2`. 

### <a name="h.6.2.9">6.2.9. species</a>

* Description: a dictionary describing the species
  of the sites of this structure. Species can be pure 
  chemical elements, or virtual-crystal atoms representing
  a statistical occupation of a given site by multiple chemical
  elements.
* Requirements/conventions: 
  * This property is REQUIRED.
  * It MUST be a dictionary, where keys represent the species name, and values are themselves dictionaries with the following keys:
    * `chemical_symbols`: REQUIRED; MUST be a list of strings   
      of all chemical elements composing this species. It MUST be 
      one of the following:
      * a valid chemical-element name, or 
      * the special value `X` to represent a non-chemical element, or
      * the special value `vacancy` to represent that this site has
        a non-zero probability of having a vacancy (the respective probability
        is indicated in the `concentration` list, see below).

    * `concentration`: REQUIRED; MUST be a list of floats, with 
      same length as `chemical_symbols`. The numbers represent 
      the relative concentration of the corresponding chemical 
      symbol in this species. The numbers SHOULD sum to one. 
      Cases in which the numbers do not sum to one typically fall only
      in the following two categories:
      - numerical errors when representing float numbers in fixed
        precision. E.g., for two chemical symbols with concentration
        `1/3` and `2/3`, the concentration might look something like
        `[0.33333333333, 0.66666666666]`. If the client is aware that
        the sum is not one because of numerical precision, it can 
        renormalize the values so that the sum is exactly one.
      - experimental errors in the data present in the database. In this
        case, it is the responsibility of the client to decide how 
        to process the data.

      Note that concentrations are uncorrelated between different sites (even of the same species).
    * `mass`: OPTIONAL. If present MUST be a float expressed in 
      a.m.u. 
    * `original_name`: OPTIONAL. Can be any valid unicode string, and SHOULD
      contain (if specified) the name of the species that is used internally 
      in the source database. 
      Note: here with source database we refer to the immediate source 
      being queried via the OPTIMADE API. The main use of this field is
      for source databases that use species names containing characters
      that are not allowed (see description of the the `species_at_site` list).
  * For systems that have only species formed by a single chemical symbol, and that have at most one species per chemical symbol, SHOULD use the chemical
  symbol as species name (e.g. Ti for titanium, O for oxygen, ...).
  However, note that this is OPTIONAL, and
  client implementations MUST NOT assume that the key
  corresponds to a chemical symbol, nor assume that if the
  species name is a valid chemical symbol, that it represents a 
  species with that chemical symbol. This means that a species `"C": {"chemical_symbols": ["Ti"], "concentration": [1.0]}` 
  is valid and represents a titanium species (and *not* a carbon species).
  * It is NOT RECOMMENDED that a structure includes species that do not have
    at least one corresponding site. 
* Examples:
  * `"Ti": {"chemical_symbols": ["Ti"], "concentration": [1.0]}`: any site with this species is occupied by a Ti atom.
  * `"Ti": {"chemical_symbols": ["Ti", "vacancy"], "concentration": [0.9, 0.1]}`: any site with this species is occupied by a Ti atom with 90% probability, and has a vacancy with 10% probability.
  * `"BaCa": {"chemical_symbols": ["vacancy", "Ba", "Ca"], "concentration": [0.05, 0.45, 0.5], "mass": 88.5}`: any site with this species is occupied by a Ba atom with 45% probability, a Ca atom with 50% probability, and by a vacancy with 5% probability. The mass of this site is (on average) 88.5 a.m.u.
  * `"C12": {"chemical_symbols": ["C"], "concentration": [1.0], "mass": 12.}`: any site with this species is occupied by a carbon isotope with mass 12.
  * `"C13": {"chemical_symbols": ["C"], "concentration": [1.0], "mass": 13.}`: any site with this species is occupied by a carbon isotope with mass 13.


### <a name="h.6.2.10">6.2.10. assemblies</a>

* Description: A description of groups of sites that are statistically correlated.
* Requirements: 
  * This key is OPTIONAL (it is absent if there are no partial occupancies).
  * Client implementations MUST check its presence (as its presence changes the interpretation of the structure).
  * If present, it MUST be a list of dictionaries, each of   
    which represents an assembly and MUST have the following two keys:
    - `sites_in_groups`: index of the sites (0-based) that belong to each group for each assembly. Example: `[[1], [2]]`: two groups, one with the second site, one with the third. Example: `[[1,2], [3]]`: one group with the second and third site, one with the fourth. 
    - `group_probabilities`:  statistical probability of each group. 
    It MUST have the same length of `sites_in_groups`. It SHOULD sum to one. 
    See below for examples of how to specify the probability of the 
    occurrence of a vacancy. The possible reasons for the values not to sum to
    one are the same already specified above for the `concentration` of each `species`.
  * If a site is not present in any group, it means that is
    is present with 100% probability (as if no assembly was
    specified)
  * a site MUST NOT appear in more than one group
* Examples (for each entry of the assemblies list):
  * `{"sites_in_groups": [[0], [1]], "group_probabilities: [0.3, 0.7]}`: the first site and the second site never occur at the same time in the unit cell. Statistically, 30% of the times the first site is present, 70% of the times the second site is present.
  * `{"sites_in_groups": [[1,2], [3]], "group_probabilities: [0.3, 0.7]}`: The second and third site are either present together or not present; they form the first group of atoms for this assembly. The second group is formed by the fourth site. Sites of the first group (the second and the third) are never present at the same time of the fourth site. 30% of times sites 1 and 2 are present (and site 3 is absent); 70% of times site 3 is present (and site 1 and 2 are absent).
* Notes:
  * Assemblies are essential to represent, for instance, the 
    situation where an atom can statistically occupy two 
    different positions (sites).
  * By defining groups, it is possible to represent for
    instance the case where a functional molecule (and not just one atom) 
    is either present or absent (or the case where it it is present in two conformations)
  * Considerations on virtual alloys and on vacancies: 
    in the special case of a virtual alloy, these specifications allow two 
    different, equivalent ways of specifying them. For instance, for a site 
    at the origin with 30% probability of being occupied by Si, 50% probability 
    of being occupied by Ge, and 20% of being a vacancy, the following two 
    representations are possible 
    - using a single species:
      ```
      "cartesian_site_positions": [[0,0,0]], 
      "species_at_sites": ["SiGe-vac"], 
      "species": {
        "SiGe-vac": {
          "chemical_symbols": ["Si", "Ge", "vacancy"], 
          "concentration": [0.3, 0.5, 0.2]
        }
      }
      ```
    - using multiple species and the assemblies:
      ```
      "cartesian_site_positions": [[0,0,0], [0,0,0], [0,0,0]], 
      "species_at_sites": ["Si", "Ge", "vac"], 
      "species": {
        "Si": {"chemical_symbols": ["Si"], "concentration": [1.]}, 
        "Ge": {"chemical_symbols": ["Ge"], "concentration": [1.]}, 
        "vac": {"chemical_symbols": ["vacancy"], "concentration": [1.]}
      }, 
      assemblies: [
        {
          "sites_in_groups": [[0], [1], [2]], 
          "group_probabilities:: [0.3, 0.5, 0.2]
        }
      ]
      ```
  * It is up to the API provider to decide which representation 
    to use, typically depending on the internal format in which 
    the structure is stored. However, given a structure identified by a unique ID, 
    the API MUST always provide the same representation for it.
  * The probabilities of occurrence of different assemblies are 
    uncorrelated. So, for instance in the following case with two assemblies:
    ` assemblies: [{"sites_in_groups": [[0], [1]], "group_probabilities: [0.2, 0.8]}, {"sites_in_groups": [[2], [3]], "group_probabilities: [0.3, 0.7]}]`
    site 0 is present with probability 0.2 annd site 1 with probability 0.8 and these two sites are correlated (either site 0 or 1 is present). Similarly, site 2 is present with probability 0.3 and site 3 with probability 0.7 and these two sites are correlated (either site 2 or 3 is present).
    However, the presence or absence of sites 0 and 1 is not
    correlated with the presence or absence of sites 2 and 3 (in the specific example, the pair of sites (0, 2) can occur with 0.2\*0.3=6% probability; the pair (0, 3) with 0.2\*0.7=14% probability; the pair (1,2) with 0.8\*0.3=24% probability; and the pair (1, 3) with 0.8\*0.7=56% probability).

## <a name="h.6.3">6.3. 'Calculation' entries</a>

Calculation entries have the properties described above in [section '6.1: Properties Used by Multiple Entry Types'](#h.6.1).

## <a name="h.app1">Appendix 1: Database provider-specific namespace prefixes</a>

This standard refers to database provider-specific prefixes. These are assigned and
included in this standard. The presently assigned prefixes are:

```YAML
# BEGIN OPTIMADE PROVIDER LIST
---
exmpl:
  - description: used for examples, not to be assigned to a real database
  - url: null
aflow:
  - description: aflow.org
  - url: null
cam:
  - description: Cambridge databases
  - url: null
cod:
  - description: Crystallography open database
  - url: http://crystallography.net/cod/optimade/
mcloud:
  - description: materialscloud.org
  - url: null
mp:
  - description: materialsproject.org
  - url: null
nmd:
  - description: nomad laboratory
  - url: null
omdb:
  - description: open materials database
  - url: null
oqmd:
  - description: open quantum materials database
  - url: null
pcod:
  - description: predicted crystallography open database
  - url: null
tcod:
  - description: theoretical crystallography open database
  - url: http://crystallography.net/tcod/optimade/
...
# END OPTIMADE PROVIDER LIST
```

The key of the YAML mappings above represents reserved names for database providers.
Each key MUST be used by the respective database provider when adding database specific
entries to their databases.
As an example, for the `exmpl` the custom string `_exmpl_` MUST be prefixed
as discussed in [section '6.1.3: database provider-specific properties'](#h.6.1.3)

The above YAML mapping serves as a machine-readable list of OPTiMaDe providers and their
default database.

API implementations SHOULD NOT make up and use new prefixes not included in
this standard, but SHOULD rather work to get such prefixes included in a future
revision of this API specification.

The initial underscore indicates an identifier that is under a separate
namespace that is under the ownership of that organisation. Identifiers
prefixed with underscores will not be used for standardized names.

## <a name="h.app2">Appendix 2. The Filter language EBNF grammar.</a>

```
(* BEGIN EBNF GRAMMAR Filter *)
(* The top-level 'filter' rule: *)

Filter = 
    Keyword, Expression;

(* Keywords *)

Keyword = "filter=" ;

(* Values *)

Value = Identifier | Number | String ;

(* The white-space: *)

Space = ' ' | '\t' ;

Spaces = Space, { Space } ;

(* Boolean relations: *)

AND = "AND" ; (* a hort-hand for: AND = 'A', 'N', 'D' *)
NOT = "NOT" ;
OR = "OR" ;

(* Expressions *)

Expression = AndExpression, [Spaces], [ OR, [Spaces], Expression ] ;

AndExpression = Term, [Spaces], [ AND, [Spaces], AndExpression ];

Term = Comparison |
       '(', [Spaces], Expression, [Spaces], ')'  |
       NOT, [Spaces], Term
       ;

(* OperatorComparison operator tokens: *)

Operator = '<', [ '=' ] | '>', [ '=' ] | '=' | '!', '=' ;

Comparison = Value, [Spaces], Operator, [Spaces], Value;

(* Identifier syntax *)

Identifier = Letter, { Letter | Digit } ;

Letter =
    'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' |
    'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' |
    'Y' | 'Z' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' |
    'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' |
    'w' | 'x' | 'y' | 'z' | '_'
;

(* Strings: *)

String = '"', { EscapedChar }, '"' ;

EscapedChar = UnescapedChar | '\', '"' | '\', '\' ;

UnescapedChar = Letter | Digit | Space | Punctuator | UnicodeHighChar ;

Punctuator =
    '!' | '#' | '$' | '%' | '&' | "'" | '(' | ')' | '*' | '+' | ',' | 
    '-' | '.' | '/' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | '[' |
    ']' | '^' | '`' | '{' | '|' | '}' | '~'
;

(* The 'UnicodeHighChar' specifies all Unicode characters above 0x7F;
   the syntax used is the onw compatible with Grammatica: *)

UnicodeHighChar = ? [^\p{ASCII}] ? ;

(* BEGIN EBNF GRAMMAR Number *)
(* Number token syntax: *)

Number = [ Sign ] ,
         ( Digits, [ '.', [ Digits ] ] | '.' , Digits ),
         [ Exponent ] ;

Exponent =  ( 'e' | 'E' ) , [ Sign ] , Digits ;

Sign = '+' | '-' ;

Digits =  Digit, { Digit } ;

Digit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;

(* END EBNF GRAMMAR Number *)
(* END EBNF GRAMMAR Filter *)
```

## <a name="h.app3">Appendix 3. The regular expressions to check OPTiMaDe number syntax.</a>

```
#BEGIN PCRE numbers
# The string below contains a Perl-Compatible Regular Expression to recognise
# numbers as described in the Minimal API specification:

[-+]?(?:\d+(\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?

#END PCRE numbers

#BEGIN ERE numbers
# The string below contains an Extended Regular Expression to recognise
# numbers as described in the Minimal API specification:

[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?

#END ERE numbers
```
