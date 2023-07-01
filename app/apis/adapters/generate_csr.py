import subprocess
import random
from app.apis.adapters.hsm_objects import HsmObjects
from app.apis.adapters import logger
from app.apis.adapters.__config__ import Configuration

config = Configuration()


class GenerateCsr:
    def __init__(self, slot_num, pin, output_file, key_id=None, key_label=None):
        self.logger = logger.get_logger("GenerateCsr")

        self.key_id = key_id
        self.key_label = key_label
        self.slot_num = slot_num
        self.pin = pin
        self.output_file = output_file

    def get_key_id_by_label(self):
        self.logger.info("-Find key ID to given label {}".format(self.key_label))
        hsm_objects = HsmObjects(
            slot_num=self.slot_num,
            pin=self.pin
        )
        self.key_id = hsm_objects.filter_id_by_label(key_label=self.key_label)
        self.logger.info("--Key ID: {}".format(self.key_id))

    def generate_csr(self, cn, o=None, ou=None, c=None, serial_number=None, pseudonym=None):
        self.logger.info("-Generate CSR ")
        self.logger.info("--File name: {}".format(self.output_file))
        # Build command to call the bash script with named arguments
        command = [
            "/home/admin/devid_api/app/apis/adapters/bash/generate_csr.sh",
            f'--output-file={self.output_file}',
            f'--hsm-pin={self.pin}',
            f'--cn={cn}',
        ]

        if self.key_label:
            self.logger.info("--Find Id for given label: {}".format(self.key_label))
            self.get_key_id_by_label()

        command += [f'--key-id={self.key_id}']

        if o:
            command += [f'--o={o}']
        if ou:
            command += [f'--ou={ou}']
        if c:
            command += [f'--c={c}']
        if serial_number:
            command += [f'--serial-number={serial_number}']
        if pseudonym:
            command += [f'--pseudonym={pseudonym}']

        # Add subject alternative names to the CSR
        # if dns_names or ip_addresses:
        #     san_config = ['[SAN]']
        #     if dns_names:
        #         san_config += ['DNS.{}={}'.format(i + 1, name) for i, name in enumerate(dns_names)]
        #     if ip_addresses:
        #         san_config += ['IP.{}={}'.format(i + 1, ip_address) for i, ip_address in enumerate(ip_addresses)]
        #     san_config_file = output_file + '.san'
        #     with open(san_config_file, 'w') as f:
        #         f.write('\n'.join(san_config))
        #     command += ['-reqexts', 'SAN', '-config', san_config_file]

        self.logger.info(command)
        # Call the bash script with the command
        subprocess.call(command)

if __name__ == "__main__":
    random_id = random.randint(1000, 9999)
    random_cn = random.randint(1000000, 9999999)
    print("--- Generate CSR ---")
    csr_generate = GenerateCsr(
        slot_num=0,
        pin=config.hsm_pin,
        key_id='4',
        output_file='/home/admin/csr_{}.csr'.format(random_id)
    )
    csr_generate.generate_csr(cn="test_cn_{}".format(random_cn),
                              serial_number=random_cn)