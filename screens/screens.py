from kivymd.uix.screen import MDScreen

from account import email_regex
from account.email_regex import check_email_validity
from main import database, screen_stack

class SignupScreen(MDScreen):
    def create_account(self, username, email, password):
        is_email_valid = check_email_validity(email)
        if is_email_valid:
            database.add_account(username, email, password)

            screen_stack.pop()
            screen_stack.push("home_screen")
            self.parent.current = screen_stack.peek()

        else:
            self.ids.error = True
            self.ids.email.helper_text = "Invalid email"

    def check_email_uix(self):
        email_regex.check_email_uix(self.ids)       # No better way was found for doing this

    def go_to_login_screen(self):
        screen_stack.push("login_screen")
        return screen_stack.peek()

class LoginScreen(MDScreen):
    def check_signin(self, email, password):
        account_list = database.check_account(email, password)
        if len(account_list) == 1:
            database.log_in(account_list[0][0], account_list[0][1], account_list[0][2])
            self.parent.current = "home_screen"

    def check_email_uix(self):
        email_regex.check_email_uix(self.ids)      # No better way was found for doing this

    def go_to_home_screen(self):
        screen_stack.pop()
        screen_stack.push("home_screen")
        return screen_stack.peek()

    def go_back(self):
        screen_stack.pop()
        return screen_stack.peek()

class HomeScreen(MDScreen):
    def go_to_account_screen(self):
        screen_stack.push("account_screen")
        return screen_stack.peek()

class AccountSettings(MDScreen):
    def on_log_out(self):
        database.account.remove_from_file()

    def go_back(self):
        screen_stack.pop()
        return screen_stack.peek()

    def go_to_signup_screen(self):
        screen_stack.clear()
        screen_stack.push("signup_screen")
        return screen_stack.peek()
