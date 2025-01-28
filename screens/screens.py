from kivymd.uix.screen import MDScreen

from account import email_regex
from account.email_regex import check_email_validity
from main import database, previous_screens

# Screen stack manipulation
def go_to_screen(current_screen, new_screen):
    previous_screens.push(current_screen)
    return new_screen

def clear_and_go_to_screen(new_screen):
    previous_screens.clear()
    return new_screen

def go_back():
    return previous_screens.pop()

class SignupScreen(MDScreen):
    def create_account(self, username, email, password):
        is_email_valid = check_email_validity(email)
        if is_email_valid:
            database.add_account(username, email, password)

            self.parent.current = clear_and_go_to_screen("home_screen")

        else:
            self.ids.error = True
            self.ids.email.helper_text = "Invalid email"

class LoginScreen(MDScreen):
    def check_signin(self, email, password):
        account_list = database.check_account(email, password)
        if len(account_list) == 1:
            database.log_in(account_list[0][0], account_list[0][1], account_list[0][2])
            self.parent.current = clear_and_go_to_screen("home_screen")

class HomeScreen(MDScreen):
    def go_to_account_screen(self):
        previous_screens.push("account_screen")
        return previous_screens.peek()

class AccountSettings(MDScreen):
    def on_log_out(self):
        database.account.remove_from_file()

    def go_back(self):
        previous_screens.pop()
        return previous_screens.peek()

    def go_to_signup_screen(self):
        previous_screens.clear()
        previous_screens.push("signup_screen")
        return previous_screens.peek()
