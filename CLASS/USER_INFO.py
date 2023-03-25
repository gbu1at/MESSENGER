from FUNCTIONS.functions_user import get_login_password_hash


class USER_INFO:
    def __init__(self, login, password, preview):
        self.login = login
        self.password = password
        self.preview = preview
        self.HASH = get_login_password_hash(login, password)
