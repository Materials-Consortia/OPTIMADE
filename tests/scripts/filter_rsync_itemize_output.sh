#!/usr/bin/env python3
#
# Pipe the output of rsync -ni into this script to simplify the output
# so that not all individual files in a new directory show up
# individually (just as a new directory)

import sys

pat = None
for line in sys.stdin:
  stat,sep,f = line.partition(" ")
  f = f.strip()
  if pat is not None and f.startswith(pat):
    continue
  if stat.startswith("cd"):
    pat = f
  sys.stdout.write(line)
