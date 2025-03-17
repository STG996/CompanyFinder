import sqlite3

from account.account import EncryptedAccount
from account.regex import convert_dob_to_age

DATABASE_PATH = "database/main.db"

class Database:
    def __init__(self):
        self.__conn, self.__cursor = self.__connect()

        self.__create_account_table()
        self.__create_company_table()
        self.__create_company_account_table()
        self.__create_matching_table()

        self.account = EncryptedAccount()

    def __connect(self):
        conn = sqlite3.connect(DATABASE_PATH, autocommit=True)
        cursor = conn.cursor()
        return conn, cursor

    # Account Table

    def __create_account_table(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Account (
            AccountUsername TEXT PRIMARY KEY,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            DateOfBirth TEXT,
            MaximumInvestment INTEGER,
            LookingToInvest INTEGER
        )
        """)

    def add_account(self, username, email, password):
        self.__cursor.execute("""
        INSERT INTO Account (AccountUsername, Email, Password) VALUES (
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

    def retrieve_account_settings(self):
        self.__cursor.execute("""
        SELECT DateOfBirth, MaximumInvestment, LookingToInvest FROM Account
        WHERE AccountUsername = :username
        """,
        {
            "username": self.account.get_username()
        })

        return self.__cursor.fetchone()

    def update_account_table(self, dob, max_investment, looking_to_invest):
        self.__cursor.execute("""
        UPDATE Account
        SET DateOfBirth = :dob,
        MaximumInvestment = :max_investment,
        LookingToInvest = :looking_to_invest
        WHERE AccountUsername = :username
        """,
        {
            "dob": dob,
            "max_investment": max_investment,
            "looking_to_invest": looking_to_invest,
            "username": self.account.get_username()
        })

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
        CREATE TABLE IF NOT EXISTS CompanyAccount (
            AccountUsername,
            CompanyName,
            FOREIGN KEY (AccountUsername) REFERENCES Account(AccountUsername),
            FOREIGN KEY (CompanyName) REFERENCES Company(CompanyName),
            PRIMARY KEY (AccountUsername, CompanyName)
        )
        """)

    def register_company(self, company_name, looking_for_investor, minimum_asking_investment, minimum_investor_age):
        self.__cursor.execute("""
            INSERT INTO Company VALUES (
                :company_name,
                :looking_for_investor,
                :minimum_asking_investment,
                :minimum_investor_age
            )
        """,
        {
            "company_name": company_name,
            "looking_for_investor": looking_for_investor,
            "minimum_asking_investment": minimum_asking_investment,
            "minimum_investor_age": minimum_investor_age
        })

        self.__cursor.execute("""
            INSERT INTO CompanyAccount VALUES (
                :username,
                :company_name
            )
        """,
        {
             "username": self.account.get_username(),
             "company_name": company_name
        })

    def get_owned_companies(self):
        self.__cursor.execute("""
        SELECT CompanyAccount.CompanyName, 
        Company.MinimumAskingInvestment,
        Company.MinimumInvestorAge FROM Company, CompanyAccount
        WHERE CompanyAccount.AccountUsername = :username
        AND Company.CompanyName = CompanyAccount.CompanyName
        """, {"username": self.account.get_username()})

        return self.__cursor.fetchall()

    # Matching

    def __create_matching_table(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Matching (
            MatchingId TEXT PRIMARY KEY,
            CompanyName,
            InvestorUsername,
            FOREIGN KEY (CompanyName) REFERENCES Company(CompanyName),
            FOREIGN KEY (InvestorUsername) REFERENCES Account(AccountUsername)
        )
        """)

    def return_potential_matchings(self):
        self.__cursor.execute("""
        SELECT Company.CompanyName, Company.MinimumInvestorAge, Account.DateOfBirth FROM Company, Account, CompanyAccount
        WHERE Account.LookingToInvest = TRUE
        AND Company.LookingForInvestor = TRUE
        AND Account.MaximumInvestment >= Company.MinimumAskingInvestment
        AND Account.AccountUsername = :username
        AND Account.AccountUsername != CompanyAccount.AccountUsername
        ORDER BY Company.MinimumAskingInvestment DESC
        """,
        {"username": self.account.get_username()})

        potential_matchings = self.__cursor.fetchall()
        temp_copy = potential_matchings.copy()
        for matching in temp_copy:
            day, month, year = matching[2].split("/")
            day = int(day)
            month = int(month)
            year = int(year)
            investor_age = convert_dob_to_age(day, month, year)

            if investor_age < matching[1]:
                potential_matchings.remove(matching)
                print(matching, "removed")

        print(potential_matchings)
        return potential_matchings

    def create_matching(self, company_name):
        self.__cursor.execute("""
        INSERT INTO Matching VALUES (
            :matching_id,
            :company_name,
            :investor_username
        )
        """, {"matching_id": company_name+self.account.get_username(), "company_name": company_name, "investor_username": self.account.get_username()})

    def get_matchings(self):
        total_matchings = []
        owner_companies = self.get_owned_companies()
        for company in owner_companies:
            self.__cursor.execute("""
            SELECT Matching.InvestorUsername, Account.Email FROM Matching, Account
            WHERE Matching.CompanyName = :company_name
            AND Account.AccountUsername = Matching.InvestorUsername
            """, {"company_name": company[0]})

            returned_matchings = self.__cursor.fetchall()
            if len(returned_matchings) == 0:
                continue

            for matching in returned_matchings:
                total_matchings.append((matching[0], matching[1], company[0]))

        return total_matchings

    def __del__(self):
        self.__conn.close()
