#! /bin/sh

# Test case: test if a provided PCRE correctly recognises integer and
# real (floating-point) numbers.

#BEGIN DEPEND

INPUT_GRAMMAR=generated/numbers.pcre

#END DEPEND

#grep -vP "^$(grep -vE '^#|^ *$' ${INPUT_GRAMMAR})\$" tests/inputs/not-numbers.lst
perl -ne "print unless /^$(grep -vE '^#|^ *$' ${INPUT_GRAMMAR})\$/" tests/inputs/not-numbers.lst
