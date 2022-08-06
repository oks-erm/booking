"""
Includes staff specific functions.
"""
import getpass
from spreadsheet import update_worksheet, get_data, update_data
from booking import pretty_print
from customer import search


KEYS = get_data("staff")[0]


def create_staff():
    """
    Creates a new member of Staff
    """
    new_name = input("Enter a name for a new member of staff: ")
    print(f"Hi, {new_name}!")
    password = getpass.getpass("Create a password: ")
    contact = input("Awesome! Enter your contact number: ")
    user = [new_name, password, contact]
    update_worksheet(user, "staff")
    return dict(zip(KEYS, user))


def staff_info_menu(staff_list):
    """
    Prints info about members of staff: search by name of a full list.
    """
    while True:
        print("\n\tEnter 'all' to see the full list")
        request = input("\tOr enter a name to search by name: ")
        if request in [dct['NAME'] for dct in staff_list] or request == "all":
            print_staff_info(request, staff_list)
            break
        print("\tNothing found, try again or view the full list.")


def edit_staff_menu(staff, user):
    """
    Edits instance of the current user. If the user wants
    to change a password or contact"
    """
    while True:
        user_inp = input("\t\tpress 1 - Change password\n\
                press 2 - Change contact\n\
                press x - <==\n\t\t")
        if user_inp in ["1", "2"]:
            if user_inp == "2":
                attr = "CONTACT"
                new_value = input("\n\t\tEnter new contact: ")
            if user_inp == "1":
                attr = "PASSWORD"
                new_value = getpass.getpass("\n\t\tNew password: ")
            updated_user = update_data("staff", user, attr, new_value)
            old_user = search(updated_user["NAME"], "NAME", staff)
            old_user.update(updated_user)
            break
        if user_inp == "x":
            break
        print("\t\tInvalid input. Please, use options above.\n")


@pretty_print
def print_staff_info(inp, staff):
    """
    ...
    """
    if inp == "all":
        for item in staff:
            print(f"\t{item['NAME']} : {item['CONTACT']}")
    else:
        result = [item for item in staff if item["NAME"] == inp]
        print(f"\t{result[0]['NAME']} : {result[0]['CONTACT']}")
