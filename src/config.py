import json
import os

class Config:

    token = ""
    prefix = ""
    prefix_len = 0
    admins = None
    is_docker = True

    def __init__(self):
        fsett = open("config/settings.json")
        data = json.load(fsett)
        self.token = data["token"]
        self.prefix = data["prefix"]
        self.prefix_len = len(self.prefix)
        if "admins" in data:
            self.admins = data["admins"]
        fsett.close()

    def save(self):
        data = {
            "token": self.token,
            "prefix": self.prefix,
            "admin": self.admins,
        }

        json_data = json.dumps(data, indent=2)
        f = open("/app/config/settings.json", "w+")
        f.write(json_data)
        f.close()


    def change_prefix(self, prefix):
        self.prefix = prefix
        self.prefix_len = len(self.prefix)
        self.save()


    def add_admin(self, user_id):
        if not user_id in self.admins:
            self.admins.append(user_id)
            self.save()

    def is_admin(self, user_id):
        return user_id in self.admins
