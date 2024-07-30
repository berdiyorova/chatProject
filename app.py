import datetime
import hashlib
import os

from fileManager.file_manager import JsonManager
from models.chat import Chat
from models.user import User


"""  USER APP  """

user_manager = JsonManager('fileManager/users.json')

def register():
    full_name = input("Enter full name:  ")
    username = input("Enter username:  ")
    password = input("Enter password:  ")
    confirm_password = input("Confirm password:  ")

    user = User(full_name, username, password)
    if not user.check_password(confirm_password):
        print("Passwords do not match.")
        register()

    user.hash_password()
    user_manager.add_data(user.__dict__)
    return show_auth_menu()

def login():
    username = input("Enter username:  ")
    password = input("Enter password:  ")

    users = user_manager.read()
    index = 0
    while index < len(users):
        if users[index]['username'] == username and users[index]['password'] == hashlib.sha256(password.encode()).hexdigest():
            users[index]['is_login'] = True
            user_manager.write(users)
            return exit_menu(username)
        index += 1
    user_manager.write(users)
    print("Username or password is incorrect. Try again.")
    return show_auth_menu()

def show_auth_menu():
    text = """
        1. Register
        2. Login
        3. Exit
    """
    print(text)

    user_input = input("Enter your choice:  ")
    if user_input == '1':
        register()
    elif user_input == '2':
        login()
    elif user_input == '3':
        return






""" CHAT APP """

chat_manager = JsonManager('fileManager/chat.json')

def create(username):
    chat_code = input("Enter chat code:  ")
    confirm_code = input("Confirm your code:  ")

    chat = Chat(chat_code)

    if not chat.check_code(confirm_code):
        print("Codes do not match.")
        create(username)

    chats = chat_manager.read()
    chat.chat_id = len(chats) + 1
    chat.hash_code()
    chat.chat_users.append(username)

    chat_manager.add_data(chat.__dict__)
    print("Chat created.")
    return _50gram(username)

def join(username):
    chat_id = int(input("Enter chat id:  "))

    chats = chat_manager.read()
    if chat_id > len(chats):
        print("Chat not found.")
        return exit_menu(username)

    chat_code = input("Enter chat code:  ")
    for chat in chats:
        if chat['chat_id'] == chat_id and chat['chat_code'] == hashlib.sha256(chat_code.encode()).hexdigest():
            if username not in chat['chat_users']:
                chat['chat_users'].append(username)
                chat_manager.write(chats)

            print("You joined this chat.")
            return _50gram(username)

    print("Chat not found.")
    return exit_menu(username)

def delete(username):
    chat_id = int(input("Enter chat id:  "))
    chats = chat_manager.read()

    for chat in chats:
        if chat['chat_id'] == chat_id:
            if username not in chat['chat_users'] or chat['chat_users'].index(username) > 0:
                print("You cannot delete this chat.")
                break
            chats.remove(chat)
            chat_manager.write(chats)
            print("Chat deleted.")

    return exit_menu(username)

def show_created_chats(username):
    chats = chat_manager.read()
    my_chats = []
    for chat in chats:
        if username in chat['chat_users']:
            if chat['chat_users'].index(username) == 0:
                my_chats.append(chat)

    print(my_chats)
    return exit_menu(username)

def show_joined_chats(username):
    chats = chat_manager.read()
    my_chats = []

    for chat in chats:
        if username in chat['chat_users']:
            if chat['chat_users'].index(username) > 0:
                my_chats.append(chat)

    print(my_chats)
    return exit_menu(username)


message_manager = JsonManager('fileManager/messages.json')

def _50gram(username):
    while True:
        user_input = input()

        if user_input.lower() == 'exit':
            open('fileManager/messages.json', 'w').close()
            return exit_menu(username)

        if user_input.lower() == 'show':
            message_print()

        message = {
            'username': username,
            'user_input': user_input,
        }

        message_manager.add_data(message)

        message_print()

def message_print():
    messages = message_manager.read()
    for message in messages:
        print(f"{message['username']}\n\t{message['user_input']}\n-----------------------------------")

def exit_menu(username):
    text = """
        1. Create chat
        2. Join the chat
        3. Delete chat
        4. Show my created chats
        5. Show my joined chats
        6. Exit
    """
    print(text)

    user_input = input("Enter your choice:  ")
    if user_input == '1':
        create(username)

    elif user_input == '2':
        join(username)

    elif user_input == '3':
        delete(username)

    elif user_input == '4':
        show_created_chats(username)

    elif user_input == '5':
        show_joined_chats(username)

    elif user_input == '6':
        show_auth_menu()




if __name__ == '__main__':
    show_auth_menu()
