#! /bin/sh

# Test case: test if a provided ERE correctly recognises integer and
# real (floating-point) numbers.

#BEGIN DEPEND

INPUT_GRAMMAR=generated/numbers.ere

#END DEPEND

grep -vE "^$(grep -vE '^#|^ *$' ${INPUT_GRAMMAR})\$" tests/inputs/not-numbers.lst
