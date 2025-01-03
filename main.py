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

import email_regex
from conn.database import Database
from email_regex import check_email_validity

database = Database()

# Screens
class SignupScreen(Screen):
    def create_account(self, username, email, password):
        is_email_valid = check_email_validity(email)
        if is_email_valid:
            database.add_account(username, email, password)
        else:
            self.ids.error = True
            self.ids.email.helper_text = "Invalid email"

    def check_email_uix(self):
        email_regex.check_email_uix(self.ids)       # No better way was found for doing this

class LoginScreen(Screen):
    def check_signin(self, email, password):
        account_list = database.check_account(email, password)
        if len(account_list) == 1:
            database.log_in(account_list[0][0], account_list[0][1], account_list[0][2])

    def check_email_uix(self):
        email_regex.check_email_uix(self.ids)      # No better way was found for doing this

class HomeScreen(Screen):
    pass

# Main app
class MainApp(MDApp):
    def build(self):

        # Theme settings
        self.theme_cls.theme_style = "Dark"

        # Loading screen design files
        Builder.load_file("screens/signup_screen.kv")
        Builder.load_file("screens/login_screen.kv")
        return Builder.load_file("main.kv")# if successful_conn else Builder.load_file("screens/no_internet.kv")


if __name__ == "__main__":
    MainApp().run()