#!/bin/bash

# Parse command-line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --output_file=*) CERT_FILE="${1#*=}"; shift 1;;
        --id=*) CERT_ID="${1#*=}"; shift 1;;
        --pin=*) PIN="${1#*=}"; shift 1;;
        *) echo "Unknown parameter: $1"; exit 1;;
    esac
done

PKCS11_TOOL=/usr/bin/pkcs11-tool
PKCS11_MODULE=/usr/lib/opensc-pkcs11.so

# Use pkcs11-tool to export certificate from HSM
$PKCS11_TOOL --module "$PKCS11_MODULE" \
            --read-object \
            --type cert \
            --id "$CERT_ID" \
            --output-file "$CERT_FILE"

# Check if the certificate was successfully exported
if [[ $? -ne 0 ]]
then
    echo "Failed to export certificate from HSM"
    exit 1
else
    echo "Certificate exported from HSM"
    exit 0
fi
