Magnetic moment
---------------


``` json
{
    "$schema": "https://schemas.optimade.org/meta/v1.2.0/optimade/property_definition.md",
    "$id": "https://example.org/schemas/v1.0.0/properties/structures/_exmpl_magnetic_moment",
    "title": "Magnetic moment",
    "x-optimade-type": "list",
    "x-optimade-property": {
        "version": "1.2.0",
        "property-format": "1.2",
        "name": "magnetic_moment",
        "unit-definitions": [
            {
                "$id": "https://schemas.optimade.org/units/v1.2.0/codata/1969/electromagnetic/bohrmagneton",
                "title": "Bohr magneton",
                "symbol": "bohrmagneton",
                "display-symbol": "\\(\\mu_B\\)",
                "description": "A unit expressing the magnetic moment of an electron caused by its orbital or spin angular momentum defined as part of CODATA 1969.\n\n\"The magneton moment of the free electron in units of the Bohr magneton \\(\\mu_B=e\\hbar/2m_e\\)\" [B. N. Taylor, W. H. Parker, and D. N. Langenberg, Rev. Mod. Phys. 41(3), 375-496 (1969)]",
                "standard": {
                    "name": "gnu units",
                    "version": "3.15",
                    "symbol": "bohrmagneton"
                },
                "resources": [
                    {
                        "relation": "Defining paper: B. N. Taylor, W. H. Parker, and D. N. Langenberg, Rev. Mod. Phys. 41(3), 375-496 (1969)",
                        "resource-id": "https://doi.org/10.1103/RevModPhys.41.375"
                    },
                    {
                        "relation": "Wikipedia article describing the unit",
                        "resource-id": "https://en.wikipedia.org/wiki/Bohr_magneton"
                    }
                ],
                "approximate-relations": [
                    {
                        "base-units": [
                            {
                                "symbol": "bohrmagneton",
                                "id": "https://schema.optimade.org/constants/v1.2.0/codata/2018/electromagnetic/bohrmagneton"
                            }
                        ],
                        "base-units-expression": "bohrmagneton"
                    }
                ],
                "x-optimade-definition": {
                    "kind": "unit",
                    "format": "1.2",
                    "version": "1.2.0",
                    "name": "bohrmagneton"
                }
            }
        ]
    },
    "type": [
        "array",
        "null"
    ],
    "description": "The magnetic moment of each atom in the structure in Bohr magnetons (\\(\\mu_B\\)).",
    "examples": [
        [
            [
                0,
                0,
                2.0
            ],
            [
                -1.2,
                0.5,
                1.8
            ]
        ]
    ],
    "x-optimade-unit": "inapplicable",
    "items": {
        "x-optimade-type": "list",
        "type": [
            "array"
        ],
        "x-optimade-unit": "inapplicable",
        "items": {
            "x-optimade-type": "float",
            "type": [
                "number"
            ],
            "x-optimade-unit": "bohrmagneton"
        }
    }
}
```