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
#     make run TEXT_TO_PARSE=filter.txt GRAMMAR=grammars/filters.ebnf

#------------------------------------------------------------------------------

# Include local configuration files from this directory:

MAKEFILE_DIR = tests/makefiles

MAKECONF_EXAMPLES = ${wildcard ${MAKEFILE_DIR}/Makeconf*.example}
MAKECONF_FILES = \
	$(sort \
		${filter-out %.example, \
		${filter-out %~, ${wildcard ${MAKEFILE_DIR}/Makeconf*}}} \
		${MAKECONF_EXAMPLES:%.example=%} \
	)

ifneq ("${MAKECONF_FILES}","")
include ${MAKECONF_FILES}
endif

TOOLS_PATH ?= tests/tools

PATH := ${PATH}:${TOOLS_PATH}

# Make local customisable Makeconfig files:

Makecon%: Makecon%.example
	test -f $@ || cp -v $< $@
	test -f $@ && touch $@

#------------------------------------------------------------------------------

.PHONY: all

all:

#------------------------------------------------------------------------------

# Include Makefiles with additional rules for this directory:

MAKELOCAL_FILES = ${filter-out %~, ${wildcard ${MAKEFILE_DIR}/Makelocal*}}

ifneq ("${MAKELOCAL_FILES}","")
include ${MAKELOCAL_FILES}
endif

#------------------------------------------------------------------------------

.PHONY: clean distclean cleanAll

clean:

distclean cleanAll: clean ${DISTCLEAN_TARGETS}
