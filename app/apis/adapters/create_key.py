from pyhsm.hsmclient import HsmClient
import random
from app.apis.adapters import logger
from app.apis.adapters.__config__ import Configuration

config = Configuration()


class HsmKey:
    def __init__(self, slot, pin, public_key_label, private_key_label, key_length=2048, library_path = '/usr/lib/opensc-pkcs11.so',
                 public_exponent=b"\x01\x00\x01", token=True, modifiable=False, extractable=False, sign_verify=True,
                 encrypt_decrypt=True, wrap_unwrap=True, derive=False):

        self.logger = logger.get_logger("HsmKey")

        self.slot = slot
        self.pin = pin
        self.pkcs11_lib = library_path
        self.public_key_label = public_key_label
        self.private_key_label = private_key_label
        self.key_length = key_length
        self.public_exponent = public_exponent
        self.token = token
        self.modifiable = modifiable
        self.extractable = extractable
        self.sign_verify = sign_verify
        self.encrypt_decrypt = encrypt_decrypt
        self.wrap_unwrap = wrap_unwrap
        self.derive = derive

    def generate_rsa_key_pair(self):
        self.logger.info("-Generate RSA keypair")
        self.logger.info("--Private Key label: {}".format(self.private_key_label))
        self.logger.info("--Public Key label: {}".format(self.public_key_label))

        with HsmClient(slot=self.slot, pin=self.pin, pkcs11_lib=self.pkcs11_lib) as c:
            key_handles = c.create_rsa_key_pair(public_key_label=self.public_key_label,
                                                private_key_label=self.private_key_label,
                                                key_length=self.key_length,
                                                public_exponent=self.public_exponent,
                                                token=self.token,
                                                modifiable=self.modifiable,
                                                extractable=self.extractable,
                                                sign_verify=self.sign_verify,
                                                encrypt_decrypt=self.encrypt_decrypt,
                                                wrap_unwrap=self.wrap_unwrap,
                                                derive=self.derive)
            return key_handles


def generate_ldev_key():
    random_id = random.randint(1000, 9999)
    hsm_key = HsmKey(slot=0,
                     pin=config.hsm_pin,
                     public_key_label="ldev_pub_key_{}".format(random_id),
                     private_key_label="ldev_pvt_key_{}".format(random_id))
    hsm_key.generate_rsa_key_pair()

def generate_idev_key():
    random_id = random.randint(1000, 9999)
    hsm_key = HsmKey(slot=0,
                     pin=config.hsm_pin,
                     public_key_label="idev_pub_key_{}".format(random_id),
                     private_key_label="idev_pvt_key_{}".format(random_id))
    hsm_key.generate_rsa_key_pair()

if __name__ == "__main__":
    generate_idev_key()
    generate_ldev_key()

