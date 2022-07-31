"""
Includes staff specific functions and classes.
"""
import getpass
from spreadsheet import update_worksheet, get_data
from booking import pretty_print


KEYS = get_data("staff")[0]


def create_staff():
    """
    Creates a new member of Staff
    """
    new_name = input("Enter a name for a new member of staff:\n")
    print(f"Hi, {new_name}!")
    password = getpass.getpass("Create a password:")
    contact = input("Awesome! Enter your contact number:")
    user = [new_name, password, contact]
    update_worksheet(user, "staff")
    return dict(zip(KEYS, user))


@pretty_print
def print_staff_info(inp, staff):
    """
    ...
    """
    if inp == "all":
        for item in staff:
            print(f"{item.get('NAME')} : {item.get('CONTACT')}")
    else:
        result = [item for item in staff if item["NAME"] == inp]
        print(f"{result[0].get('NAME')} : {result[0].get('CONTACT')}")
