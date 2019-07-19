#! /bin/bash

# Test case: test if a provided EBNF grammar correctly recognises
# integer and real (floating-point) numbers.

#BEGIN DEPEND

INPUT_GRAMMAR=tests/generated/Number.ebnf

#END DEPEND

tests/tools/grammatiker/BNF/scripts/grammatica-tree \
    <(tests/tools/grammatiker/EBNF/scripts/ebnf2grammatica ${INPUT_GRAMMAR}) \
    <(echo -n 1234)
