import re

EMAIL_REGEX = r"^[a-zA-Z0-9.%-+_]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
DATE_REGEX = r"^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$"
INTEGER_REGEX = r"^[0-9]+$"

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

def check_date(date):
    valid = re.match(DATE_REGEX, date)
    return True if valid else False

def check_integer(string):
    valid = re.match(INTEGER_REGEX, string)
    return True if valid else False
