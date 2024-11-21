import re

EMAIL_REGEX = r"^[a-zA-Z0-9.%-+_]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def check_email_validity(email):
    valid = re.match(EMAIL_REGEX, email)
    return True if valid else False