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

# Database initialisation
database = Database()
try:
    database.account.retrieve_from_file()
    logged_in = database.account.get_logged_in()
except FileNotFoundError:
    logged_in = False

# Main app class
class CompanyFinderApp(MDApp):
    def build(self):
        # Theme settings
        self.theme_cls.theme_style = "Dark"

        Builder.load_file("screens/signup_screen.kv")
        Builder.load_file("screens/login_screen.kv")
        Builder.load_file("screens/home_screen.kv")

        screen_manager = ScreenManager(transition=NoTransition())
        if not logged_in:
            screen_manager.add_widget(screens.SignupScreen(name="signup_screen"))
            screen_manager.add_widget(screens.LoginScreen(name="login_screen"))
        screen_manager.add_widget(screens.HomeScreen(name="home_screen"))

        return screen_manager

if __name__ == "__main__":
    print(logged_in)
    CompanyFinderApp().run()