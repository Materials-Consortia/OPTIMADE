#! /bin/sh

# Test case: tests the equivalence of the provided PCRE and ECMA regular
# expressions used in the validation of space group symmetry operations.
# The equivalence is tested by translating the expression from PCRE to ECMA.

set -ue

#BEGIN DEPEND

INPUT_PCRE_DEFS=tests/generated/symop_definitions.pcre
INPUT_PCRE_GRAMMAR=tests/generated/symops.pcre
INPUT_ECMA_GRAMMAR=tests/generated/symops.ecma

#END DEPEND

PCRE_REGEX=$( \
    grep -v -e '^ *#' -e '^\s+$' ${INPUT_PCRE_GRAMMAR} | \
    perl -ne 's/\s+//g; s/#.*//; s/[\$]$/\\\$/; print;' | \
    perl -ne 's/^[\^][(](.+)[)][(](.+)[)]\{2\}\\[\$]$/^$1$2$2$3\\\$/; print;' \
)

EXPANDED_PCRE_REGEX=$( \
    perl -I. -w \
        -e "require '${INPUT_PCRE_DEFS}';" \
        -e "my \$extended_regex = \"${PCRE_REGEX}\";" \
        -e '$extended_regex =~ s/[\s\\]+//g;' \
        -e 'print $extended_regex;' \
)

ECMA_REGEX=$( \
    grep -v -e '^ *#' -e '^\s+$' ${INPUT_ECMA_GRAMMAR} | \
    perl -n -e 's/\s+//g; print;' \
)

if [ "${EXPANDED_PCRE_REGEX}" = "${ECMA_REGEX}" ]
then
    printf '%s\n' 'PASS: expanded regular expressions match.'
else
    printf '%s\n' 'FAIL: expanded regular expressions do not match.'
    echo "PCRE: ${EXPANDED_PCRE_REGEX}"
    echo "ECMA: ${ECMA_REGEX}"
fi
