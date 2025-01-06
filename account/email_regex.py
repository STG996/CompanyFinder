import re

EMAIL_REGEX = r"^[a-zA-Z0-9.%-+_]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def check_email_validity(email):
    valid = re.match(EMAIL_REGEX, email)
    return True if valid else False

def check_email_uix(text_field):
    if not check_email_validity(text_field.email.text):
        text_field.email.error = True
        text_field.email.helper_text = "Invalid email"
    else:
        text_field.email.error = False
        text_field.email.helper_text = ""