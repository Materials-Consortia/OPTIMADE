#!/bin/bash
spellcheck=$(aspell list -M -p ./.words.lst -l en_US < optimade.rst)
if [ -n "$spellcheck" ] ; then
    echo "$spellcheck"
    (>&2 echo "Spelling errors found, please run "make fix_spelling" to fix them interactively.")
    exit 1
fi
