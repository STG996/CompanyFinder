import os
import random

USERNAME_INDEX = 1
EMAIL_INDEX = 2
PASSWORD_INDEX = 3

ALPHABET = "".join([chr(x) for x in range(ord("A"), ord("Z")+1)])

class Account:
    def __init__(self):
        self._username = None
        self._email = None
        self._password = None
        self._file_name = "account/account_info.txt"
        self._logged_in = False

    def retrieve_from_file(self):
        file = open(self._file_name, "r")
        lines = file.readlines()
        file.close()

        try:
            self._username = lines[USERNAME_INDEX][:-1]
            self._email = lines[EMAIL_INDEX][:-1]
            self._password = lines[PASSWORD_INDEX][:-1]
            self._logged_in = True
        except IndexError:
            self._logged_in = False

    def add_to_file(self, username, email, password):
        file = open(self._file_name, "w")
        file.write(f"\n{username}\n{email}\n{password}\n")
        file.close()
        self._username = username
        self._email = email
        self._password = password
        self._logged_in = True

    def remove_from_file(self):
        os.remove(self._file_name)

    def get_logged_in(self):
        return self._logged_in

    def get_username(self):
        return self._username

class EncryptedAccount(Account):
    def __init__(self):
        super().__init__()
        self.__key = None

    def __generate_key(self):
        length_required = len(self._username) + len(self._email) + len(self._password) + 5
        self.__key = "".join(random.choice(ALPHABET) for _ in range(length_required))

    def __encrypt_file(self):
        file = open(self._file_name, "r")
        plaintext = file.read()
        file.close()

        self.__generate_key()

        ciphertext = ""
        for count, character in enumerate(plaintext):
            ciphertext += chr(ord(character) ^ ord(self.__key[count]))

        file = open(self._file_name, "w")
        file.write(ciphertext + "XXX" + self.__key)
        file.close()

    def __decrypt_file(self):
        file = open(self._file_name, "r")
        contents = file.read()
        file.close()

        first_x_index = None
        for count, character in enumerate(contents):
            if character == "X" and contents[count + 1] == "X" and contents[count + 2] == "X":
                first_x_index = count
                break
        ciphertext = contents[:first_x_index]
        self.__key = contents[first_x_index+3:]

        plaintext = ""
        for count, character in enumerate(ciphertext):
            plaintext += chr( ord(character) ^ ord(self.__key[count]) )

        file = open(self._file_name, "w")
        file.write(plaintext)
        file.close()

    def retrieve_from_file(self):
        self.__decrypt_file()
        super().retrieve_from_file()
        self.__encrypt_file()

    def add_to_file(self, username, email, password):
        super().add_to_file(username, email, password)
        self.__encrypt_file()