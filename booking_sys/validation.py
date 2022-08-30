"""
Functions for validating user input.
"""
import re
from datetime import datetime, date


def to_date(string):
    """
    Converts a string date to date format.
    """
    try:
        return datetime.strptime(string, '%d-%m-%Y').date()
    except (ValueError, TypeError):
        return False


def convert_date(new_date):
    """
    Converts a date with various date separators
    into a date separated with "-".
    """
    try:
        return re.sub('[/,.]', '-', new_date)
    except (ValueError, TypeError):
        return False


def date_input(new_date):
    """
    Validates if a date is correct dd mm yyyy format and
    it's not from the past. Returns a valid date in a valid
    format or False.
    """
    try:
        f_date = convert_date(new_date)
        if ((f_date != datetime.strptime(f_date, "%d-%m-%Y")
             .strftime("%d-%m-%Y")) or
                (to_date(f_date) < date.today())):
            raise ValueError
        return f_date
    except (ValueError, TypeError):
        return False


def birthdate(new_date):
    """
    Validates if a date is correct dd mm yyyy format.
    Returns a valid date in a valid format or False.
    """
    try:
        f_date = convert_date(new_date)
        if ((f_date != datetime.strptime(f_date, "%d-%m-%Y")
            .strftime("%d-%m-%Y")) or
                (to_date(f_date) > date.today())):
            raise ValueError
        return f_date
    except (ValueError, TypeError):
        return False


def time_input(new_time):
    """
    Validates if time is correct hh:mm format and
    it's not from the past. Returns boolean.
    """
    try:
        if new_time != datetime.strptime(new_time, "%H:%M").strftime("%H:%M"):
            raise ValueError
        return True
    except (ValueError, TypeError):
        return False


def email(user_email):
    """
    Checks if an email is a valid email address.
    Returns boolean.
    """
    try:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, user_email):
            return True
        raise ValueError
    except (ValueError, TypeError):
        return False


def phone_num(user_phone):
    """
    Validates a phone number. Force start with a plus
    or two zeros. White space, brackets, minus and
    point are optional, no other characters allowed.
    Returns boolean.
    """
    try:
        regex = r'^(\+|00)[1-9][0-9 \-\(\)\.]{7,16}$'
        if re.fullmatch(regex, user_phone):
            return True
        raise ValueError
    except (ValueError, TypeError):
        return False
