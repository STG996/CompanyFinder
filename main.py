'''
CompanyFinder: AQA non-exam assessment submission 2025
Copyright (C) 2024  STG996

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from conn.db_connection import connect_to_db, add_account, check_account
from email_regex import check_email_validity


# Screens
class SignupScreen(Screen):
    def create_account(self, username, email, password):
        is_email_valid = check_email_validity(email)
        if is_email_valid:
            add_account(conn, cursor, username, email, password)
        else:
            # TODO: ADD UIX TO SHOW INVALID EMAIL
            pass

class LoginScreen(Screen):
    def check_signin(self, email, password):
        is_valid = check_account(conn, cursor, email, password)
        if is_valid:
            # Do next step
            print("Account is valid and was found")

# Database connection
successful_conn = True
try:
    conn, cursor = connect_to_db()
except:
    successful_conn = False

# Main app
class MainApp(MDApp):
    def build(self):

        # Theme settings
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Loading screen design files
        Builder.load_file("screens/signup_screen.kv")
        Builder.load_file("screens/login_screen.kv")
        return Builder.load_file("main.kv") if successful_conn else Builder.load_file("screens/no_internet.kv")


if __name__ == "__main__":
    MainApp().run()