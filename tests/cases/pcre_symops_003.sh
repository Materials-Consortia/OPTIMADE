#! /bin/sh

# Test case: test if the PCRE given in the OPTIMADE standard correctly
# recognises symmetry operations from the 'optimade.rst' examples:

#BEGIN DEPEND

INPUT_DEFS=tests/generated/symop_definitions.pcre
INPUT_GRAMMAR=tests/generated/symops.pcre

#END DEPEND

perl -I. -w -ne "
     require '${INPUT_DEFS}';
     print if /$(grep -v '^ *#' ${INPUT_GRAMMAR} | perl -pe 's/ #.*//')/x
" \
<<EOF
x,y,z
-x,y,-z
x+1/2,y+1/2,z
-x+1/2,y+1/2,-z
EOF
