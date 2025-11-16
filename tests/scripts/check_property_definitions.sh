#!/bin/bash
# Script to verify that all properties in the specification have corresponding schema definitions
# Compares fields extracted from optimade.rst with schema definition files

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Extract fields from specification
spec_fields=$(tests/scripts/extract_entry_fields.sh)

# Track errors
errors=0
warnings=0

echo "Checking property definitions against specification..."
echo ""

# Function to check if a property definition file exists
check_property() {
    local entry_type=$1
    local property=$2
    local version=${3:-v1.2}  # Default to v1.2

    # Check in the main entry type directory first
    local primary_path="schemas/src/defs/$version/properties/optimade/$entry_type/$property.yaml"

    # Also check v1.3 for newer properties
    local v13_path="schemas/src/defs/v1.3/properties/optimade/$entry_type/$property.yaml"

    # Check core properties (shared across types)
    local core_path="schemas/src/defs/$version/properties/core/$property.yaml"

    if [[ -f "$primary_path" ]] || [[ -f "$v13_path" ]] || [[ -f "$core_path" ]]; then
        return 0
    else
        return 1
    fi
}

# Get the entry types from the JSON output
entry_types=$(echo "$spec_fields" | jq -r 'keys[]')

for entry_type in $entry_types; do
    echo "Checking $entry_type..."

    # Special handling for _common (these should be in core/)
    if [[ "$entry_type" == "_common" ]]; then
        properties=$(echo "$spec_fields" | jq -r '.["_common"][]')
        for property in $properties; do
            # Common properties should exist in core/ or be shared
            if [[ -f "schemas/src/defs/v1.2/properties/core/$property.yaml" ]]; then
                echo -e "  ${GREEN}✓${NC} $property (core)"
            else
                # Check if it exists in any entry type
                found=false
                for et in structures files references calculations; do
                    if check_property "$et" "$property"; then
                        echo -e "  ${GREEN}✓${NC} $property (in $et)"
                        found=true
                        break
                    fi
                done
                if [[ "$found" == "false" ]]; then
                    echo -e "  ${RED}✗${NC} $property - MISSING"
                    ((errors++))
                fi
            fi
        done
    else
        properties=$(echo "$spec_fields" | jq -r --arg et "$entry_type" '.[$et][]')

        # Skip if no properties (empty array) - this is OK for some entry types like calculations
        if [[ -z "$properties" ]]; then
            echo -e "  No specific properties with ~~~~ underlines (uses common properties only)"
            continue
        fi

        for property in $properties; do
            if check_property "$entry_type" "$property"; then
                echo -e "  ${GREEN}✓${NC} $property"
            else
                # Special case: references properties are defined but not with ~~~~ in spec
                if [[ "$entry_type" == "references" ]]; then
                    # References are documented differently, check if the file exists anyway
                    if [[ -f "schemas/src/defs/v1.2/properties/optimade/references/$property.yaml" ]]; then
                        echo -e "  ${GREEN}✓${NC} $property"
                    else
                        echo -e "  ${RED}✗${NC} $property - MISSING"
                        ((errors++))
                    fi
                else
                    echo -e "  ${RED}✗${NC} $property - MISSING"
                    ((errors++))
                fi
            fi
        done
    fi
    echo ""
done

# Also check for orphaned schema files (schemas without spec entries)
echo "Checking for properties defined in schemas but not in specification..."
echo ""

for entry_type in structures files references calculations trajectories; do
    schema_dir="schemas/src/defs/v1.2/properties/optimade/$entry_type"

    if [[ ! -d "$schema_dir" ]]; then
        # Check v1.3
        schema_dir="schemas/src/defs/v1.3/properties/optimade/$entry_type"
        if [[ ! -d "$schema_dir" ]]; then
            continue
        fi
    fi

    # Get properties from spec for this entry type
    if [[ "$entry_type" == "trajectories" ]]; then
        spec_props=$(echo "$spec_fields" | jq -r '.trajectories[]?' 2>/dev/null || echo "")
    else
        spec_props=$(echo "$spec_fields" | jq -r --arg et "$entry_type" '.[$et][]?' 2>/dev/null || echo "")
    fi

    # Also include common properties
    common_props=$(echo "$spec_fields" | jq -r '._common[]?' 2>/dev/null || echo "")
    all_spec_props=$(echo -e "$spec_props\n$common_props" | sort | uniq)

    # Find all schema files
    for schema_file in "$schema_dir"/*.yaml; do
        if [[ ! -f "$schema_file" ]]; then
            continue
        fi

        property=$(basename "$schema_file" .yaml)

        # Check if this property is in the spec
        if echo "$all_spec_props" | grep -q "^${property}$"; then
            : # Found, nothing to do
        else
            if [[ "$entry_type" == "references" ]]; then
                # References properties might not be in spec with ~~~~ but still valid
                if grep -q "^${property}$" <<< "$spec_props"; then
                    echo -e "  ${GREEN}✓${NC} $entry_type/$property"
                    continue
                fi
            else  
                echo -e "  ${YELLOW}⚠${NC} $entry_type/$property - Schema exists but not in specification (or uses different formatting)"
                ((warnings++))
            fi
        fi
    done
done

echo ""
echo "=============================================="
echo "Summary:"
echo "  Errors: $errors"
echo "  Warnings: $warnings"
echo "=============================================="

if [[ $errors -gt 0 ]]; then
    exit 1
else
    exit 0
fi
