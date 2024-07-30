import hashlib


class Chat:
    def __init__(self, chat_code):
        self.chat_code = chat_code
        self.chat_id = 0
        self.chat_users = []

    def check_code(self, confirm_code):
        return self.chat_code == confirm_code

    def hash_code(self):
        self.chat_code = hashlib.sha256(self.chat_code.encode()).hexdigest()
