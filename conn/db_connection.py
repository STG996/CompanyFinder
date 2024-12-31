import sqlite3

DATABASE_PATH = "conn/main.db"

'''
# Initialise connection with database
def connect_to_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="compsci_project"
    )
    cursor = conn.cursor(buffered=True)

    return conn, cursor

# Inserting new account into database
def add_account(conn, cursor, username, email, password):
    cursor.execute(
        f"INSERT INTO account (username, email, password) VALUES ('{username}', '{email}', '{password}');"
    )
    conn.commit()

    print(f"Created account:\nUsername:\t{username}\nEmail:\t{email}\nPassword:\t{password}")

# Check account
def check_account(conn, cursor, email, password):
    cursor.execute(
        f"SELECT * FROM account WHERE email = '{email}' AND password = '{password}';"
    )
    account = cursor.fetchall()

    return account
'''

class Database:
    def __init__(self):
        self.__conn, self.__cursor = self.__connect()
        self.__create_account_table()

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
        self.__conn.close()
