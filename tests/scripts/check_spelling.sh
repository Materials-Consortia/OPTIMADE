#!/bin/bash
spellcheck=$(cat optimade.rst | aspell pipe list -x -M -p ./.words.lst -l en_US 2>&1 | grep "^[&,#]")
if [ -n "$spellcheck" ] ; then
    echo "$spellcheck"
    (>&2 echo "Spelling errors found, please run "make fix_spelling" to fix them interactively.")
    exit 1
fi
