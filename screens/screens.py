from kivymd.uix.screen import MDScreen

from account.regex import check_email_validity
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

class LoginScreen(MDScreen):
    def check_signin(self, email, password):
        account_list = database.check_account(email, password)
        if len(account_list) == 1:
            database.log_in(account_list[0][0], account_list[0][1], account_list[0][2])
            self.parent.current = clear_and_go_to_screen("home_screen")

class HomeScreen(MDScreen):
    pass

class AccountSettings(MDScreen):
    def on_log_out(self):
        database.account.remove_from_file()

    def retrieve_account_settings(self):
        value = database.retrieve_account_settings()
        return value

    def update_settings(self):
        if not self.ids.dob.error and not self.ids.max_investment.error:
            database.update_account_table(self.ids.dob.text, int(self.ids.max_investment.text), self.ids.looking_to_invest.active)

class CompanyRegistrationScreen(MDScreen):
    pass
