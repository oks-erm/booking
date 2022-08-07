"""
Functions for validating user input.
"""
from datetime import datetime, date


def to_date(string):
    """
    Converts string date data to date format.
    """
    return datetime.strptime(string, "%d-%m-%Y").date()


def validate_date_input(inp):
    """
    Validates if date is correct dd-mm-yyyy format and
    it's not from the past.
    """
    try:
        if inp != datetime.strptime(inp, "%d-%m-%Y").strftime("%d-%m-%Y") or \
                to_date(inp) < date.today():
            raise ValueError
        return True
    except ValueError:
        return False


def validate_birthdate(inp):
    """
    Validates if date is correct dd-mm-yyyy format and
    it's not from the past.
    """
    try:
        if inp != datetime.strptime(inp, "%d-%m-%Y").strftime("%d-%m-%Y"):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_time_input(inp):
    """
    Validates if time is correct hh:mm format and
    it's not from the past.
    """
    try:
        if inp != datetime.strptime(inp, "%H:%M").strftime("%H:%M"):
            raise ValueError
        return True
    except ValueError:
        return False
