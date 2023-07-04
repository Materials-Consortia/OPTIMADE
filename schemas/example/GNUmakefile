#---*- Makefile -*-------------------------------------------------------

# Use "make schemas schemas_html_pretty=true" to apply OPTIMADE styling to the html pages

# Use "make schemas schemas_html_ext=true" to generate html files with .html extensions also for files meant to be served
# without extensions, which is useful for hosting, e.g., on github that automatically redirects URLs without extensions.

.PHONY: all
all: schemas

PROCESS_SCHEMAS=../../tests/scripts/process_schemas.py
RESOLVE_PATHS_ARGS=--resolve-path ../output
BASE_ID=https://example.org/schemas/

ifeq ($(origin schemas_html_pretty), undefined)
	OPTIMADE_HTML_HEADER ?=
	OPTIMADE_HTML_TOP ?=
else
	OPTIMADE_HTML_HEADER = <link rel="stylesheet" type="text/css" media="screen" href="https://www.optimade.org/assets/css/style.css" /><style>body {background: \#f2f2f2;} html {margin: 0 auto; max-width: 900px;}</style>
	OPTIMADE_HTML_TOP = <a href="https://www.optimade.org/"><img style="margin: 0.5em; float: left" src="https://avatars0.githubusercontent.com/u/23107754" width="10%" /></a><div style="width: 100%; clear: both"></div>
endif

SCHEMAS := $(wildcard src/*/*/*/*/*/*.yaml src/*/*/*/*/*.yaml src/*/*/*/*.yaml src/*/*/*.yaml src/*/*.yaml)
SCHEMAS_JSON = $(patsubst src/%.yaml,output/%.json,$(SCHEMAS))
SCHEMAS_MD = $(patsubst src/%.yaml,output/%.md,$(SCHEMAS))

ifeq ($(origin schemas_html_ext), undefined)
	SCHEMAS_HTML = $(patsubst src/%.yaml,output/%,$(SCHEMAS))
else
	SCHEMAS_HTML = $(patsubst src/%.yaml,output/%.html,$(SCHEMAS))
endif

EXT_SCHEMAS := $(filter-out ../../external/json-schema/LICENSE, $(wildcard ../../external/json-schema/*))
EXT_SCHEMAS_ARGS := $(foreach schema,$(EXT_SCHEMAS),--schema $(schema))

META_SCHEMAS_JSON := $(wildcard ../output/meta/current/optimade/*.json)
META_SCHEMAS_ARGS := $(foreach schema,$(META_SCHEMAS_JSON),--schema $(schema))

INDEXES := $(wildcard src/*)
INDEXES_HTML := $(patsubst src/%,output/%/index.html,$(INDEXES))

.PHONY: schemas

schemas: $(SCHEMAS_JSON) $(SCHEMAS_MD) $(SCHEMAS_HTML) $(INDEXES_HTML)

output/%/index.html: src/% $(SCHEMAS)
	mkdir -p "$(dir $@)"
	$(PROCESS_SCHEMAS) --index --basedir "src" --baseid="$(BASE_ID)" $(RESOLVE_PATHS_ARGS) -f html --html-header '$(OPTIMADE_HTML_HEADER)' --html-top '$(OPTIMADE_HTML_TOP)' $(EXT_SCHEMAS_ARGS) --output "$@" "$<"

output/%.json: src/%.yaml $(META_SCHEMAS_JSON)
	mkdir -p "$(dir $@)"
	$(PROCESS_SCHEMAS) --remove-null --clean-inner-schemas $(RESOLVE_PATHS_ARGS) --basedir "src" --baseid="$(BASE_ID)" $(META_SCHEMAS_ARGS) $(EXT_SCHEMAS_ARGS) --output "$@" "$<"

output/%.md: src/%.yaml
	mkdir -p "$(dir $@)"
	$(PROCESS_SCHEMAS) --remove-null --clean-inner-schemas -f md $(RESOLVE_PATHS_ARGS) --basedir "src" --baseid="$(BASE_ID)" --output "$@" "$<"

ifeq ($(origin schemas_html_ext), undefined)
$(SCHEMAS_HTML): output/%: src/%.yaml
	mkdir -p "$(dir $@)"
	$(PROCESS_SCHEMAS) --remove-null --clean-inner-schemas -f html $(RESOLVE_PATHS_ARGS) --basedir "src" --baseid="$(BASE_ID)" --html-header '$(OPTIMADE_HTML_HEADER)' --html-top '$(OPTIMADE_HTML_TOP)' --output "$@" "$<"
else
$(SCHEMAS_HTML): output/%.html: src/%.yaml
	mkdir -p "$(dir $@)"
	$(PROCESS_SCHEMAS) --remove-null --clean-inner-schemas -f html $(RESOLVE_PATHS_ARGS) --basedir "src" --baseid="$(BASE_ID)" --html-header '$(OPTIMADE_HTML_HEADER)' --html-top '$(OPTIMADE_HTML_TOP)' --output "$@" "$<"
endif

.PHONY: clean clean_schemas

clean: clean_schemas

clean_schemas:
	rm -rf output
