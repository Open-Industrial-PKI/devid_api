#!/bin/bash

# Usage:
# bash /home/admin/devid_api/app/core/adapters/bash/generate_csr.sh --key-id="3" --output-file="/home/admin/test_csr_setup_1.csr" --cn="test_csr_setup_1"

# Parse named arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --key-id=*) key_id="${1#*=}"; shift 1;;
        --output-file=*) output_file="${1#*=}"; shift 1;;
        --hsm-pin=*) hsm_pin="${1#*=}"; shift 1;;
        --cn=*) cn="${1#*=}"; shift 1;;
        --o=*) o="${1#*=}"; shift 1;;
        --ou=*) ou="${1#*=}"; shift 1;;
        --c=*) c="${1#*=}"; shift 1;;
        --serial-number=*) serial_number="${1#*=}"; shift 1;;
        --pseudonym=*) pseudonym="${1#*=}"; shift 1;;
        *) echo "Unknown parameter: $1"; exit 1;;
    esac
done


# Concatenate the subject fields
subj="/CN=$cn"
if [ ! -z "$o" ]; then subj="$subj/O=$o"; fi
if [ ! -z "$ou" ]; then subj="$subj/OU=$ou"; fi
if [ ! -z "$c" ]; then subj="$subj/C=$c"; fi
if [ ! -z "$serial_number" ]; then subj="$subj/serialNumber=$serial_number"; fi
if [ ! -z "$pseudonym" ]; then subj="$subj/pseudonym=$pseudonym"; fi


# Generate CSR using openssl command
openssl req -engine pkcs11 -keyform engine -subj "$subj" -key "$key_id" -passin pass:"$hsm_pin" -new -sha256 -out $output_file --verbose

