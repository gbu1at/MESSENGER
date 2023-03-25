from datetime import date
import os

from flask import Flask, render_template, redirect, request
from FUNCTIONS.functions_user import *
from FUNCTIONS.function_chat import *
from FUNCTIONS.function_blog import *
from CLASS.USER_INFO import USER_INFO

app = Flask(__name__)


def check_autorization(app_func):
    def decorator(*args, **kwargs):
        HASH = kwargs["HASH_USER"]
        if not check_login_password_hash(HASH):
            return redirect("/autorization")
        return app_func(*args, **kwargs)

    return decorator


def check_chat(app_func):
    def decorator(*args, **kwargs):
        HASH_CHAT = kwargs["HASH_CHAT"]
        if not find_chat(HASH_CHAT):
            return "чат не найден!!!"
        return app_func(*args, **kwargs)

    return decorator


@app.route("/")
def start():
    return render_template("HTML/start.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        new_login = request.form.get("login")
        password = request.form.get("password")
        new_user = USER_INFO(new_login, password, {})
        if find_login_in_base(new_login):
            return render_template("HTML/registration.html", flag_login=True, flag_password=False,
                                   text_error_login="пользователь с таким логином уже есть")
        if not is_corrcet_login(new_login):
            return render_template("HTML/registration.html", flag_login=True, flag_password=False,
                                   text_error_login="некорректный логин. Логин не может содержать символы: & ^ % # *")
        if not is_corrcet_password(password):
            return render_template("HTML/registration.html", flag_login=False, flag_password=True,
                                   text_error_password="некорректный пароль. Пароль должен содержать хотя бы 8 символов")
        add_user_in_base(new_user)
        return redirect(f"/home/{new_login}&&{password}")

    else:
        return render_template("HTML/registration.html", flag_login=False, flag_password=False)


@app.route("/autorization", methods=["GET", "POST"])
def autorization():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        HASH = get_login_password_hash(login, password)
        if check_login_password_hash(HASH):
            return redirect(f"/home/{HASH}")
        else:
            return render_template("HTML/autorization.html", flag=True)
    else:
        return render_template("HTML/autorization.html", flag=False)


@app.route("/home/<HASH_USER>", endpoint="home_user_page", methods=["GET", "POST"])
@check_autorization
def home_user_page(HASH_USER):
    login, _ = rehash_login_password(HASH_USER)
    return redirect(f"/home/{HASH_USER}/watching_page/{login}")


@app.route("/home/<HASH_USER>/watching_page/<other_login_user>", methods=["GET", "POST"])
@check_autorization
def watching_other_user_page(HASH_USER, other_login_user):
    user = get_user_(HASH_USER)
    other_user = get_user(other_login_user)
    is_friend = is_friend_user(user, other_user)
    is_root = (user == other_user)
    if request.method == "POST":
        file = request.files['photo']
        if file.filename == '':
            return redirect(request.url)
        photo_update(file, HASH_USER)
        return redirect(f"/home/{HASH_USER}")
    return render_template("HTML/information_user_page.html", root_user=user, other_user=other_user, is_root=is_root,
                           is_friend=is_friend)


@app.route("/home/<HASH_USER>/watching_blogs/<other_login>", methods=['POST', 'GET'], endpoint="watching_blogs_page")
@check_autorization
def watching_blogs_page(HASH_USER, other_login):
    login, _ = rehash_login_password(HASH_USER)
    user = get_user(login)
    other_user = get_user(other_login)
    is_root = (login == other_login)

    if request.method == "POST":
        blog = request.form
        t = str(date.today())
        title = blog.get('title')
        topic = blog.get('topic')
        text = blog.get('text')
        add_blog(HASH_USER, t, title, topic, text)
        return redirect(f'/home/{HASH_USER}/watching_blogs/{other_login}')
    other_user["BLOG"]["BLOGS"] = {k: v for k, v in reversed(other_user["BLOG"]["BLOGS"].items())}
    return render_template("HTML/blog.html", root_user=user, other_user=other_user, is_root=is_root)


@app.route("/home/<HASH_USER>/delete_blog/<blog_ID>", methods=['POST', 'GET'], endpoint="delete_blog")
@check_autorization
def delete_blog(HASH_USER, blog_ID):
    login, _ = rehash_login_password(HASH_USER)
    if find_blog(login, blog_ID):
        del_blog(login, blog_ID)
    return redirect(f"/home/{HASH_USER}/watching_blogs/{login}")


@app.route("/home/<HASH_USER>/find_user", methods=["GET", "POST"], endpoint="find_user_page")
@check_autorization
def find_user_page(HASH_USER):
    flag = False
    user = get_user_(HASH_USER)
    if request.method == "POST":
        search_login = request.form.get("search_login")
        if find_login_in_base(search_login):
            return redirect(f"/home/{HASH_USER}/watching_page/{search_login}")
        flag = True
    return render_template("HTML/find_user.html", flag=flag, root_user=user)


@app.route("/home/<HASH_USER>/create_chat", methods=['POST', 'GET'], endpoint='addChat')
@check_autorization
def addChat(HASH_USER):
    user = get_user_(HASH_USER)
    if request.method == 'POST':
        password = request.form.get("password")
        hash_chat = create_new_chat(password)
        add_chat_in_user(HASH_USER, hash_chat)
        return redirect(f"/home/{HASH_USER}/list_chats/{hash_chat}")
    return render_template("HTML/create_chat.html", root_user=user)


@app.route("/home/<HASH_USER>/find_chat", methods=['GET', 'POST'], endpoint="findChat")
@check_autorization
def findChat(HASH_USER):
    user = get_user_(HASH_USER)
    if request.method == "POST":
        chat_id = request.form.get("chat ID")
        password = request.form.get("password")
        hash_chat = get_chat_hash(chat_id, password)
        if find_chat(hash_chat):
            add_chat_in_user(HASH_USER, hash_chat)
            return redirect(f"/home/{HASH_USER}/list_chats/{hash_chat}")
        else:
            render_template("HTML/find_chat.html", flag=True, root_user=user)
    return render_template("HTML/find_chat.html", flag=False, root_user=user)


@app.route("/home/<HASH_USER>/list_chats/<HASH_CHAT>", methods=["GET", "POST"], endpoint='chat')
@check_autorization
@check_chat
def chat(HASH_USER, HASH_CHAT):
    user = get_user_(HASH_USER)
    if request.method == "POST":
        message = request.form.get("message")
        add_message_in_chat(HASH_CHAT, message, HASH_USER)
        return redirect(f"/home/{HASH_USER}/list_chats/{HASH_CHAT}")
    CHAT = get_chat(HASH_CHAT)
    return render_template("HTML/chat.html", CHAT=CHAT, root_user=user, null_chat=(CHAT is None))


# @app.route("/home/<HASH_USER>/list_chats/<HASH_CHAT>", endpoint="list_chat")
# @check_autorization
# def list_chat(HASH_USER, HASH_CHAT):
#     user = get_user_(HASH_USER)
#     return render_template("HTML/list_chat.html", root_user=user, CHAT=HASH_CHAT)


@app.route("/home/<HASH_USER>/add_friend/<other_login>", endpoint="add_friend")
@check_autorization
def add_friend(HASH_USER, other_login):
    add_friend_user(HASH_USER, other_login)
    return redirect(f"/home/{HASH_USER}/watching_page/{other_login}")


@app.route("/home/<HASH_USER>/watching_photos/<other_login>", endpoint="watching_photos_user")
@check_autorization
def watching_photos_user(HASH_USER, other_login):
    user = get_user_(HASH_USER)
    other_user = get_user(other_login)
    is_root = (user == other_user)
    return render_template("HTML/photo_user.html", root_user=user, other_user=other_user, is_root=is_root)


@app.route("/home/<HASH_USER>/watching_blog/<other_login>/<blog_id>", endpoint="watching_blog")
@check_autorization
def watching_blog(HASH_USER, other_login, blog_id):
    user = get_user_(HASH_USER)
    other_user = get_user(other_login)
    is_root = (user == other_user)
    blog = get_blog(other_user, blog_id)
    return render_template("HTML/watching_blog.html", root_user=user, other_user=other_user, blog=blog, blog_id=blog_id,
                           is_root=is_root)


@app.route("/home/<HASH_USER>/del_photo/<id_photo>", endpoint="delete_photo")
@check_autorization
def delete_photo(HASH_USER, id_photo):
    login, _ = rehash_login_password(HASH_USER)
    del_photo(HASH_USER, id_photo)
    return redirect(f"/home/{HASH_USER}/watching_photos/{login}")


@app.route("/home/<HASH_USER>/create_root_photo/<id_new_photo>", endpoint="create_root_photo")
@check_autorization
def create_root_photo(HASH_USER, id_new_photo):
    swap_photo(HASH_USER, id_new_photo, "root_photo")
    return redirect(f"/home/{HASH_USER}")


# @app.route("home/<HASH_USER>/redactor_blog/<blog.id>", endpoint="redactor_blog")
# @check_autorization
# def redactor_blog(HASH_USER, blog_id):
#     text = get_blog(get_user_(HASH_USER), blog_id).text
#

if __name__ == "__main__":
    app.run(debug=True)
