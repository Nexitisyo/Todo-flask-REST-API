import json
import os
import datetime


class database(object):
    def __init__(self, path):
        self.path = os.path.join(path)
        self.initJSON()

    def initJSON(self):
        file = os.path.join(self.path, "entries.json")
        structure = []
        if not os.path.isfile(file):
            structure.append({
                "id": 0,
                "description": "",
                "due_date": "",
                "done": False,
                "priority": 0
            })
            self.write_file('entries', structure)

    def write_file(self, filename, data):
        with open(os.path.join(self.path, filename + ".json"), "w") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    def read_file(self, filename):
        with open(os.path.join(self.path, filename + '.json'), "r") as f:
            data = json.load(f)
        return data
