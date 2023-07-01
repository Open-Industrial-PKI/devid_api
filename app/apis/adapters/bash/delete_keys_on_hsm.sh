#!/bin/bash

# Set the path to the PKCS11 tool
PKCS11_TOOL=/usr/bin/pkcs11-tool

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --key_type=*) key_type="${1#*=}"; shift 1;;
        --id=*) id="${1#*=}"; shift 1;;
        --pin=*) pin="${1#*=}"; shift 1;;
        *) echo "Unknown parameter: $1"; exit 1;;
    esac
done

# Check that all required arguments were provided
if [[ -z "$key_type" || -z "$id" || -z "$pin" ]]
then
    echo "Usage: $0 --key_type <key_type> --id <id> --pin <pin>"
    exit 1
fi

# Run the PKCS11 tool command to delete the object
$PKCS11_TOOL --delete-object --type "$key_type" --id=$id --login --pin $pin
