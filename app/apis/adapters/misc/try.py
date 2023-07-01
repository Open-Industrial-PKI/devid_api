import re
import json

# Define a regular expression pattern to match each key-value pair
pattern = r'^\s*([^:]+):\s*(.*?)\s*$'

input_str = 'Private Key Object; RSA \n  label:      my_priv_rsa\n  ID:         68c962b61000000068c962b610000000\n  Usage:      decrypt, sign, unwrap\n  Access:     none\nPublic Key Object; RSA 2048 bits\n  label:      my_rsa_pub\n  ID:         68c962b61000000068c962b610000000\n  Usage:      encrypt, verify, wrap\n  Access:     none\nPrivate Key Object; RSA \n  label:      test\n  ID:         02\n  Usage:      decrypt, sign\n  Access:     none\nPublic Key Object; RSA 2048 bits\n  label:      test\n  ID:         02\n  Usage:      encrypt, verify\n  Access:     none\nProfile object 3031686432\n  profile_id:          CKP_PUBLIC_CERTIFICATES_TOKEN (4)\n'

# Initialize a dictionary to hold the parsed information
data = {}

# Initialize variables to hold the current object's information
current_obj_type = None
current_obj_label = None
current_obj_id = None
current_obj_usage = None
current_obj_access = None

# Split the input by '\n' to iterate over each line
for line in input_str.split('\n'):
    # Use a regular expression pattern to match the object type
    match = re.match(r'^\s*(Private|Public) Key Object;\s*(RSA.*)$', line)
    if match:
        # Extract the object type and label
        current_obj_type = match.group(1).lower()
        current_obj_label = None
        continue

    # Use the regular expression pattern to extract the key and value
    match = re.match(pattern, line)
    if match:
        key = match.group(1)
        value = match.group(2)
        # Check if the key is 'label' to set the current object's label
        if key == 'label':
            current_obj_label = value
        # Check if the key is 'ID', 'Usage', or 'Access' to add it to the current object's dictionary
        elif key == 'ID':
            current_obj_id = value
        elif key == 'Usage':
            current_obj_usage = value
        elif key == 'Access':
            current_obj_access = value
            # Add the object's dictionary to the main dictionary using the label as the key
            if current_obj_label and current_obj_id and current_obj_usage and current_obj_access:
                obj_data = {
                    'ID': current_obj_id,
                    'Usage': current_obj_usage,
                    'Access': current_obj_access,
                }
                if current_obj_type not in data:
                    data[current_obj_type] = {}
                data[current_obj_type][current_obj_label] = obj_data
                # Reset the object variables
                current_obj_label = None
                current_obj_id = None
                current_obj_usage = None
                current_obj_access = None

# Convert the dictionary to a JSON object
json_data = json.dumps(data, indent=4)

print(json_data)