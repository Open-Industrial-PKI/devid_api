import re

# Open the input file and read its contents
with open('c/origin/iothub_ll_client_x509_sample.c', 'r') as f:
    content = f.read()

with open("/home/admin/certs/my_cert_3443.pem", "r") as cert_file:
    cert_data = cert_file.read()

c_format_certificate = 'static const char* x509certificate = \n"' + cert_data.replace('"', '\\"').replace('\n', '\\n"\n"') + '";\n'


# Define a dictionary of replacement strings
replacements = {
    '<host_name>': 'testdevice123',
    '<device_id>': 'common_name_of_the_cert',
    '<x509privatekey>': 'pkcs11:model=PKCS%2315;manufacturer=unknown;serial=0000;token=JavaCard%20isoApplet%20%28User%20PIN%29;id=%10%1F%15%A6%7F%00%00%00%10%00%00%00%00%00%00%00;object=ldev_pvt_key_3443;type=private;pinvalue=1234;',
    '/* placeholder x509privatekey */': c_format_certificate
}

# Loop through each key-value pair in the replacements dictionary
for pattern, replacement in replacements.items():
    # Use the re.sub() method to replace all occurrences of the pattern with the replacement string
    content = re.sub(pattern, replacement, content)

# Open the output file and write the modified contents
with open('./c/test_2.c', 'w') as f:
    f.write(content)