#!/usr/bin/env python3

import argparse
import json
import yaml

def process(filename):

    with open(filename, 'r') as f:
         parsed = yaml.safe_load(f)
         print(json.dumps(parsed, indent=4))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process YAML property definition into JSON", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('yamlfile', help='The YAML formatted property definition file.')
    parser.set_defaults(dry=False)
    args = parser.parse_args()

    process(args.yamlfile)
