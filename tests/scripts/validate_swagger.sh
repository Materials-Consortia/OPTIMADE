#!/bin/bash
# Takes a filename for an OpenAPI schema as the first argument, and pushes it
# through validator.swagger.io, exiting if the length of the validation response
# is not 0 (i.e. if there are error messages).

set -e

if [ $# -eq 0 ]; then
    echo "Please provide an OpenAPI schema filename!"
    exit 126
fi

echo "Validating schema at ${1}":

response=$(curl -sS -H "Content-Type: application/json" -d @${1} https://validator.swagger.io/validator/debug)
length=$(echo $response | jq 'length')

if [ $length -eq 0 ]; then
    echo "Success!"
    status=0
else
    echo "Schema ${1} failed validation. Response:"
    echo $response
    status=1
fi

exit $status
