#!/bin/bash
#
# Builds an HTML version of the OPTIMADE specification.
# Intended use is either:
#   * via the makefile at the root of the repository.
#   * directly using a Docker invocation like:
#       docker run \
#            -v `pwd`:/data \
#            --entrypoint /data/tests/makefiles/build_html.sh \
#            pandoc/ubuntu:latest \
#            optimade.rst

# Setting the `--metadata-file` will not work if called from
# other dirs.

# pandoc does not quite understand .rst '.. comment' blocks
sed -z "s/.. comment\n/.. /g" $1 > .stripped_comments.rst
pandoc \
    --standalone \
    --toc \
    --number-sections \
    --metadata-file=./tests/makefiles/html_build_metadata.yml \
    .stripped_comments.rst \
    -o ${1/.rst/.html}
rm .stripped_comments.rst