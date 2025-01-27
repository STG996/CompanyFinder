"""
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
"""
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
except FileNotFoundError:
    logged_in = False

screen_stack = Stack()

# Main app class
class CompanyFinderApp(MDApp):
    def build(self):
        # Theme settings
        self.theme_cls.theme_style = "Dark"

        Builder.load_file("screens/signup_screen.kv")
        Builder.load_file("screens/login_screen.kv")
        Builder.load_file("screens/home_screen.kv")
        Builder.load_file("screens/account_screen.kv")

        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(screens.SignupScreen(name="signup_screen"))
        screen_manager.add_widget(screens.LoginScreen(name="login_screen"))
        screen_manager.add_widget(screens.HomeScreen(name="home_screen"))
        screen_manager.add_widget(screens.AccountSettings(name="account_screen"))

        if logged_in:
            screen_manager.current = "home_screen"
            screen_stack.push("home_screen")
        else:
            screen_manager.current = "signup_screen"
            screen_stack.push("signup_screen")

        return screen_manager

if __name__ == "__main__":
    print(logged_in)
    CompanyFinderApp().run()


# ideas for what to do next:
# - make a stack for the loaded screens and pop and stuff
# - figure out what to do next with the main app functionality
# - get the database structure figured out
# - pump the app with features for marks