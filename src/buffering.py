import threading
import config
import json
import time
import db_functions as database

time_sleep = 10
isCleanBuffer = True

class UserBuffer:
    def __init__(self, chat_id):
        self.id = chat_id
        self.name = str()
        self.question = QuestionBuffer()
        self.status = ''
        self.keyboard = ''
        self.variables = {}
        self.is_admin = 0
        self.company = 0
        self.departament = 0
        self.email = str()

    def from_json(self, json):
        self.id             = int(json["id"])
        self.name           = str(json["name"])
        self.status         = str(json["status"])
        self.keyboard       = str(json["keyboard"])
        self.is_admin       = int(json["is_admin"])
        self.company        = int(json["company"])
        self.departament    = int(json["departament"])
        self.email          = str(json["email"])

    def to_json(self):
        result = {
                "id":          f"{self.id}",
                "name":        f"{self.name}",
                "status":      f"{self.status}",
                "keyboard":    f"{self.keyboard}",
                "is_admin":    f"{self.is_admin}",
                "company":     f"{self.company}",
                "departament": f"{self.departament}",
                "email":       f"{self.email}"
            }
        return result


class QuestionBuffer:
    def __init__(self):
        self.id = 0
        self.thema = -1
        self.description = ''
        self.files = []

class FileBuffer:
    def __init__(self):
        self.file_id = 0
        self.contentType = 0
        self.date = 0


def user_exists(tg_id):
    users = database.db_execute_fetch(f"SELECT tg_id FROM Users WHERE tg_id='{tg_id}'")
    if users == None:
        return False
    for user in users:
        if str(user[0]) == str(tg_id):
            return True
    return False

def get_buffer():
    users = []
    buf_user = None
    with open(config.buffer_local_path, 'r') as json_file:
        if len(json_file.read()) != 0:
            isCleanBuffer = False
        else:
            return
    with open(config.buffer_local_path, 'r') as json_file:
        users = json.load(json_file)
    
    for user in users["users"]:
        chat_id = int(user["id"])
        config.buffer[chat_id] = UserBuffer(chat_id)
        config.buffer[chat_id].from_json(user)
    

def start():
    try:
        threading.Thread(target=run).start()
    except Exception as e:
        print(f"buffering.start: {repr(e)}")

def run():
    try:
        keys = None
        while True:
            time.sleep(time_sleep)
            keys = config.buffer.keys()
            users = []
            if keys == None:
                continue
            for key in keys:
                exist = user_exists(str(key))
                if exist == True:
                    user = config.buffer[key].to_json()
                    users.append(user)

            with open(config.buffer_local_path, 'w') as json_file:
                json.dump({"users":users}, json_file, indent=4)
    except Exception as e:
        print(f"buffering.start: {repr(e)}")

