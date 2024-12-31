import sqlite3

from account import EncryptedAccount

DATABASE_PATH = "conn/main.db"

class Database:
    def __init__(self):
        self.__conn, self.__cursor = self.__connect()
        self.__create_account_table()
        self.__account = EncryptedAccount()

    def __connect(self):
        conn = sqlite3.connect(DATABASE_PATH, autocommit=True)
        cursor = conn.cursor()
        return conn, cursor

    def __create_account_table(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Account (
            Username TEXT PRIMARY KEY,
            Email TEXT,
            Password TEXT
        )
        """)

    def add_account(self, username, email, password):
        self.__cursor.execute("""
        INSERT INTO Account VALUES (
            :username,
            :email,
            :password
        )
        """,
        {
            "username": username,
            "email": email,
            "password": password
        })

        self.__account.add_to_file(username, email, password)

    def check_account(self, email, password):
        self.__cursor.execute("""
        SELECT * FROM Account
        WHERE Email = :email AND Password = :password
        """,
        {
            "email": email,
            "password": password
        })

        account_list = self.__cursor.fetchall()
        return account_list

    def log_in(self, username, email, password):
        self.__account.add_to_file(username, email, password)

    def __del__(self):
        self.__conn.close()
