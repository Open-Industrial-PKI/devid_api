import random
from app.apis.adapters.create_key import HsmKey
from app.apis.adapters.generate_csr import GenerateCsr
from app.apis.adapters.request_cert import CertRequest
from app.apis.adapters.cert_handler import CertHandler
from app.apis.adapters.validate_chain import CertValidator
from app.apis.adapters.hsm_objects import HsmObjects
from app.apis.adapters.id_manager import IDManager
import os
from app.apis.adapters import logger
from app.apis.adapters.__config__ import Configuration

config = Configuration()

class BootstrapDevId:
    def __init__(self, pin, slot):

        self.logger = logger.get_logger("BootstrapDevID")
        self.pin = pin
        self.slot = slot
        self.key_generated = False
        self.csr_generated = False
        self.cert_path = None
        self.valid_idev = None
        self.idev = False
        self.ldev = False
        self.hsm_id = None
        self.serial_number = None
        self.id = random.randint(10000, 99999)
        self.hsm_objects = None

    def setup_idev_id(self):
        self.logger.info("--Setup IDevID")

        self.idev = True
        self.private_key_label="idev_pvt_key_{}".format(self.id)
        self.public_key_label="idev_pub_key_{}".format(self.id)
        self.cert_path='/home/admin/certs/id_{}/idev_cert_{}.cert.pem'.format(self.id, self.id)
        self.cn="idev_cn_{}".format(self.id)
        self.serial_number=self.id

        self.presetup()
        self.validate_single_idev()

    def setup_ldev_id(self):
        self.logger.info("--Setup LDevID")
        self.private_key_label = "ldev_pvt_key_{}".format(self.id)
        self.public_key_label = "ldev_pub_key_{}".format(self.id)
        self.cert_path='/home/admin/certs/id_{}/ldev_cert_{}.cert.pem'.format(self.id, self.id)
        self.cn="ldev_cn_{}".format(self.id)

        self.presetup()


    def presetup(self):
        self.logger.info("--Presetup")
        self.validate_key_label_exists()

        self.create_directory("/home/admin/certs")
        self.create_directory("/home/admin/certs/id_{}".format(self.id))

    def validate_single_idev(self):
        self.logger.info("--Validate if a IDevID exists")

        idev = self.hsm_objects.get_actual_idev_id()
        if idev is not None:
            self.logger.error("❌ IDevID already exists")
            raise Exception("IDevID already exists. There can only be one IDevID on the device")

    def create_directory(self, directory_path):

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            self.logger.info(f"Created directory at {directory_path}")

    def create_key(self):
        self.logger.info("🔑 Create keypair")
        hsm_key = HsmKey(slot=self.slot,
                         pin=self.pin,
                         public_key_label=self.public_key_label,
                         private_key_label=self.private_key_label)
        hsm_key.generate_rsa_key_pair()
        self.hsm_objects = HsmObjects(
            slot_num=self.slot,
            pin=self.pin
        )
        self.hsm_id = self.hsm_objects.filter_id_by_label(key_label=self.private_key_label)
        log_id = IDManager("/home/admin/certs/ldev_ids.json")
        log_id.add_id(self.hsm_id)
        self.key_generated = True

    def generate_csr(self, key_label=None, cn=None, o=None, ou=None, c=None, serial_number=None, pseudonym=None):
        self.logger.info("🖋️ Generate CSR")

        if self.key_generated:
            pre_label = "idev" if self.idev else "ldev"
            key_label = "{}_pvt_key_{}".format(pre_label, self.id)
        else:
            if key_label is None:
                raise Exception("key_label needs to be defined if there was no prior key generation")

        csr_generate = GenerateCsr(
            slot_num=self.slot,
            pin=self.pin,
            key_label=key_label,
            output_file='/home/admin/certs/id_{}/csr_{}.csr'.format(self.id, self.id)
        )
        if cn:
            self.cn=cn
        if serial_number:
            self.serial_number=serial_number

        csr_generate.generate_csr(cn=self.cn,
                                  serial_number=self.serial_number,
                                  o=o,
                                  ou=ou,
                                  c=c,
                                  pseudonym=pseudonym)

    def request_cert(self, base_url, p12_file, p12_pass, certificate_profile_name, end_entity_profile_name, certificate_authority_name,
                     token_user, token_pw, ca_certificate=False):
        self.logger.info("📄 Request certificate")

        cert_req = CertRequest(
            base_url=base_url,
            p12_file=p12_file,
            p12_pass=p12_pass,
            csr_file='/home/admin/certs/id_{}/csr_{}.csr'.format(self.id, self.id),
        )

        cert_req.request_certificate(cert_file=self.cert_path,
                                     certificate_profile_name=certificate_profile_name,
                                     end_entity_profile_name=end_entity_profile_name,
                                     certificate_authority_name=certificate_authority_name,
                                     token_user=token_user,
                                     token_pw=token_pw,
                                     ca_certificate=ca_certificate)

    def import_certificate(self):
        self.logger.info("⬆️ Import certificate")

        insert_cert = CertHandler(
            pin=self.pin,
            cert_id=self.hsm_id,
        )
        insert_cert.insert_certificate(slot=self.slot,
                                       cert_label=self.cn,
                                       certificate_path=self.cert_path)

    def export_certificate(self):
        self.logger.info("--Export certificate with hsm_id: <{}>".format(str(self.hsm_id)))
        export_cert = CertHandler(
            pin=self.pin,
            cert_id=self.hsm_id,
        )
        export_cert.export_certificate(output_directory="/home/admin")

    def validate_idev_certifificate(self, ca_chain_url):
        self.logger.info("？ Validate certificate")

        self.logger.info("-Export IDev Certificate to tmp storage")

        self.hsm_objects = HsmObjects(
            slot_num=self.slot,
            pin=self.pin
        )
        hsm_idev_id = self.hsm_objects.get_actual_idev_id()

        public_web_validator = CertValidator(id=hsm_idev_id)
        public_web_validator._load_ca_certs_via_public_web(ca_chain_url)
        self.valid_idev = public_web_validator.validate()
        return self.valid_idev

    def validate_key_label_exists(self):
        self.hsm_objects = HsmObjects(
            slot_num=self.slot,
            pin=self.pin
        )
        key_label_on_hsm = self.hsm_objects.filter_id_by_label(key_label=self.private_key_label)
        if key_label_on_hsm is not None:
            Exception("key label already exists for key label: {}".format(self.private_key_label))

    def configure_azure(self):
        self.logger.info("🛠️ Work in progress")

    def hsm_key_count(self):
        return self.hsm_objects.count_keys()


