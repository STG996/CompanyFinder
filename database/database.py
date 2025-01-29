import sqlite3

from account.account import EncryptedAccount

DATABASE_PATH = "database/main.db"

class Database:
    def __init__(self):
        self.__conn, self.__cursor = self.__connect()
        self.__create_account_table()
        self.account = EncryptedAccount()

    def __connect(self):
        conn = sqlite3.connect(DATABASE_PATH, autocommit=True)
        cursor = conn.cursor()
        return conn, cursor

    # Account Table

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

        self.account.add_to_file(username, email, password)

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
        self.account.add_to_file(username, email, password)

    # Company Table

    def __create_company_table(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Company (
            CompanyName TEXT PRIMARY KEY,
            LookingForInvestor INTEGER,
            MinimumAskingInvestment INTEGER,
            MinimumInvestorAge INTEGER
        )
        """)

    def __create_company_account_table(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Company (
            
        )
        """) ####### TODO: ask teacher how to implement this exactly

    def __del__(self):
        self.__conn.close()
