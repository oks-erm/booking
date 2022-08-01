"""
Includes customers specific functions.
"""
from spreadsheet import get_data, update_worksheet


customers = get_data("customers")[1:]
KEYS = get_data("customers")[0]


def search(name, data):
    """
    Find and returns an element from data
    that has a requested value of NAME.
    """
    for element in data:
        if element['NAME'] == name:
            return element


def create_customer(name):
    """
    Creates a new customer with a parameter 'name' and writes
    it to the spreadsheet.
    """
    new_name = name
    phone = input("Enter contact number: ")
    email = input("Enter email to receive reminders: ")
    bday = input("Enter date of birth: ")
    new_data = [new_name, phone, email, bday, 1, ""]
    update_worksheet(new_data, "customers")
    return dict(zip(KEYS, new_data))


def get_customer():
    """
    Checks if the customer exists and returns
    customer ductionary.
    """
    user_inp = input("Enter customer's name: ")
    names = [dct['NAME'] for dct in customers]
    if user_inp in names:
        return search(user_inp, customers)
    return create_customer(user_inp)