#! /bin/sh

# Test case: test if a provided PCRE correctly recognises integer and
# real (floating-point) numbers.

#BEGIN DEPEND

INPUT_GRAMMAR=generated/numbers.pcre

#END DEPEND

#grep -P "^$(grep -vE '^#|^ *$' ${INPUT_GRAMMAR})\$" tests/inputs/integers.lst
perl -ne "print if /^$(grep -vE '^#|^ *$' ${INPUT_GRAMMAR})\$/" tests/inputs/integers.lst
