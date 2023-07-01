import json
import re
import subprocess
from app.apis.adapters.__config__ import Configuration

config = Configuration()

class P11ToolParser:
    def __init__(self, pin):
        self.pin = pin
        self.output = None
        self.keys = None

    def get_keys(self):
        cmd = ['p11tool', '--provider=/usr/lib/opensc-pkcs11.so', '--list-keys', '--login', '--set-pin={}'.format(self.pin)]
        self.output = subprocess.check_output(cmd, universal_newlines=True)
        return self.keys_to_json()

    def parse_keys(self):
        pattern = r"Object (\d+):\n\s+URL: (.+)\n\s+Type: (.+)\n\s+Label: (.+)\n\s+Flags: (.+)\n\s+ID: (.+)"
        objects = []
        for match in re.finditer(pattern, self.output):
            obj = {
                "index": match.group(1),
                "url": match.group(2),
                "type": match.group(3),
                "label": match.group(4),
                "flags": match.group(5),
                "id": match.group(6),
            }
            objects.append(obj)
        return objects

    def keys_to_json(self):
        objects = self.parse_keys()
        return json.dumps(objects, indent=4)

    def get_url_by_label(self, label):
        keys = self.keys_to_json()
        keys_trans = json.loads(keys)
        for key in keys_trans:
            if key["label"] == label:
                return key["url"]
        return None

def main():
    p11_keys = P11ToolParser(pin=config.hsm_pin)
    p11_keys.get_keys()
    url = p11_keys.get_url_by_label("ldev_pvt_key_3443")
    print(url)

if __name__ == "__main__":
    main()
