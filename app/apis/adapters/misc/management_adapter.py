import pyhsm

class HSMKeyManager:
    def __init__(self, key_partition, key_password):
        self.key_partition = key_partition
        self.key_password = key_password

    def enable_key(self, key_index):
        with pyhsm.HSMClient(partition_password=self.key_password, partition_id=self.key_partition) as hsm:
            key = hsm.get_key_by_index(key_index)
            key.enabled = True
            hsm.put_key(key)

    def disable_key(self, key_index):
        with pyhsm.HSMClient(partition_password=self.key_password, partition_id=self.key_partition) as hsm:
            key = hsm.get_key_by_index(key_index)
            key.enabled = False
            hsm.put_key(key)

class HSMSigner:
    def __init__(self, key_partition, key_password):
        self.key_partition = key_partition
        self.key_password = key_password

    def sign_data(self, key_index, data_to_sign):
        with pyhsm.HSMClient(partition_password=self.key_password, partition_id=self.key_partition) as hsm:
            private_key = hsm.get_key_by_index(key_index)
            signature = private_key.sign(data_to_sign)
            return signature