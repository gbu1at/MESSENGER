import json


def open_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def write_json(json_path, data):
    with open(json_path, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False))


def rehash_chat_id_password(HASH_CHAT):
    return HASH_CHAT.split("&&")


def rehash_login_password(HASH_USER):
    return HASH_USER.split("&&")
