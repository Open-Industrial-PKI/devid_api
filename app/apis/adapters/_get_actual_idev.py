from cert_handler import CertHandler
from hsm_objects import HsmObjects
from app.apis.adapters.__config__ import Configuration

config = Configuration()

def main():
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    hsm_idev_id = hsm_objects.get_actual_idev_id()

    export_cert = CertHandler(
        pin=config.hsm_pin,
        cert_id=hsm_idev_id,
    )
    export_cert.export_certificate(output_directory="/home/admin/")
    actual_idev = export_cert.parse_certificate()

if __name__ == "__main__":
    main()