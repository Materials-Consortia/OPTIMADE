#! /bin/sh

# Test case: test if a provided PCRE correctly recognises integer and
# real (floating-point) numbers.

#BEGIN DEPEND

INPUT_GRAMMAR=tests/generated/identifiers.pcre

#END DEPEND

grep -v -P "^$(grep -vE '^#|^ *$' ${INPUT_GRAMMAR})\$" tests/inputs/not-identifiers.lst
