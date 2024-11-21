from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from conn.db_connection import connect_to_db, add_account, check_account
from email_regex import check_email_validity


# Screens
class SignupScreen(Screen):
    def create_account(self, username, email, password):
        is_email_valid = check_email_validity(email)
        if is_email_valid:
            add_account(conn, cursor, username, email, password)
        else:
            # TODO: ADD UIX TO SHOW INVALID EMAIL
            pass

class LoginScreen(Screen):
    def check_signin(self, email, password):
        is_valid = check_account(conn, cursor, email, password)
        if is_valid:
            # Do next step
            print("Account is valid and was found")

# Database connection
successful_conn = True
try:
    conn, cursor = connect_to_db()
except:
    successful_conn = False

# Main app
class MainApp(MDApp):
    def build(self):

        # Theme settings
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Loading screen design files
        Builder.load_file("screens/signup_screen.kv")
        Builder.load_file("screens/login_screen.kv")
        return Builder.load_file("main.kv") if successful_conn else Builder.load_file("screens/no_internet.kv")


if __name__ == "__main__":
    MainApp().run()