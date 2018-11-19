#! /bin/bash

# Test case: test if a provided EBNF grammar correctly recognises
# integer and real (floating-point) numbers.

BASENAME="$(basename $0)"

#BEGIN DEPEND

INPUT_GRAMMAR=generated/Number.ebnf

#END DEPEND

test -z "${TMP_DIR}" && TMP_DIR="."
TMP_DIR="${TMP_DIR}/tmp-${BASENAME}-$$"
mkdir "${TMP_DIR}"

# To make the trap portable between bash and dash, we need to trap
# "signal" 0 ("EXIT") and rely on it for the cleanup:
## trap "rm -rf '${TMP_DIR}'" 0 1 2 3 15
trap "rm -rf '${TMP_DIR}'" EXIT
trap "exit 1" HUP INT QUIT TERM

TMP_GRAMMAR="${TMP_DIR}/numbers.g"

./tools/grammatiker/EBNF/scripts/ebnf2grammatica ${INPUT_GRAMMAR} \
    > ${TMP_GRAMMAR}

while read LINE
do
    ./tools/grammatiker/BNF/scripts/grammatica-tree \
        ${TMP_GRAMMAR} \
        <(echo -n ${LINE})
done < tests/inputs/integers.lst
