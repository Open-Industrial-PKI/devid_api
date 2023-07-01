import json
import datetime
import os
from app.apis.adapters import logger


class IDManager:
    def __init__(self, file_path):
        self.logger = logger.get_logger("IDManager")
        self.file_path = file_path
        self.check_json_file()

        with open(self.file_path, 'r') as file:
            self.ids = json.load(file)

    def check_json_file(self):
        self.logger.info("--Check JSON file")
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file)

    def add_id(self, id_value):
        self.logger.info("--Adding ID: id_value: <{}>".format(str(id_value)))
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.ids.append({'id': id_value, 'timestamp': timestamp})

        with open(self.file_path, 'w') as file:
            json.dump(self.ids, file)

    def get_latest_id(self):
        self.logger.info("--Get latest ID")
        if len(self.ids) == 0:
            return None
        else:
            return max(self.ids, key=lambda x: x['timestamp'])['id']

if __name__ == "__main__":
    id = IDManager(file_path="/home/admin/certs/ids.json")
    id.add_id(id_value="10542d997f0000001000000000000000")
    most_recent = id.get_latest_id()
    print(most_recent)