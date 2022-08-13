"""
Functions for validating user input.
"""
import re
from datetime import datetime, date


def to_date(string):
    """
    Converts string date data to date format.
    """
    try:
        return datetime.strptime(string, '%d-%m-%Y').date()
    except ValueError:
        return False


def convert_date(new_date):
    """
    Converts a date with various date separators
    into a date separated with "-".
    """
    repl_delim = '-'
    return re.sub('[/,.]', repl_delim, new_date)


def date_input(new_date):
    """
    Validates if date is correct dd mm yyyy format and
    it's not from the past.
    """
    try:
        f_date = convert_date(new_date)
        if ((f_date != datetime.strptime(f_date, "%d-%m-%Y")
             .strftime("%d-%m-%Y")) or
                (to_date(f_date) < date.today())):
            raise ValueError
        return f_date
    except ValueError:
        return False


def birthdate(new_date):
    """
    Validates if date is correct dd mm yyyy format.
    """
    try:
        f_date = convert_date(new_date)
        if (f_date != datetime.strptime(f_date, "%d-%m-%Y")
                .strftime("%d-%m-%Y")):
            raise ValueError
        return f_date
    except ValueError:
        return False


def time_input(new_time):
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


def email(user_email):
    """
    Checks if an email is a valid email address.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, user_email):
        return True
    return False