def bootstrap_idev():
    idevid = BootstrapDevId(pin=config.hsm_pin, slot=0)
    idevid.setup_idev_id()
    idevid.create_key()
    idevid.generate_csr()
    idevid.request_cert(base_url=config.ejbca_url,
                           p12_file=config.p12_auth_file_path,
                           p12_pass=config.p12_auth_file_pwd,
                           certificate_profile_name=config.certificate_profile_name_idev,
                           end_entity_profile_name=config.end_entity_profile_name_idev,
                           certificate_authority_name=config.certificate_authority_name_idev)
    idevid.import_certificate()

def bootstrap_ldev():
    ldevid = BootstrapDevId(pin=config.hsm_pin, slot=0)
    ldevid.setup_ldev_id()
    ldevid.validate_idev_certifificate(ca_chain_url=config.ca_chain_url_idev)
    ldevid.create_key()
    ldevid.generate_csr()
    ldevid.request_cert(base_url=config.ejbca_url,
                           p12_file=config.p12_auth_file_path,
                           p12_pass=config.p12_auth_file_pwd,
                           certificate_profile_name=config.certificate_profile_name_ldev_basic,
                           end_entity_profile_name=config.end_entity_profile_name_ldev_basic,
                           certificate_authority_name=config.certificate_authority_name_ldev_basic)
    ldevid.import_certificate()
    ldevid.configure_azure()

if __name__ == "__main__":
    bootstrap_ldev()