from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from db_connection import connect_to_db, add_account


# Screens
class SignupScreen(Screen):
    def create_account(self, username, email, password):
        add_account(conn, cursor, username, email, password)

# Database connection
conn, cursor = connect_to_db()

# Main app
class MainApp(MDApp):
    def build(self):

        # Theme settings
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Loading screen design files
        Builder.load_file("signupscreen.kv")
        return Builder.load_file("main.kv")


if __name__ == "__main__":
    MainApp().run()