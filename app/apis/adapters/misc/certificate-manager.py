import OpenSSL
import os
import json
import shutil
from pathlib import Path



class X509CertificateManager:
    def __init__(self, cert_directory):
        self.cert_directory = cert_directory

    def enumerate_certificates(self):
        certificates = []
        for root, dirs, files in os.walk(self.cert_directory):
            for filename in files:
                cert_file_path = os.path.join(root, filename)
                with open(cert_file_path, "rb") as f:
                    cert_bytes = f.read()
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_bytes)
                certificate_index = cert.get_serial_number()
                key_index = cert.get_issuer().hash()
                enabled = Path(cert_file_path) == "enabled"
                is_id_evid = False  # Change this to the actual is_id_evid value
                self.certificates.append((certificate_index, key_index, enabled, is_id_evid, cert_bytes))
        return certificates

    def enable_certificate_by_index(self, certificateIndex):
        target_dir = 'enabled'
        for root, dirs, files in os.walk(self.cert_directory):
            for filename in files:
                cert_file_path = os.path.join(root, filename)
                with open(cert_file_path, "rb") as f:
                    cert_bytes = f.read()
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_bytes)
                if cert.get_subject().CN == certificateIndex:
                    path = Path(cert_file_path)
                    if path.parent.absolute() == "enabled":
                        return json.dumps({
                            "success": True,
                            "message": f"Certificate with the Index {certificateIndex} is already ENABLED"
                        })
                    else:
                        try:
                            target_path = os.path.join(self.cert_directory, target_dir, os.path.basename(self.cert_path))
                            shutil.move(cert_file_path, target_path)
                        except FileNotFoundError:
                            return json.dumps({
                                "success": False,
                                "message": f"No certificate found for {certificateIndex}"
                            })
                        else:
                            return json.dumps({
                                "success": True,
                                "message": f"Successfully moved certificate for {certificateIndex} to ENABLED"
                            })

    def disable_certificate_by_index(self, certificateIndex):
        target_dir = 'disabled'
        for root, dirs, files in os.walk(self.cert_directory):
            for filename in files:
                cert_file_path = os.path.join(root, filename)
                with open(cert_file_path, "rb") as f:
                    cert_bytes = f.read()
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_bytes)
                if cert.get_subject().CN == certificateIndex:
                    path = Path(cert_file_path)
                    if path.parent.absolute() == "enabled":
                        return json.dumps({
                            "success": True,
                            "message": f"Certificate with the Index {certificateIndex} is already DISABLED"
                        })
                    else:
                        try:
                            target_path = os.path.join(self.cert_directory, target_dir, os.path.basename(self.cert_path))
                            shutil.move(cert_file_path, target_path)
                        except FileNotFoundError:
                            return json.dumps({
                                "success": False,
                                "message": f"No certificate found for {certificateIndex}"
                            })
                        else:
                            return json.dumps({
                                "success": True,
                                "message": f"Successfully moved certificate for {certificateIndex} to DISABLED"
                            })

    def delete_certificate_by_index(self, certificateIndex):
        for filename in os.listdir(self.cert_directory):
            cert_file_path = os.path.join(self.cert_directory, filename)
            with open(cert_file_path, "rb") as f:
                cert_bytes = f.read()
            cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_bytes)
            if cert.get_subject().CN == certificateIndex:
                try:
                    os.remove(cert_file_path)
                except FileNotFoundError:
                    return json.dumps({
                        "success": False,
                        "message": f"No certificate found for {certificateIndex}"
                    })
                else:
                    return json.dumps({
                        "success": True,
                        "message": f"Successfully deleted certificate for {certificateIndex}"
                    })