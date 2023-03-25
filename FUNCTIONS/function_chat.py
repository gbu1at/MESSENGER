from SETTING import CHAT_JSON
from FUNCTIONS.functions import *


def find_chat(HASH_CHAT):
    if HASH_CHAT == "null":
        return True
    data = open_json(CHAT_JSON)
    id, password = rehash_chat_id_password(HASH_CHAT)
    return (id in data) and (password == data[id]["password"])


def get_chat(HASH):
    if HASH == "null":
        return None
    data = open_json(CHAT_JSON)
    id, password = rehash_chat_id_password(HASH)
    return data[id]


def add_message_in_chat(HASH_CHAT, message, HASH_USER):
    login_user, _ = rehash_login_password(HASH_USER)
    id_chat, _ = rehash_chat_id_password(HASH_CHAT)
    text = f"[{login_user}]: " + message
    data = open_json(CHAT_JSON)
    data[id_chat]["MESSAGES"].append(text)
    write_json(CHAT_JSON, data)


def create_new_chat(password):
    data = open_json(CHAT_JSON)
    chat_id = len(data)
    data[chat_id] = {
        "ID": chat_id,
        "password": password,
        "MESSAGES": [],
        "USERS": []
    }
    write_json(CHAT_JSON, data)
    return get_chat_hash(chat_id, password)


def get_chat_hash(chat_id, password):
    return str(chat_id) + "&&" + password
