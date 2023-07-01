import ssl
import OpenSSL.crypto

def verify_id_devid(id_devid_cert_file, root_ca_cert_file):
    # Load the IDevID certificate
    with open(id_devid_cert_file, 'rb') as f:
        id_devid_cert_data = f.read()
    id_devid_cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_ASN1, id_devid_cert_data)

    # Load the root CA certificate
    with open(root_ca_cert_file, 'rb') as f:
        root_ca_cert_data = f.read()
    root_ca_cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_ASN1, root_ca_cert_data)

    # Create a certificate store containing the root CA certificate
    store = OpenSSL.crypto.X509Store()
    store.add_cert(root_ca_cert)

    # Create a certificate context and add the IDevID certificate
    context = OpenSSL.SSL.Context(ssl.PROTOCOL_TLS)
    context.load_verify_locations(cafile=root_ca_cert_file)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    context._set_verify(
        OpenSSL.SSL.VERIFY_PEER | OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
        lambda conn, cert, errno, depth, ok: True)
    context.get_ca_certs()

    # Verify the IDevID certificate against the root CA certificate chain
    try:
        OpenSSL.crypto.X509StoreContext(store, id_devid_cert).verify_certificate()
        return True
    except OpenSSL.crypto.X509StoreContextError:
        return False

result = verify_id_devid('id_devid.crt', 'root_ca.crt')
if result:
    print('IDevID is valid')
else:
    print('IDevID is invalid')