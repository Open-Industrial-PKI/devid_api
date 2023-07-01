from cert_handler import CertHandler
from hsm_objects import HsmObjects
from app.apis.adapters.__config__ import Configuration

config = Configuration()

def main():
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    most_recent = hsm_objects.get_most_recent_ldev_id()

    export_cert = CertHandler(
        pin=config.hsm_pin,
        cert_id=most_recent,
    )
    export_cert.export_certificate(output_directory="/home/admin/")
    actual_idev = export_cert.parse_certificate()
    print(actual_idev)

if __name__ == "__main__":
    main()

