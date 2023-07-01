"""EST Client.
based on the implementation of laurentluce
interacting with the EJBCA Campus PKI system
"""

import subprocess
import OpenSSL.crypto
import asn1crypto.core
import est.errors
import est.request

class Client(object):
    """API client.

    Attributes:
        uri (str): URI prefix to use for requests.

        url_prefix (str): URL prefix to use for requests.  scheme://host:port
    """
    url_prefix = None
    username = None
    password = None
    implicit_trust_anchor_cert_path = None

    def __init__(self, host, port, alias, implicit_trust_anchor_cert_path):
        """Initialize the client to interact with the EST server.

        Args:
            host (str): EST server hostname.

            port (int): EST server port number.
            alias (str): user defined alias if not the default EST channel is used
            implicit_trust_anchor_cert_path (str):
                EST server implicit trust anchor certificate path.
        """
        self.url_prefix_base = 'https://%s:%s/.well-known/est' % (host, port)
        if alias:
            self.url_prefix = self.url_prefix_base + alias
        self.implicit_trust_anchor_cert_path = implicit_trust_anchor_cert_path

    def cacerts(self):
        """EST /cacerts request.
        Args:
            None

        Returns:
            str.  CA certificates (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/cacerts'
        content = est.request.get(url,
            verify=self.implicit_trust_anchor_cert_path)

        pem = self.pkcs7_to_pem(content)

        return pem

    def simpleenroll(self, csr):
        """EST /simpleenroll request.

        Args:
            csr (str): Certificate signing request (PEM).

        Returns:
            str.  Signed certificate (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/simpleenroll'
        auth = (self.username, self.password)
        headers = {
            'Content-Type': 'application/pkcs10',
#            'Content-Transfer-Encoding': 'base64',
        }
        content = est.request.post(url, csr, auth=auth, headers=headers,
            verify=self.implicit_trust_anchor_cert_path)
        pem = self.pkcs7_to_pem(content)

        return pem

    def simplereenroll(self, csr, cert=False):
        """EST /simplereenroll request.

        Args:
            csr (str): Certificate signing request (PEM).

            cert (tuple): Client cert path and private key path.

        Returns:
            str.  Signed certificate (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/simplereenroll'
        auth = (self.username, self.password)
        headers = {'Content-Type': 'application/pkcs10'}
        content = est.request.post(url, csr, auth=auth, headers=headers,
            verify=self.implicit_trust_anchor_cert_path,
            cert=cert)
        pem = self.pkcs7_to_pem(content)

        return pem


    def set_basic_auth(self, username, password):
        """Set up HTTP Basic authentication.

        Args:
            username (str).

            password (str).
        """
        self.username = username
        self.password = password

    def create_csr(self, common_name, country=None, state=None, city=None,
                   organization=None, organizational_unit=None,
                   email_address=None, subject_alt_name=None):
        """
        Args:
            common_name (str).

            country (str).

            state (str).

            city (str).

            organization (str).

            organizational_unit (str).

            email_address (str).

            subject_alt_name (str).

        Returns:
            (str, str).  Tuple containing private key and certificate
            signing request (PEM).
        """
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

        req = OpenSSL.crypto.X509Req()
        req.get_subject().CN = common_name
        if country:
            req.get_subject().C = country
        if state:
            req.get_subject().ST = state
        if city:
            req.get_subject().L = city
        if organization:
            req.get_subject().O = organization
        if organizational_unit:
            req.get_subject().OU = organizational_unit
        if email_address:
            req.get_subject().emailAddress = email_address
        if subject_alt_name:
            altName = OpenSSL.crypto.X509Extension(b'subjectAltName', False, subject_alt_name)
            req.add_extensions([altName])

        req.set_pubkey(key)
        req.sign(key, 'sha256')

        private_key = OpenSSL.crypto.dump_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, key)

        csr = OpenSSL.crypto.dump_certificate_request(
                   OpenSSL.crypto.FILETYPE_PEM, req)

        return private_key, csr

    def pkcs7_to_pem(self, pkcs7):
        inform = None
        for filetype in (OpenSSL.crypto.FILETYPE_PEM,
                         OpenSSL.crypto.FILETYPE_ASN1):
            try:
                OpenSSL.crypto.load_pkcs7_data(filetype, pkcs7)
                if filetype == OpenSSL.crypto.FILETYPE_PEM:
                    inform = 'PEM'
                else:
                    inform = 'DER'
                break
            except OpenSSL.crypto.Error:
                pass

        if not inform:
            raise est.errors.Error('Invalid PKCS7 data type')

        stdout, stderr = subprocess.Popen(
            ['openssl', 'pkcs7', '-inform', inform, '-outform', 'PEM',
             '-print_certs'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        ).communicate(pkcs7)

        return stdout.decode("utf-8")
