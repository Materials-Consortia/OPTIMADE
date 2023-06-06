#! /bin/sh

# Test case: test if a provided PCRE correctly recognises integer and
# real (floating-point) numbers.

#BEGIN DEPEND

INPUT_DEFS=tests/generated/symop_definitions.pcre
INPUT_GRAMMAR=tests/generated/symops.pcre

#END DEPEND

perl -I. -w -ne "
     require '${INPUT_DEFS}';
     print unless /$(grep -v '^ *#' ${INPUT_GRAMMAR} | perl -pe 's/ #.*//')/x
" \
     tests/inputs/symops.lst
