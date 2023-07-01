#!/bin/bash


while [ $# -gt 0 ]; do
    case "$1" in
        --certificate_path=*) CERTIFICATE_PATH="${1#*=}"; shift 1;;
        --hsm_slot=*) HSM_SLOT="${1#*=}"; shift 1;;
        --hsm_pin=*) HSM_PIN="${1#*=}"; shift 1;;
        --id=*) CERT_ID="${1#*=}"; shift 1;;
        --label=*) CERT_LABEL="${1#*=}"; shift 1;;
        *) echo "Unknown parameter: $1"; exit 1;;
    esac
done

# Check if certificate file exists
if [[ ! -f "$CERTIFICATE_PATH" ]]
then
    echo "Certificate file not found: $CERTIFICATE_PATH"
    exit 1
fi

PKCS11_TOOL=/usr/bin/pkcs11-tool
PKCS11_MODULE=/usr/lib/opensc-pkcs11.so

# Use pkcs11-tool to insert certificate into HSM
$PKCS11_TOOL --module $PKCS11_MODULE \
            --slot "$HSM_SLOT" \
            --pin "$HSM_PIN" \
            --write-object "$CERTIFICATE_PATH" \
            --type cert \
            --id "$CERT_ID" \
            --label "$CERT_LABEL"

# Check if the certificate was successfully inserted
if [[ $? -ne 0 ]]
then
    echo "Failed to insert certificate into HSM"
    exit 1
else
    echo "Certificate inserted into HSM"
    exit 0
fi
