import sqlite3
from functools import partial

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText

from account.regex import check_email_validity, check_date, check_integer
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

def show_snackbar(supporting_text):
    MDSnackbar(
        MDSnackbarSupportingText(
            text=supporting_text,
            halign="center"
        ),
        size_hint_x=0.5,
        pos_hint={"center_x": 0.5}
    ).open()

# Screen classes
class SignupScreen(MDScreen):
    def create_account(self, username, email, password):
        is_email_valid = check_email_validity(email)
        if is_email_valid:
            try:
                database.add_account(username, email, password)
                self.parent.current = clear_and_go_to_screen("home_screen")
            except sqlite3.IntegrityError:
                show_snackbar("Username or email already in use!")
        else:
            show_snackbar("Invalid email")

class LoginScreen(MDScreen):
    def check_signin(self, email, password):
        account_list = database.check_account(email, password)
        if len(account_list) == 1:
            database.log_in(account_list[0][0], account_list[0][1], account_list[0][2])
            self.parent.current = clear_and_go_to_screen("home_screen")
        else:
            show_snackbar("Incorrect email or password")

class HomeScreen(MDScreen):
    pass

class AccountSettings(MDScreen):
    def on_enter(self):
        try:
            account_settings = database.retrieve_account_settings()
            self.ids.dob.text = account_settings[0]
            self.ids.max_investment.text = str(account_settings[1])
            self.ids.looking_to_invest.active = bool(account_settings[2])
        except:
            pass # If no values entered yet, do nothing

    def on_log_out(self):
        database.account.remove_from_file()

    def retrieve_account_settings(self, index):
        value = database.retrieve_account_settings()[index]
        if value == None:
            show_snackbar("No settings were found")
            if index == 2:
                return False
            return ""
        return value

    def update_settings(self):
        if not self.ids.dob.error and not self.ids.max_investment.error and check_date(self.ids.dob.text) and check_integer(self.ids.max_investment.text):
            database.update_account_table(self.ids.dob.text, int(self.ids.max_investment.text), self.ids.looking_to_invest.active)
            show_snackbar("Updated successfully!")
        else:
            show_snackbar("Invalid date of birth or investment amount")

class CompanyRegistrationScreen(MDScreen):
    def register_company(self):
        if check_integer(self.ids.min_investment.text):
            try:
                database.register_company(self.ids.company_name.text, self.ids.looking_for_investor.active,
                                          self.ids.min_investment.text, self.ids.min_age.value)
                show_snackbar("Company registered successfully!")
                self.parent.current = go_back()
            except sqlite3.IntegrityError:
                show_snackbar("Company name already taken")
        else:
            show_snackbar("Invalid minimum investment amount")

class MyCompaniesScreen(MDScreen):
    def on_enter(self):
        self.ids.company_list.clear_widgets()
        print(database.get_owned_companies())
        for company in database.get_owned_companies():
            print(company)
            self.ids.company_list.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text=company[0]
                    ),
                    MDListItemSupportingText(
                        text=f"Min. investment: ${company[1]}"
                    ),
                    MDListItemSupportingText(
                        text=f"Min. investor age: {company[2]} years"
                    )
                )
            )

class MatchRequestsScreen(MDScreen):
    def on_enter(self):
        self.ids.match_requests_list.clear_widgets()
        match_requests = database.get_matchings()
        print(match_requests)
        for request in match_requests:
            print(f"request: {request}")
            print(f"request[0]: {request[0]}")
            list_item = MDListItem(
                MDListItemHeadlineText(
                    text=request[0]
                ),
                MDListItemSupportingText(
                    text="Investor email: "+request[1]
                ),
                MDListItemTertiaryText(
                    text="Request for "+request[2]
                )
            )
            self.ids.match_requests_list.add_widget(list_item)

class MatchingCompaniesScreen(MDScreen):
    def on_enter(self):
        show_snackbar("Press on a company to send a match request")

        self.ids.matching_companies_list.clear_widgets()
        potential_matchings = database.return_potential_matchings()
        for matching in potential_matchings:
            list_item = MDListItem(
                MDListItemHeadlineText(
                    text=matching[0]
                )
            )
            list_item.bind(on_release=partial(self.create_matching_and_show_snackbar, matching[0]))
            self.ids.matching_companies_list.add_widget(list_item)

    def create_matching_and_show_snackbar(self, *args):
        print(*args)
        try:
            database.create_matching(args[0])
            show_snackbar("Match request sent!")
        except:
            show_snackbar("Match request already sent")
