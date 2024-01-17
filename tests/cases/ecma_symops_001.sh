#! /bin/sh

# Test case: test if the provided ECMA-compatible regular expression correctly
# recognises symmetry operation strings.

#BEGIN DEPEND

INPUT_GRAMMAR=tests/generated/symops.ecma

#END DEPEND


/usr/bin/env python << EOF
import re
import sys
with open("${INPUT_GRAMMAR}") as f:
    expression = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith("#")][0]

with open("tests/inputs/symops.lst") as cases:
    for case in cases:
        if re.match(expression, case):
            print(case, end="")
EOF
