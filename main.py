from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp

from database.database import Database
from screens import screens
from screens.stack import Stack

# Database initialisation
database = Database()
try:
    database.account.retrieve_from_file()
    logged_in = database.account.get_logged_in()
except:
    logged_in = False

previous_screens = Stack()

# Main app class
class CompanyFinderApp(MDApp):
    def build(self):
        # Theme settings
        self.theme_cls.theme_style = "Dark"

        Builder.load_file("screens/signup_screen.kv")
        Builder.load_file("screens/login_screen.kv")
        Builder.load_file("screens/home_screen.kv")
        Builder.load_file("screens/account_screen.kv")
        Builder.load_file("screens/company_registration_screen.kv")
        Builder.load_file("screens/my_companies_screen.kv")
        Builder.load_file("screens/match_requests_screen.kv")
        Builder.load_file("screens/matching_companies_screen.kv")

        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(screens.SignupScreen(name="signup_screen"))
        screen_manager.add_widget(screens.LoginScreen(name="login_screen"))
        screen_manager.add_widget(screens.HomeScreen(name="home_screen"))
        screen_manager.add_widget(screens.AccountSettings(name="account_screen"))
        screen_manager.add_widget(screens.CompanyRegistrationScreen(name="company_registration_screen"))
        screen_manager.add_widget(screens.MyCompaniesScreen(name="my_companies_screen"))
        screen_manager.add_widget(screens.MatchRequestsScreen(name="match_requests_screen"))
        screen_manager.add_widget(screens.MatchingCompaniesScreen(name="matching_companies_screen"))

        if logged_in:
            screen_manager.current = "home_screen"
            previous_screens.push("home_screen")
        else:
            screen_manager.current = "signup_screen"
            previous_screens.push("signup_screen")

        return screen_manager

if __name__ == "__main__":
    print(logged_in)
    CompanyFinderApp().run()
