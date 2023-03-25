import os
import random

from SETTING import USERS_JSON
from FUNCTIONS.functions import *


def find_login_in_base(login):
    data = open_json(USERS_JSON)
    return login in data


def check_login_password_hash(HASH_USER):
    login, password = rehash_login_password(HASH_USER)
    data = open_json(USERS_JSON)
    return (login in data) and (password == data[login]["password"])


def add_user_in_base(new_user):
    data = open_json(USERS_JSON)

    data[new_user.login] = {
        "login": new_user.login,
        "password": new_user.password,
        "HASH": new_user.HASH,
        "id": len(data),
        "preview": new_user.preview,
        "BLOG": {
            "next_id": 0,
            "BLOGS": {}
        },
        "FRIENDS": [],
        "CHATS": {},
        "PHOTOS": {
        }
    }

    write_json(USERS_JSON, data)


def get_login_password_hash(login, password):
    return login + "&&" + password


def is_corrcet_login(login):
    ERROR_CHAR = ["&", "*", "$", "#", " "]
    for char in ERROR_CHAR:
        if char in login:
            return False
    return True


def is_corrcet_password(password):
    if " " in password:
        return False
    return len(password) >= 8


def get_user(login):
    data = open_json(USERS_JSON)
    return data[login]


def get_user_(HASH_USER):
    login, _ = rehash_login_password(HASH_USER)
    return get_user(login)


def add_chat_in_user(HASH_USER, hash_chat):
    data = open_json(USERS_JSON)
    login, _ = rehash_login_password(HASH_USER)
    id_chat, name_chat = rehash_chat_id_password(hash_chat)
    data[login]["CHATS"][hash_chat] = name_chat
    write_json(USERS_JSON, data)


def add_friend_user(HASH_USER, other_login):
    login, _ = rehash_login_password(HASH_USER)
    data = open_json(USERS_JSON)
    if other_login not in data[login]["FRIENDS"]:
        data[login]["FRIENDS"].append(other_login)
    else:
        data[login]["FRIENDS"].remove(other_login)
    write_json(USERS_JSON, data)


def is_friend_user(root_user, other_user):
    login_root = root_user["login"]
    data = open_json(USERS_JSON)
    return other_user['login'] in data[login_root]["FRIENDS"]


def user_add_photo(HASH_USER, id_photo, path):
    login, _ = rehash_login_password(HASH_USER)
    data = open_json(USERS_JSON)
    data[login]["PHOTOS"][id_photo] = path
    write_json(USERS_JSON, data)


def del_photo(HASH_USER, id_photo):
    login, _ = rehash_login_password(HASH_USER)
    data = open_json(USERS_JSON)
    data[login]["PHOTOS"].pop(id_photo)
    if id_photo == "root_photo":
        data[login]["PHOTOS"][id_photo] = None
    write_json(USERS_JSON, data)


def swap_photo(HASH_USER, first_id_photo, second_id_photo):
    login, _ = rehash_login_password(HASH_USER)
    data = open_json(USERS_JSON)
    first = data[login]["PHOTOS"][first_id_photo]
    second = data[login]["PHOTOS"][second_id_photo]

    data[login]["PHOTOS"][first_id_photo] = second
    data[login]["PHOTOS"][second_id_photo] = first

    write_json(USERS_JSON, data)


def random_str():
    s = ""
    for i in range(10):
        s += chr(random.randint(97, 120))
    return s

def photo_update(file, HASH_USER):
    user = get_user_(HASH_USER)
    id_photo = random_str()
    filename = str(id_photo) + '.jpg'
    if len(user["PHOTOS"]) == 0:
        id_photo = "root_photo"
        filename = "root_photo.jpg"
    path = f"static/USER_IMAGES/{user['login']}"
    if user['login'] not in os.listdir('static/USER_IMAGES'):
        os.mkdir(path)
    file.save(os.path.join(path, filename))
    path = "/" + path + '/' + filename
    user_add_photo(HASH_USER, id_photo, path)
