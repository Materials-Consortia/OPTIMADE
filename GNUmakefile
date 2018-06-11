#---*- Makefile -*-------------------------------------------------------
# Run tests in a test directory (tests/cases by default) and report if
# all tests pass.

# USAGE:
#     make clean
#     make distclean
#     make tests
#     make

#     make run
#     make run TEXT_TO_PARSE=filter.txt
#     make run TEXT_TO_PARSE=filter.txt GRAMMAR=generated/filters.ebnf

#------------------------------------------------------------------------------

# Include local configuration files from this directory:

MAKECONF_EXAMPLES = ${wildcard Makeconf*.example}
MAKECONF_FILES = \
	$(sort \
		${filter-out %.example,${filter-out %~, ${wildcard Makeconf*}}} \
		${MAKECONF_EXAMPLES:%.example=%} \
	)

ifneq ("${MAKECONF_FILES}","")
include ${MAKECONF_FILES}
endif

# Make local customisable Makeconfig files:

Makecon%: Makecon%.example
	test -f $@ || cp -v $< $@
	test -f $@ && touch $@

#------------------------------------------------------------------------------

.PHONY: all

all:

#------------------------------------------------------------------------------

# Include Makefiles with additional rules for this directory:

MAKELOCAL_FILES = ${filter-out %~, ${wildcard Makelocal*}}

ifneq ("${MAKELOCAL_FILES}","")
include ${MAKELOCAL_FILES}
endif

#------------------------------------------------------------------------------

# The 'make run' target for quick testing of grammars:

GEN_DIR = generated
GRAM_DIR = grammars

GRAMMAR ?= ${GRAM_DIR}/filters.ebnf
GRAMMAT ?= ${GRAMMAR:${GRAM_DIR}/%.ebnf=${GEN_DIR}/%.g}
TEXT_TO_PARSE ?= filter.txt

.PHONY: run

run: ${GRAMMAT}
	awk '{print}' ${TEXT_TO_PARSE}
	./tools/grammatiker/BNF/scripts/grammatica-tree $< ${TEXT_TO_PARSE}

${GEN_DIR}/%.g: $(dir ${GRAMMAR})/%.ebnf
	./tools/grammatiker/EBNF/scripts/ebnf2grammatica $< > $@

#------------------------------------------------------------------------------

.PHONY: clean distclean cleanAll

clean:

distclean cleanAll: clean
