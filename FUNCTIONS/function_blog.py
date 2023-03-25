from SETTING import *
from FUNCTIONS.functions import *


def add_blog_(HASH_USER, new_post):
    login, _ = rehash_login_password(HASH_USER)
    data = open_json(USERS_JSON)
    new_ID = data[login]["BLOG"]["next_id"]
    data[login]["BLOG"]["next_id"] += 1
    data[login]["BLOG"]["BLOGS"][new_ID] = new_post
    write_json(USERS_JSON, data)


def find_blog(login, blog_ID):
    data = open_json(USERS_JSON)
    return blog_ID in data[login]["BLOG"]["BLOGS"]


def del_blog(login, blog_ID):
    data = open_json(USERS_JSON)
    data[login]["BLOG"]["BLOGS"].pop(blog_ID)
    write_json(USERS_JSON, data)


def add_blog(HASH_USER, date, title, topic, text):
    new_post = formating_data_blog__(*formating_data_blog_(date, title, topic, text))
    add_blog_(HASH_USER, new_post)


def formating_data_blog_(date, title, topic, text):
    return {
        "date": date,
        "title": title,
        "topic": topic
    }, text


def formating_data_blog__(information, text):
    return {"information": information, "text": text.split('\n')}


def get_blog(user, blog_id):
    if blog_id in user["BLOG"]["BLOGS"]:
        return user["BLOG"]["BLOGS"][blog_id]
    return None
