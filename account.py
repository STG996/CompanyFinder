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
        self._file_name = "account_info.txt"
        self._logged_in = False

    def retrieve_account_from_file(self):
        file = open(self._file_name, "r") # will error if file not found, TODO: fix
        lines = file.readlines()
        file.close()

        try:
            self._username = lines[USERNAME_INDEX]
            self._email = lines[EMAIL_INDEX]
            self._password = lines[PASSWORD_INDEX]
            self._logged_in = True
        except IndexError:
            self._logged_in = False

    def add_account_to_file(self, username, email, password):
        file = open(self._file_name, "w")
        file.write(f"\n{username}\n{email}\n{password}\n")
        file.close()
        self.retrieve_account_from_file()

    def remove_account_from_file(self):
        os.remove(self._file_name)

    # Information hiding
    def get_logged_in(self):
        return self._logged_in, self._username

class EncryptedAccount(Account):
    def __init__(self):
        super().__init__()
        self.__key = None

    def __generate_key(self):
        length_required = len(self._username) + len(self._email) + len(self._password)
        self.__key = "".join(random.choice(ALPHABET) for x in range(length_required))

    def __encrypt_file(self):
        file = open(self._file_name, "r")
        plaintext = file.read()
        file.close()

        ciphertext = ""
        for count, character in enumerate(plaintext):
            ciphertext += chr(ord(character) ^ ord(self.__key[count]))

        file = open(self._file_name, "w")
        file.write(self.__key + "BREAKER" + ciphertext) # breaker is placeholder TODO: make better breaker
        file.close()