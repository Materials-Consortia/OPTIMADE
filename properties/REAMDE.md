# Property definitions

The subdirectories below contain source files for property definitions for the standard OPTIMADE properties.
They are organized with one subdirectory per OPTIMADE endpoint, and one directory `common` for common definitions used across multiple endpoints.

The source files are formatted in yaml to be human-editable and uses JSON Schema pointers to to avoid duplication of information.

The source files can be compiled into standard JSON-formatted property definitions by the command:
```
make properties
```
The JSON-formatted (and thus JSON Schema-compatible) output files are placed alongside the source files without filename extensions.
Note that this process replaces the JSON Schema pointers with verbatim copies of the corresponding definitions.
