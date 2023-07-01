import json
import requests
from requests_pkcs12 import Pkcs12Adapter
import OpenSSL.crypto
from app.apis.adapters import logger
import base64
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from app.apis.adapters.__config__ import Configuration

config = Configuration()


class CertRequest:
    def __init__(self, base_url, p12_file, p12_pass, csr_file):
        self.logger = logger.get_logger("CertRequest")

        self.base_url = base_url
        self.p12_file = p12_file
        self.p12_pass = p12_pass
        self.csr_file = csr_file

        # Read CSR from file
        with open(csr_file, 'r') as f:
            self.csr = f.read()

    def request_certificate(self, cert_file, certificate_profile_name, end_entity_profile_name, certificate_authority_name, token_user, token_pw, ca_certificate=False):
        self.logger.info("--Request certificate ")
        # Create JSON payload
        try:
            payload = {
                'certificate_request': self.csr,
                'certificate_profile_name': certificate_profile_name,
                'end_entity_profile_name': end_entity_profile_name,
                'certificate_authority_name': certificate_authority_name,
                "username": token_user,
                "password": token_pw
            }
            json_payload = json.dumps(payload)

            url = f'https://{self.base_url}/ejbca/ejbca-rest-api/v1/certificate/pkcs10enroll'

            # Send request
            session = requests.Session()
            session.mount(url, Pkcs12Adapter(max_retries=3, pkcs12_filename=self.p12_file, pkcs12_password=self.p12_pass))
            response = session.post(
                url=url,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                data=json_payload,
                verify=ca_certificate
            )
            response.raise_for_status()  # raise an HTTPError if status code is >= 400
            if "certificate" not in response.text:
                raise Exception("Response does not contain a certificate")

            response = json.loads(response.text)

            self.logger.info("---Save certificate")
            self.logger.info("----Path: {}".format(cert_file))
            self.logger.info("----Certificate: {}".format(response["certificate"]))

            certificate = response["certificate"]

            self.save_cert_to_pem(certificate, cert_file)
            self.get_sha_fingerprint(cert_file)

            self.logger.info("---Certificate received ✅")
            self.logger.info("----Serial number: {}".format(response["serial_number"]))

        except requests.exceptions.HTTPError as err:
            self.logger.error("❌ HTTP error occurred: %s", str(err))
        except requests.exceptions.RequestException as err:
            self.logger.error("❌ An error occurred:", str(err))
        except (json.JSONDecodeError, OSError, KeyError) as e:
            self.logger.error(f"❌ Error requesting certificate: {str(e)}")

    def save_cert_to_pem_legacy(self, certificate_string, cert_path):
        # Insert a newline character after every 64 characters
        formatted_certificate_text = '\n'.join(
            [certificate_string[i:i + 64] for i in range(0, len(certificate_string), 64)])

        with open(cert_path, "w") as certificate_file:
            certificate_file.write("-----BEGIN CERTIFICATE-----\n")
            certificate_file.write(formatted_certificate_text + "\n")
            certificate_file.write("-----END CERTIFICATE-----\n")

    def save_cert_to_pem(self, certificate_string, cert_path):
        self.logger.info("--Save certificate string to PEM file: Filepath: <{}>".format(cert_path))
        # Decode the received text string from base64 and convert it to bytes
        certificate_bytes = base64.b64decode(certificate_string)

        # Parse the certificate bytes as an X.509 certificate
        certificate = x509.load_der_x509_certificate(certificate_bytes, default_backend())

        # Write the certificate to a file in PEM format
        with open(cert_path, 'wb') as f:
            f.write(certificate.public_bytes(encoding=serialization.Encoding.PEM))

    def get_sha_fingerprint(self, cert_path):
        self.logger.info("--Get SHA fingerprint from certificate")
        # Load the certificate from the PEM file
        with open(cert_path, "r") as cert_file:
            cert_data = cert_file.read().encode("ascii")
            cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)

        # Calculate the SHA-256 fingerprint
        fingerprint = cert.digest("sha256").decode("ascii")
        self.logger.info("Certificate fingerprint: {}".format(fingerprint))

if __name__ == "__main__":
    cert_req = CertRequest(
        base_url=config.ejbca_url,
        p12_file=config.p12_auth_file_path,
        p12_pass=config.p12_auth_file_pwd,
        csr_file='/home/admin/certs/id_74976/csr_74976.csr',
    )

    cert_req.request_certificate(cert_file='/home/admin/my_cert.pem',
                                 certificate_profile_name=config.certificate_profile_name_idev,
                                 end_entity_profile_name=config.end_entity_profile_name_idev,
                                 certificate_authority_name=config.certificate_authority_name_idev)
