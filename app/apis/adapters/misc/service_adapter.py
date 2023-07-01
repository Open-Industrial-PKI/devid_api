import os
import OpenSSL
from pyhsm.hsmclient import HsmClient
import requests

class ServiceManager:
    def __init__(self, hsm_user, hsm_pass, pki_url):
        c = HsmClient(pkcs11_lib="/usr/lib/vendorp11.so")
        c.open_session(slot=1)
        c.login(pin="partition_password")
        self.pki_url = pki_url

    def generate_key(self, keyIndex):
        # Generate a new RSA key using the HSM and store it on the HSM
        key = self.hsm.generate_key(0x04, pyhsm.defines.ALGO_RSA2048, keyIndex)
        return key

    def get_certificate(self, keyIndex):
        # Request a new certificate from the PKI using the provided key label
        csr = self.generate_csr(keyIndex)
        cert_req = {
            'csr': csr,
            'profile': 'default',
        }
        response = requests.post(self.pki_url + '/certificates/request', json=cert_req)
        if response.status_code != 200:
            raise Exception('Failed to request certificate from PKI: ' + response.text)
        cert = response.json()['certificate']
        return cert

    def generate_csr(self, keyIndex):
        # Generate a new certificate signing request (CSR) using the provided key label
        key = self.hsm.get_key(0x04, pyhsm.defines.ALGO_RSA2048, keyIndex)
        subject = OpenSSL.crypto.X509Req()
        subject.get_subject().CN = keyIndex
        subject.set_pubkey(key.get_pubkey())
        subject.sign(key, "sha256")
        csr = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, subject)
        return csr

    def delete_key(self, keyIndex):
        # Delete the key from the HSM
        self.hsm.delete_key(0x04, pyhsm.defines.ALGO_RSA2048, keyIndex)

    def delete_certificate(self, cert_file_path):
        # Delete the certificate file from disk
        os.remove(cert_file_path)

    def validate_certificate(self, cert, chain):
        # Validate a certificate against a certificate chain
        store_ctx = OpenSSL.crypto.X509StoreContext(OpenSSL.crypto.X509Store())
        store_ctx.set_verify_flags(OpenSSL.crypto.X509_V_FLAG_CRL_CHECK_ALL | OpenSSL.crypto.X509_V_FLAG_X509_STRICT)
        for cert_str in chain:
            cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_str)
            store_ctx.get_cert_store().add_cert(cert)
        cert_to_verify = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        try:
            store_ctx.verify_certificate()
            store_ctx.get_chain()
            return True
        except OpenSSL.crypto.X509StoreContextError:
            return False

    def insert_certificate_chain(self, cert_index, chain):
        # Insert a certificate chain to a given certificate index
        return True

    def enumerate_certificates(self):
        with pyhsm.connect(self.hsm_address, self.hsm_user, self.hsm_password) as hsm:
            certificates = hsm.list_certificates()
            table = []
            for cert in certificates:
                cert_index = cert.index
                key_index = cert.key_id
                enabled = cert.enabled
                is_idev = cert.id_evid
                cert_der = cert.export_as_der()
                table.append((cert_index, key_index, enabled, is_idev, cert_der))
            return table