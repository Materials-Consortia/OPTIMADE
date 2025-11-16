#!/bin/bash
# Script to extract field names from optimade.rst Entry List section
# Extracts properties with ~~~~ underlines and groups by entry type

input_file="optimade.rst"

if [[ ! -f "$input_file" ]]; then
    echo "Error: $input_file not found" >&2
    exit 1
fi

# Use awk to process the entire file
awk '
BEGIN {
    in_entry_list = 0
    in_section = 0
    current_section = ""
    prev_line = ""
    print "{"
    first_section = 1
}

# Detect "Entry List" section start
/^Entry List$/ {
    getline  # Read the ===== line
    in_entry_list = 1
    next
}

# Exit Entry List section when we hit another major section (with ======)
in_entry_list && /^=+$/ && prev_line !~ /^Entry List$/ {
    in_entry_list = 0
}

# Detect "Properties Used by Multiple Entry Types"
in_entry_list && /^Properties Used by Multiple Entry Types$/ {
    if (in_section) {
        print "  ],"
    } else if (!first_section) {
        print ","
    }
    print "  \"_common\": ["
    current_section = "_common"
    in_section = 1
    first_section = 0
    first_field = 1
    next
}

# Detect entry type sections (e.g., "Structures Entries")
in_entry_list && /^[A-Z][a-z]+ Entries$/ {
    if (in_section) {
        print ""
        print "  ],"
    } else if (!first_section) {
        print ","
    }
    # Extract entry type name and convert to lowercase
    entry_type = tolower($1)
    printf "  \"%s\": [\n", entry_type
    current_section = entry_type
    in_section = 1
    first_section = 0
    first_field = 1
    next
}

# Detect field names (lines with ~~~~ underneath)
in_section && /^~+$/ && prev_line ~ /^[a-z_][a-z_0-9\\]*$/ {
    # prev_line contains the field name
    if (!first_field) {
        print ","
    }
    # Handle escaped underscores in field names
    field = prev_line
    gsub(/\\/, "", field)  # Remove backslashes
    printf "    \"%s\"", field
    first_field = 0
}

# Store current line for next iteration
{
    prev_line = $0
}

END {
    if (in_section) {
        print ""
        print "  ]"
    }
    print "}"
}
' "$input_file"
