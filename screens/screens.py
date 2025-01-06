from kivy.uix.screenmanager import Screen

from account import email_regex
from account.email_regex import check_email_validity
from main import database


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
