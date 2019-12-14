#---*- Makefile -*-------------------------------------------------------
#
# This is the makefile for the OPTiMaDe specification
# It contains targets for creating formatted documents,
# auditing / testing the specification documents,
# and a few other helpers.
#
#
# Targets for formatted documents
#################################
#
# - html: renders a html version of the specification
# - pdf: renders a pdf version of the specification
#
#
# Targets for helpers for misc tasks
####################################
#
# - spell: runs an interactive spellchecker
#
#
# Extracting machine-readable parts of the specification
########################################################
#
# - tests/generated/<part>.<format>: extracts the corresponding
#   part from the specification document and places the result
#   in the target file.
#
#   The following such targets exist:
#   - tests/generated/Filter.ebnf
#   - tests/generated/Number.ebnf
#   - tests/generated/identifiers.pcre
#   - tests/generated/numbers.pcre
#   - tests/generated/strings.pcre
#   - tests/generated/identifiers.ere
#   - tests/generated/numbers.ere
#   - tests/generated/strings.ere
#
#
# Targets for testing / auditing the specification
##################################################
#
# Note: the distinction of 'test'-type and 'audit'-type targets is:
#
# - A 'test' target returns successfully if the test
#   could run, even if the test failed.
# - An 'audit' target returns unsuccessfully if the test fails.
#
# These are the targets:
#
# - audit: runs the full suite of audit targets
#
# - docker_audit: dynamically builds a docker image and
#   runs the full suite of audit targets inside it.
#
# - audit_grammar: audits the filter language grammar included
#   in the specification
#
# - audit_authors: audits the AUTHORS file
#
# - audit_spelling: presently a placeholder where we will add audit
#   of the spelling of the specification
#
# - tests: runs the grammar tests
#
# - test_authors: runs tests on the AUTHORS file (checks order)
#
#
# Furthermore, there are some more granular targets specifically for
# testing the grammar.
#
# A typical interaction with the grammar test system runs tests in a
# test directory (tests/cases by default) and report if all tests
# pass.

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

TOOL_DIR ?= tests/tools

PATH := ${PATH}:${TOOL_DIR}

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
