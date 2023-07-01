import json
import subprocess
import re
from app.apis.adapters.__config__ import Configuration

config = Configuration()

# Execute the p11tool command and capture its output
cmd = ['p11tool', '--provider=/usr/lib/opensc-pkcs11.so', '--list-keys', '--login', '--set-pin={}'.format(config.hsm_pin)]
output = subprocess.check_output(cmd, universal_newlines=True)


print(output)
# Define a regular expression pattern to extract each field from an object
pattern = r"Object (\d+):\n\s+URL: (.+)\n\s+Type: (.+)\n\s+Label: (.+)\n\s+Flags: (.+)\n\s+ID: (.+)"

# Extract the information from each object and store it in a dictionary
objects = []
for match in re.finditer(pattern, output):
    obj = {
        "index": match.group(1),
        "url": match.group(2),
        "type": match.group(3),
        "label": match.group(4),
        "flags": match.group(5),
        "id": match.group(6),
    }
    objects.append(obj)

# Convert the list of dictionaries to a JSON object
json_output = json.dumps(objects, indent=4)

# Print the JSON object
print(json_output)