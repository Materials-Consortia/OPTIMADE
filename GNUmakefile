###############################################################
# This is the OPTiMaDe makefile
# There is no default target, use make <target>.
###############################################################

all:
	@echo "There is no default target for this makefile. Please use make <target>."

clean:
	rm -f AUTHORS.sorted
	$(MAKE) -f tests/GNUmakefile clean

distclean:
	rm -f AUTHORS.sorted
	$(MAKE) -f tests/GNUmakefile distclean

.PHONY: all clean distclean


# Targets for validation of the specification
#############################################

validate: 
	sudo docker build -t optimade . -f tests/Dockerfile
	sudo docker run -it --rm optimade:latest

validate_without_docker: print_make_version validate_grammar validate_authors

.PHONY: validate validate_without_docker

## Print out the version of make
print_make_version:
	$(MAKE) --version

.PHONY: print_make_version

## Grammar validation targets

### Run grammar validation in the OS itself
### (has security considerations since the tests download external code)
validate_grammar:
	$(MAKE) -f tests/GNUmakefile tools
	$(MAKE) -f tests/GNUmakefile grammars
	$(MAKE) -f tests/GNUmakefile tests
	$(MAKE) -f tests/GNUmakefile listdiff 
	(exit $$($(MAKE) -s -f tests/GNUmakefile listdiff | head -n 1 | wc -l))

.PHONY: validate_grammar_docker validate_grammar

## Validate authors sort order

validate_authors: AUTHORS.sorted
	diff AUTHORS AUTHORS.sorted
	rm -f AUTHORS.sorted


# Helper targets 
################

## Spellchecks the document; a clean spellcheck is not yet a validation requirement
spellcheck:
	aspell -x -p ./.words.lst -l en_US -c optimade.rst

## Produce an AUTHORS list with the names in alphabetical order.
## Note: May need extending when new surname prefixes are added, e.g., Di.
AUTHORS.sorted:
	awk '{print} /The OPTiMaDe development team in alphabetical order:/ {exit}' AUTHORS > AUTHORS.sorted
	awk 'NAMES {print} /The OPTiMaDe development team in alphabetical order:/ {NAMES=1}' AUTHORS | sed 's/Di /Di_/' | awk '{printf("%s:%s\n",$$NF,$$0)}' | sort | awk -F: '{print $$2}' | sed 's/Di_/Di /' >> AUTHORS.sorted


# Text extration targets
########################

extract_filter_grammar:
	gawk -F "^    " '/END EBNF GRAMMAR Filter/ {OUT=0} OUT {print $$2} /BEGIN EBNF GRAMMAR Filter/ {OUT=1}' optimade.rst  

extract_number_grammar:
	gawk -F "^    " '/END EBNF GRAMMAR Number/ {OUT=0} OUT {print $$2} /BEGIN EBNF GRAMMAR Number/ {OUT=1}' optimade.rst  

extract_pcre_identifiers:
	gawk -F "^    " '/END PCRE identifiers/ {OUT=0} OUT {print $$2} /BEGIN PCRE identifiers/ {OUT=1}' optimade.rst  

extract_pcre_numbers:
	gawk -F "^    " '/END PCRE numbers/ {OUT=0} OUT {print $$2} /BEGIN PCRE numbers/ {OUT=1}' optimade.rst

extract_pcre_strings:
	gawk -F "^    " '/END PCRE strings/ {OUT=0} OUT {print $$2} /BEGIN PCRE strings/ {OUT=1}' optimade.rst

extract_ere_identifiers:
	gawk -F "^    " '/END ERE identifiers/ {OUT=0} OUT {print $$2} /BEGIN ERE identifiers/ {OUT=1}' optimade.rst  

extract_ere_numbers:
	gawk -F "^    " '/END ERE numbers/ {OUT=0} OUT {print $$2} /BEGIN ERE numbers/ {OUT=1}' optimade.rst

extract_ere_strings:
	gawk -F "^    " '/END ERE strings/ {OUT=0} OUT {print $$2} /BEGIN ERE strings/ {OUT=1}' optimade.rst


.PHONY: extract_filter_grammar extract_number_grammar extract_pcre_identifiers extract_pcre_numbers extract_pcre_strings extract_ere_identifiers extract_ere_numbers extract_ere_strings
