#!/bin/bash

input='Private Key Object; RSA \n
label:      my_priv_rsa\n
ID:         68c962b61000000068c962b610000000\n
Usage:      decrypt, sign, unwrap\n
Access:     none\n
Public Key Object; RSA 2048 bits\n
label:      my_rsa_pub\n
ID:         68c962b61000000068c962b610000000\n
Usage:      encrypt, verify, wrap\n
Access:     none\n'

# Remove newline characters and replace colons with keys to create JSON object
json=$input
#$(echo "$input" | tr '\n' ' ' | sed -e 's/ *: */": "/g' -e 's/ *\([^ ]* \)/"\1/g' -e 's/ *$//g')


# Split input string into arrays based on "Private Key Object" and "Public Key Object"
priv_key=()
pub_key=()
while read -r line; do
    if [[ $line == *"Private Key Object; RSA"* ]]; then
        priv_key+=("{")
        priv_key+=("[")
    elif [[ $line == *"Public Key Object; RSA 2048 bits"* ]]; then
        pub_key+=("{")
        pub_key+=("[")
    fi
    if [[ $line != *"Private Key Object; RSA"* && ! -z "${priv_key[1]}" ]]; then
        priv_key+=("$line")
    fi
    if [[ $line != *"Public Key Object; RSA 2048 bits"* && ! -z "${pub_key[1]}" ]]; then
        pub_key+=("$line")
    fi
done <<< "$json"

# Add sub-objects to Private Key Object and Public Key Object arrays
priv_key+=('}')
priv_key+=(']')
priv_key=$(printf '%s\n' "${priv_key[@]}" | sed -e 's/ Private Key Object; RSA / Private Key Object; RSA:\n[ { /')
priv_key=$(echo "$priv_key" | sed -e 's/"Access": /"Access": "/')

pub_key+=('}')
pub_key+=(']')
pub_key=$(printf '%s\n' "${pub_key[@]}" | sed -e 's/ Public Key Object; RSA 2048 bits / Public Key Object; RSA 2048 bits:\n[ { /')
pub_key=$(echo "$pub_key" | sed -e 's/"Access": /"Access": "/')

# Combine arrays into single JSON object
json='{'
json+="$priv_key,"
json+="$pub_key"
json+='}'

echo "$json"
