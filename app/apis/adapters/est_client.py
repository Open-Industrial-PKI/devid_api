import re

class ESTClient:
    def __init__(self, host, port, alias, implicit_trust_anchor_cert_path):
        self.host = host
        self.port = port
        self.alias = alias
        self.implicit_trust_anchor_cert_path = implicit_trust_anchor_cert_path
        self.client = app.apis.adapters.est.client.Client(host, port, alias, implicit_trust_anchor_cert_path)

    def set_basic_auth(self, username, password):
        self.client.set_basic_auth(username, password)

    def create_csr(self, common_name, organization, organizational_unit, country, subject_alt_name):
        priv, csr = self.client.create_csr(common_name=common_name,
                                           organization=organization,
                                           organizational_unit=organizational_unit,
                                           country=country,
                                           subject_alt_name=subject_alt_name)
        m = re.search(r"(?<=-----BEGIN CERTIFICATE REQUEST-----).*?(?=-----END CERTIFICATE REQUEST-----)", csr.decode(), flags=re.DOTALL)
        csr = m.group()
        return priv, csr

    def simpleenroll(self, csr):
        return self.client.simpleenroll(csr)

    def get_ca_certs(self):
        return self.client.cacerts()

if __name__ == "__main__":

    client = ESTClient('campuspki.com', 443, '/Test_PC_OPC_Server', 'ManagementCA-chain.pem')

    username = 'test'
    password = 'test'
    client.set_basic_auth(username, password)

    common_name = 'test_cn'
    country = 'DE'
    organization = 'Campus Schwarzwald'
    organization_unit = 'IEEE 802.1 AR'
    subject_alt_name = b'URI:http://www.ietf.org/rfc/rfc3986.txt'

    priv, csr = client.create_csr(common_name=common_name,
                                  organization=organization,
                                  organizational_unit=organization_unit,
                                  country=country,
                                  subject_alt_name=subject_alt_name)

    client_cert = client.simpleenroll(csr)
    print(client_cert)

    ca_certs = client.get_ca_certs()

