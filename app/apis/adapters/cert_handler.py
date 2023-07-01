import subprocess
from app.apis.adapters import logger
import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import OpenSSL.crypto as crypto
from app.apis.adapters.__config__ import Configuration

config = Configuration()


class CertHandler:
    def __init__(self, pin, cert_id, pkcs11_module='/usr/lib/opensc-pkcs11.so'):
        self.logger = logger.get_logger("CertHandler")

        self.pkcs11_module = pkcs11_module
        self.cert_id = cert_id
        self.pin = pin
        self.output_path = None
        self.target_path_der = None
        self.cert_content = None
        self.parsed_cert = {}

    def insert_certificate(self, certificate_path, slot, cert_label):
        self.logger.info("-insert certificate")
        self.logger.info("--cert id: {}; cert label: {}".format(self.cert_id, cert_label))

        command = [
            "/home/admin/devid_api/app/apis/adapters/bash/insert_certificate.sh",
            f'--certificate_path={certificate_path}',
            f'--hsm_slot={slot}',
            f'--hsm_pin={self.pin}',
            f'--id={self.cert_id}',
            f'--label={cert_label}',
        ]

        subprocess.call(command)

    def export_certificate(self, output_directory, pem = False):
        self.logger.info("-export certificate")
        target_dir = os.path.join(output_directory, "temp_certs")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            self.logger.info(f"--Created directory at {target_dir}")
        self.target_path_der = os.path.join(target_dir, "{}.der".format(self.cert_id))


        self.logger.info("--cert id: {}".format(self.cert_id))
        self.logger.info("--output file: {}".format(self.target_path_der))

        command = [
            "/home/admin/devid_api/app/apis/adapters/bash/export_certificate.sh",
            f'--id={self.cert_id}',
            f'--output_file={self.target_path_der}',
            f'--pin={self.pin}',
        ]

        subprocess.call(command)
        self.load_cert()
        if pem:
            target_path_pem = os.path.join(target_dir, "{}.pem".format(self.cert_id))
            self.logger.info("--output file: {}".format(target_path_pem))
            # Save the PEM certificate to a file
            with open(target_path_pem, "wb") as pem_file:
                pem_file.write(self.cert_content)
            return target_path_pem
        else:
            return self.target_path_der

    def load_cert(self):
        self.logger.info("-load certificate")
        # Load the PEM certificate
        with open(self.target_path_der, 'rb') as der_data:
            der_data = der_data.read()

        # Convert the DER certificate to PEM format
        cert = crypto.load_certificate(crypto.FILETYPE_ASN1, der_data)
        self.cert_content = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)


    def parse_certificate(self):
        self.logger.info("-parse certificate")

        # Parse the certificate
        cert = x509.load_pem_x509_certificate(self.cert_content, default_backend())

        # Extract the issuer
        self.parsed_cert["issuer"] = str(cert.issuer)

        # Extract the validity period
        validFrom = cert.not_valid_before
        validFrom_formatted = validFrom.strftime("%Y-%m-%d %H:%M:%S")
        validTill = cert.not_valid_after
        validTill_formatted = validTill.strftime("%Y-%m-%d %H:%M:%S")
        self.parsed_cert["validFrom"] = validFrom_formatted
        self.parsed_cert["validTill"] = validTill_formatted

        # Extract the serial number
        self.parsed_cert["serial_number_ca"] = cert.serial_number


        # Extract the subject
        subject = cert.subject

        org_name_attr = cert.subject.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)
        org_unit_name_attr = cert.subject.get_attributes_for_oid(x509.NameOID.ORGANIZATIONAL_UNIT_NAME)
        serial_num_attr = cert.subject.get_attributes_for_oid(x509.NameOID.SERIAL_NUMBER)
        country_attr = cert.subject.get_attributes_for_oid(x509.NameOID.COUNTRY_NAME)
        state_attr = cert.subject.get_attributes_for_oid(x509.NameOID.STATE_OR_PROVINCE_NAME)
        pseudonym_attr = cert.subject.get_attributes_for_oid(x509.NameOID.PSEUDONYM)



        # Extract the CN, O, and OU fields from the subject
        self.parsed_cert["cn"] = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value


        self.parsed_cert["o"] = org_name_attr[0].value if org_name_attr else "None"
        self.parsed_cert["ou"] = org_unit_name_attr[0].value if org_unit_name_attr else "None"
        self.parsed_cert["serial_number"] = serial_num_attr[0].value if serial_num_attr else "None"
        self.parsed_cert["c"] = country_attr[0].value if country_attr else "None"
        self.parsed_cert["st"] = state_attr[0].value if state_attr else "None"
        self.parsed_cert["pseudonym"] = pseudonym_attr[0].value if pseudonym_attr else "None"
        self.parsed_cert["cert_str"] = str(self.cert_content)


        self.logger.info(self.parsed_cert)

        return self.parsed_cert


def import_certificate():
    insert_cert = CertHandler(
        pin = config.hsm_pin,
        cert_id = 5,
    )
    insert_cert.insert_certificate(slot=0,
                                   cert_label="test",
                                   certificate_path="/home/admin/certs/test.pem")

def export_certificate():
    export_cert = CertHandler(
        pin = config.hsm_pin,
        cert_id = 5,
    )
    export_cert.export_certificate(output_directory="/home/admin/")

if __name__ == "__main__":
    import_certificate()
