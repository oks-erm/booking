"""
Includes customers specific functions.
"""
from spreadsheet import get_data, update_worksheet


KEYS = get_data("customers")[0]


def search(name, data):
    """
    Find and returns an element from data
    that has a requested value of NAME.
    """
    for element in data:
        if element['NAME'] == name:
            return element


def get_customer():
    """
    Checks if the customer exists and returns
    customer ductionary.
    """
    customers = get_data("customers")[1:]
    user_inp = input("\n\tEnter customer's name: ")
    names = [dct['NAME'] for dct in customers]
    if user_inp in names:
        return search(user_inp, customers)
    return create_customer(user_inp)