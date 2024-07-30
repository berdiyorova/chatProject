import hashlib


class User:
    def __init__(self, full_name, username, password):
        self.full_name = full_name
        self.username = username
        self.password = password
        self.is_login = False

    def check_password(self, confirm_password):
        return self.password == confirm_password

    def hash_password(self):
        self.password = hashlib.sha256(self.password.encode()).hexdigest()
