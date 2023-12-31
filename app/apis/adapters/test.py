import base64
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

certificate_string="MIIDMjCCAhqgAwIBAgIUa4itR6+qM2dawdxN2rKQUUl48XswDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UEAwwRS0YtQ1MtSE1JLTIwMjMtQ0EwHhcNMjMwNDA0MTQ0MjAzWhcNMjgwMjIyMTI1NDIyWjAoMRYwFAYDVQQDDA1pZGV2X2NuXzU4MTIyMQ4wDAYDVQQFEwU1ODEyMjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAIF3wGv90tXjuS+9HqTTnQD4k1hQ6S15b3tiogR4pTwJ3bRH+cX9xe00sb+5VdrZxaexT2/JOxJMakdp61gIHihj4EF2Xp3nRRRneJJRB1RpIIQU1vouPU6DdnYIgcMQOerfd8QI7bs4pNciwQB/ArnkDq2oFrcTpeyvlP0rnR592P+XKPv4fOC4szLvLmXpj8wZmTQPbBNlX+RnMBkZ2NYH+w3FMlyxng57KgAOmWiGv6VwOtz3XE05dprgUvXz9c2qFS+4rrmYxrT9jGtnqNUDlypxemCBZfXsGcOHp85f6meiPUS0EuW27Usuq/rVW31dUTART+XeFDGCYLDFZKkCAwEAAaNgMF4wDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBRs7vNgClxEU6UoQr91oJLS4r/nPjAdBgNVHQ4EFgQUi+9PStOWc56zay0JcyrbSB94Tn0wDgYDVR0PAQH/BAQDAgWgMA0GCSqGSIb3DQEBCwUAA4IBAQC7MePcib1pDed7t6ESRhucrIKqfTNUEYhnNT+E0z0fsSQpBjkQjeuSR3sGNjRjzlDsYmjZFjsyIxkdgAzMrJXE7OVUTr7ZIkiaQeUHoBAHvURlo6cDzlNnCeplG3sF4HxRre1WOydD5BPh3k2uMiII0QMDWlfBm/2FiX0GSRn9ZB8r3mo1xalFuCgTcm8Rz1JzGZdtY8MKl2mUTCEmVpLygCvfZx6HTsyZ/Lx/3798PPbQRBD3oN71wWM9qRcJuW9M9L33YUpu9/SobwVJVUb6h8juY20uoYquwsxbDozw3+1JftlEEiLYLzgzxRkKeAEyHMadfoFK8Dy9ZQL/bUP9"
cert_path="thisisatest.pem"
# Decode the received text string from base64 and convert it to bytes
certificate_bytes = base64.b64decode(certificate_string)

# Parse the certificate bytes as an X.509 certificate
certificate = x509.load_der_x509_certificate(certificate_bytes, default_backend())

# Write the certificate to a file in PEM format
with open(cert_path, 'wb') as f:
    f.write(certificate.public_bytes(encoding=serialization.Encoding.PEM))