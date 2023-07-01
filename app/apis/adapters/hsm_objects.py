import re
import json
import subprocess
import os
from app.apis.adapters import logger
from app.apis.adapters.id_manager import IDManager
from app.apis.adapters.__config__ import Configuration

config = Configuration()


class HsmObjects:
    def __init__(self, slot_num, pin):
        self.logger = logger.get_logger("HsmObjects")
        self.slot_num = slot_num
        self.pin = pin
        objects = self.list_objects_on_hsm()
        self.parsed_objects = None
        self.parse_input_str(objects)

    def list_objects_on_hsm(self):
        self.logger.info("-List objects on HSM")
        # Run the bash script and capture the output
        result = subprocess.check_output(
            ["/home/admin/devid_api/app/apis/adapters/bash/list_objects.sh", str(self.slot_num), self.pin])
        result_str = result.decode('utf-8')  # decode bytes object to string
        return result_str

    def parse_input_str(self, input_str):

        self.parsed_objects = {
            "private_keys": {},
            "public_keys": {},
            "certificates": {}
        }

        current_key_type = None
        current_key_label = None

        for line in input_str.split("\n"):
            line = line.strip()
            if line.startswith("Private Key Object"):
                current_key_type = "private_keys"
            elif line.startswith("Public Key Object"):
                current_key_type = "public_keys"
            elif line.startswith("Certificate Object"):
                current_key_type = "certificates"
            elif line.startswith("label:"):
                current_key_label = line.split(":")[1].strip()
                self.parsed_objects[current_key_type][current_key_label] = {}
            elif line.startswith("ID:"):
                self.parsed_objects[current_key_type][current_key_label]["ID"] = line.split(":")[1].strip()
            elif line.startswith("Usage:"):
                self.parsed_objects[current_key_type][current_key_label]["Usage"] = line.split(":")[1].strip()
            elif line.startswith("Access:"):
                self.parsed_objects[current_key_type][current_key_label]["Access"] = line.split(":")[1].strip()
            elif line.startswith("subject:"):
                self.parsed_objects[current_key_type][current_key_label]["subject"] = "{}: {}".format(
                    line.split(":")[1].strip(), line.split(":")[2].strip())

    def to_dict(self):
        return self.parsed_objects

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def count_keys(self, private=True, public=True):
        self.logger.info("--Counting Keys; Private {}; Public: {}".format(str(private), str(public)))
        keycounter = 0
        if private:
            keycounter += len(self.to_dict()['private_keys'])
        if public:
            keycounter += len(self.to_dict()['public_keys'])

        return keycounter

    def count_idev_keys(self):
        return self.count_objects_by_type("idev", certs=False)

    def count_ldev_keys(self):
        return self.count_objects_by_type("ldev", certs=False)

    def count_idev_certs(self):
        return self.count_objects_by_type("idev", keys=False)

    def count_ldev_certs(self):
        return self.count_objects_by_type("ldev", keys=False)

    def count_objects_by_type(self, type="idev", keys=True, certs=True):
        self.logger.info("--Counting Objects by Type: Type: <{}>; Keys: <{}>; Certs: <{}>".format(type, str(keys), str(certs)))
        count = 0

        if keys:
            for key in self.to_dict()['private_keys']:
                if key.startswith(type):
                    count += 1
            for key in self.to_dict()['public_keys']:
                if key.startswith(type):
                    count += 1
        elif certs:
            for key in self.to_dict()['certificates']:
                if key.startswith(type):
                    count += 1

        return count

    def count_certificates(self):
        certificates_count = len(self.to_dict()['certificates'])
        return certificates_count

    def filter_id_by_label(self, key_label):
        self.logger.info("--Filter ID by Label: key_label: <{}>".format(str(key_label)))
        keys = self.to_json()
        keys_str = json.loads(keys)
        for key_type in ["private_keys", "public_keys"]:
            if key_label in keys_str[key_type]:
                return keys_str[key_type][key_label]["ID"]

    def get_actual_idev_id(self):
        self.logger.info("--Search actual IDevID")
        data = self.to_dict()

        for key, value in data['private_keys'].items():
            if key.startswith('idev'):
                self.logger.info("--IDevID found with ID: {}".format(value['ID']))
                return value['ID']
        self.logger.info("--No IDevID found")
        return None

    def get_most_recent_ldev_id(self):
        self.logger.info("-Search most recent LDevID")

        id = IDManager(file_path="/home/admin/certs/ldev_ids.json")
        most_recent = id.get_latest_id()
        if self.validate_id_exists(most_recent):
            self.logger.info("--LDevID found with ID: {}".format(most_recent))
            return most_recent
        self.logger.info("--No LDevID found")
        return None

    def validate_id_exists(self, id):
        keys = self.to_dict()
        for key_type in keys:
            for key_name in keys[key_type]:
                key_data = keys[key_type][key_name]
                if key_data['ID'] == id:
                    return True
        return False

    def delete_all_objects(self):
        self.logger.info("--Delete all objects")
        keys = self.to_dict()
        deleted_keys = self.delete_objects(keys)
        return deleted_keys

    def delete_ldev_objects(self):
        self.logger.info("--Delete LDev objects")
        deleted_keys = self.delete_objects_by_type("ldev")
        return deleted_keys


    def delete_idev_objects(self):
        self.logger.info("--Delete IDev objects")
        deleted_keys = self.delete_objects_by_type("idev")
        return deleted_keys


    def delete_objects_by_type_legacy(self, type):
        keys = self.to_dict()
        filtered_dict = {k1: {k2: v2 for k2, v2 in v1.items() if k2.startswith(type)} for k1, v1 in keys.items()}
        deleted_keys = self.delete_objects(filtered_dict)
        return deleted_keys

    def delete_objects_by_type(self, type, delete_num=None):
        self.logger.info("--Delete objects by type: type: <{}>; Delte specific number of objects: <{}>".format(type, str(delete_num)))
        keys = self.to_dict()
        filtered_dict = {}

        if delete_num is not None:
            # Delete <delete_num> private keys, public keys and certificates
            private_key_counter = 0
            public_key_counter = 0
            certificate_counter = 0

            for k1, v1 in keys.items():
                filtered_dict[k1] = {}
                for k2, v2 in v1.items():
                    if k2.startswith(type):
                        if 'private_keys' in k1 and private_key_counter < delete_num:
                            filtered_dict[k1][k2] = v2
                            private_key_counter += 1
                        elif 'public_keys' in k1 and public_key_counter < delete_num:
                            filtered_dict[k1][k2] = v2
                            public_key_counter += 1
                        elif 'certificates' in k1 and certificate_counter < delete_num:
                            filtered_dict[k1][k2] = v2
                            certificate_counter += 1
        else:
            filtered_dict = {k1: {k2: v2 for k2, v2 in v1.items() if k2.startswith(type)} for k1, v1 in keys.items()}

        deleted_keys = self.delete_objects(filtered_dict)
        return deleted_keys



    def delete_objects(self, keys):
        counter = 0
        for key_type in keys:
            type = "privkey" if key_type == "private_keys" else "pubkey" if key_type == "public_keys" else "cert"
            for key_name in keys[key_type]:
                counter += 1
                key_data = keys[key_type][key_name]
                self.delete_hsm_object(type, key_data['ID'])
        return counter

    def delete_key_by_label(self, key_label):
        self.filter_id_by_label(key_label)

    def delete_hsm_object(self, type, key_id):
        command = [
            "/home/admin/devid_api/app/apis/adapters/bash/delete_keys_on_hsm.sh",
            f'--key_type={type}',
            f'--id={key_id}',
            f'--pin={self.pin}',

        ]

        self.logger.info("Executing command:", " ".join(command))
        subprocess.call(command)


def main():
    print("--- Print Objects ---")
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    print(hsm_objects.to_dict())
    print(hsm_objects.to_json())
    # print(hsm_objects.to_dict())
    print("--- Get key ID ---")
    print("ID: {}".format(hsm_objects.filter_id_by_label(key_label="my_rsa_pvt_86599")))


def most_recent_ldev():
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    most_recent = hsm_objects.get_most_recent_ldev_id()
    print(most_recent)


def delete_idev():
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    hsm_objects.delete_idev_objects()


def get_actual_idev():
    hsm_objects = HsmObjects(
        slot_num=0,
        pin=config.hsm_pin
    )
    print(hsm_objects.get_actual_idev_id())


if __name__ == "__main__":
    main()
