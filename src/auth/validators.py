import re


def login_validations(email: str, password: str):
    errors = []
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        errors.append("Please provide a valid email\n")
    if len(password) < 6 or len(password) > 20:
        errors.append("Password must be between 6 characters and 20 characters long\n")

    return errors


def register_validations(confirm_password, email, name, password):
    errors = []
    if len(name) < 2 or len(name) > 50:
        errors.append("Name must be between 2 characters and 50 characters long\n")
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        errors.append("Please provide a valid email\n")
    if len(password) < 6 or len(password) > 20:
        errors.append("Password must be between 6 characters and 20 characters long\n")
    if len(confirm_password) < 6 or len(confirm_password) > 20:
        errors.append("Confirm Password must be between 6 characters and 20 characters long\n")
    if password != confirm_password:
        errors.append("Password and Confirm Password are not same \n")

    return errors
