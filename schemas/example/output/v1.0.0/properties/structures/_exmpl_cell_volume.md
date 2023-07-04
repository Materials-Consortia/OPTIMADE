# Cell volume (property)
This page documents an [OPTIMADE](https://www.optimade.org/) [Property Definition](https://schemas.optimade.org/#definitions). See [https://schemas.optimade.org/](https://schemas.optimade.org/) for more information.

**ID: [`https://example.org/schemas/v1.0.0/properties/structures/_exmpl_cell_volume`](https://example.org/schemas/v1.0.0/properties/structures/_exmpl_cell_volume)**  
**Definition name:** `_exmpl_cell_volume`

**Property name:** Cell volume  
**Description:** The volume of the unit cell in in ångström cubed ($\AA^3$).  
**Type:** float  



**Examples:**

- `42.0`

**Formats:** [[JSON](_exmpl_cell_volume.json)] [[MD](_exmpl_cell_volume.md)]

**JSON definition:**

``` json
{
    "$schema": "https://schemas.optimade.org/meta/v1.2.0/optimade/property_definition.md",
    "$id": "https://example.org/schemas/v1.0.0/properties/structures/_exmpl_cell_volume",
    "title": "Cell volume",
    "$comment": "This is an example of a database provider-specific property definition.",
    "x-optimade-type": "float",
    "x-optimade-definition": {
        "kind": "property",
        "version": "1.2.0",
        "format": "1.2",
        "name": "_exmpl_cell_volume"
    },
    "x-optimade-unit-definitions": [
        {
            "$id": "https://schemas.optimade.org/units/v1.2.0/si/general/angstrom",
            "title": "\u00e5ngstr\u00f6m",
            "symbol": "angstrom",
            "display-symbol": "\u00c5",
            "description": "A unit of length equal to 10\u207b\u00b9\u2070 meter, using the current, or one of the historical, definitions of the SI units.\n\nThe \u00e5ngstr\u00f6m appear in the International System of Units (SI), 1th ed. (1970) defined as \"1 \u00c5 = 0.1 nm = 10\u207b\u00b9\u2070 m\".\n\nThe \u00e5ngstr\u00f6m was implicitly redefined via the redefinition of the metre at the 17th CGPM meeting (1983), resolution 1.\n\nThe International System of Units (SI), 1th ed. (1970) categorizes the unit as \"temporarily admitted\" for use with the SI units.\nThe International System of Units (SI), 7th ed. (1998) changes the categorisation to \"Other non-SI units currently accepted for use with the International System.\"\nThe International System of Units (SI), 8th ed. (2006) changes the categorization to \"Other non-SI units\" and adds as a clarifying footnote \"The \u00e5ngstr\u00f6m is widely used by x-ray crystallographers and structural chemists because all chemical bonds lie in the range 1 to 3 \u00e5ngstr\u00f6ms. However it has no official sanction from the CIPM or the CGPM.\"\nThe \u00e5ngstr\u00f6m is omitted in the International System of Units (SI), 9th Edition (2019).\n\nThis is a generalized definition taken to reference the current, or one of the historical, SI unit definitions.\nThis definition is intended for situations when it is not possible to be more precise, e.g., in contexts where data have been collected that uses different historical SI definitions.",
            "compatibility": [
                "https://schemas.optimade.org/units/v1.2.0/si/1970/temporary/angstrom",
                "https://schemas.optimade.org/units/v1.2.0/si/1983/temporary/angstrom"
            ],
            "standard": {
                "name": "gnu units",
                "version": "3.15",
                "symbol": "angstrom"
            },
            "resources": [
                {
                    "relation": "Definition in the International System of Units (SI), 1th Edition",
                    "resource-id": "https://www.bipm.org/en/publications/si-brochure"
                },
                {
                    "relation": "Redefinition of the metre at the 17th CGPM meeting (1983), resolution 1",
                    "resource-id": "https://www.bipm.org/en/committees/cg/cgpm/17-1983/resolution-1"
                },
                {
                    "relation": "Wikipedia article describing the unit",
                    "resource-id": "https://en.wikipedia.org/wiki/Angstrom"
                }
            ],
            "defining-relation": {
                "base-units": [
                    {
                        "symbol": "m",
                        "id": "https://schema.optimade.org/units/v1.2.0/si/general/metre"
                    }
                ],
                "base-units-expression": "m",
                "scale": {
                    "exponent": -10
                }
            },
            "x-optimade-definition": {
                "kind": "unit",
                "format": "1.2",
                "version": "1.2.0",
                "name": "angstrom"
            }
        }
    ],
    "type": [
        "number",
        "null"
    ],
    "description": "The volume of the unit cell in in \u00e5ngstr\u00f6m cubed ($\\AA^3$).",
    "examples": [
        42.0
    ],
    "x-optimade-unit": "angstrom^3",
    "minimum": 0.0
}
```