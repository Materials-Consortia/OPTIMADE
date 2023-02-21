# Property definitions

The src subdirectory contains source files for property definitions for the standard OPTIMADE properties.
They are organized with one subdirectory per OPTIMADE endpoint, and one directory `common` for common definitions used across multiple endpoints.

The source files are formatted in YAML to be human-editable and use JSON Schema pointers to avoid duplication of information.

The source files can be compiled into standard JSON-formatted property definitions by the command:
```
make properties
```
The JSON-formatted (and thus JSON Schema-compatible) output files are placed in the output directory.
Note that this process replaces the JSON Schema pointers by inline copies of the corresponding definitions to adhere to the OPTIMADE standard for property definitions.
