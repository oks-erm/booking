"""
Functions for validating user input.
"""
import re
from datetime import datetime, date


def to_date(string):
    """
    Converts string date data to date format.
    """
    for date_format in ('%d-%m-%Y', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(string, date_format).date()
        except ValueError:
            pass
    return False


def validate_date_input(new_date):
    """
    Validates if date is correct dd-mm-yyyy format and
    it's not from the past.
    """
    try:
        if ((to_date(new_date) is False) or
                (to_date(new_date) <= date.today())):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_birthdate(new_date):
    """
    Validates if date is correct dd-mm-yyyy format and
    it's not from the past.
    """
    try:
        if to_date(new_date) is False:
            raise ValueError
        return True
    except ValueError:
        return False


def validate_time_input(new_time):
    """
    Validates if time is correct hh:mm format and
    it's not from the past.
    """
    try:
        if new_time != datetime.strptime(new_time, "%H:%M").strftime("%H:%M"):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_email(email):
    """
    Checks if an email is a valid email address.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False
