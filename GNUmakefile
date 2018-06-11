#---*- Makefile -*-------------------------------------------------------
# Run tests in a test directory (tests/cases by default) and report if
# all tests pass.

# USAGE:
#     make clean
#     make distclean
#     make tests
#     make

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

.PHONY: clean distclean cleanAll

clean:

distclean cleanAll: clean
