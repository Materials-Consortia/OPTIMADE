#!/usr/bin/env python3
"""
This script validates a json file against a JSON Schema file using the jsonschema Python library.

Usage:
  validate_json_schema.py jsonfile schemafile

Examples:
  validate_json_schema.py file.json schema.json

"""

import argparse
import json

import jsonschema
from jsonschema import validate

arguments = [
    {
        'names': ['infile'],
        'help': 'The JSON file to process.',
        'type': str,
    },
    {
        'names': ['schema'],
        'help': 'The JSON Schema file to process.',
        'type': str,
    }
]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for arg in arguments:
        names = arg.pop('names')
        parser.add_argument(*names, **arg)

    args = parser.parse_args()

    with open(args.infile, "r") as f:
        data=json.load(f)
    with open(args.schema, "r") as f:
        schema=json.load(f)

    validate(instance=data, schema=schema, format_checker=jsonschema.FormatChecker())

    print("JSON file: "+str(args.infile)+" validated against JSON Schema: "+str(args.schema)+": OK")
