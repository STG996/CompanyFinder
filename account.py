import os

USERNAME_INDEX = 1
EMAIL_INDEX = 2
PASSWORD_INDEX = 3


class Account:
    def __init__(self):
        self.__username = None
        self.__email = None
        self.__password = None
        self.__file_name = "account_info.txt"
        self.__logged_in = False

    def retrieve_account_from_file(self):
        file = open(self.__file_name, "r")
        lines = file.readlines()
        file.close()

        try:
            self.__username = lines[USERNAME_INDEX]
            self.__email = lines[EMAIL_INDEX]
            self.__password = lines[PASSWORD_INDEX]
            self.__logged_in = True
        except IndexError:
            self.__logged_in = False

    def add_account_to_file(self, username, email, password):
        file = open(self.__file_name, "w")
        file.write(f"\n{username}\n{email}\n{password}\n")
        file.close()
        self.retrieve_account_from_file()

    def remove_account_from_file(self):
        os.remove(self.__file_name)

    # Information hiding
    def get_logged_in(self):
        return self.__logged_in, self.__username
