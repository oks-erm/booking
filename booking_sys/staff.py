"""
Includes staff specific functions.
"""
import getpass
from booking_sys.spreadsheet import update_worksheet, get_data, update_data
from booking_sys.customer import new_phone, search
from booking_sys.decorators import pretty_print, loop_menu_qx


KEYS = get_data("staff")[0]


def create_staff(data):
    """
    Creates a new member of Staff
    """
    print("\n~ ~ x - <== ~ ~")
    user_name = get_name(data)
    if user_name == "x":
        return None
    print(f"Hi, {user_name}!")
    password = getpass.getpass("\n\tCreate a password: ")
    if password == "x":
        return None
    contact = new_phone()
    if contact in ["x", "q"]:
        return None
    user = [user_name, password, contact]
    update_worksheet(user, "staff")
    return dict(zip(KEYS, user))


def get_name(data):
    """
    Accepts user input and checks if it is empty
    or already exists.
    """
    while True:
        name = input("Enter a name for a new member of staff: ")
        if name == "":
            print("Please, enter your name!\n")
            continue
        if name not in [dict['NAME'] for dict in data]:
            return name
        print(f"'{name}' already exists. Try something else.\n")


@loop_menu_qx("\t",
              "x - <== ",
              "press 1 - Staff info\n\t"
              "press 2 - Edit your info\n\t",
              "Invalid input. Please, use options above.")
def staff_menu(*args):
    """
    Displays staff menu.
    """
    user_input, user = (args)
    if user_input == "1":
        all_staff = get_data("staff")
        return staff_info_menu(all_staff)
    if user_input == "2":
        return edit_staff_menu(user)
    return False


@loop_menu_qx("\t\t",
              "x - <== // q - home",
              "Enter 'all' to see the full list\n\t\t"
              "Or enter a name to search by name: ",
              "Invalid input. Please, use options above.")
def staff_info_menu(*args):
    """
    Prints info about members of staff: search by name of a full list.
    """
    name, data = (args)
    if name in [dict['NAME'] for dict in data] or name == "all":
        print_staff_info(name, data)
        return True
    return False


@loop_menu_qx("\t\t",
              "x - <== // q - home",
              "press 1 - Change password\n\t\t"
              "press 2 - Change contact\n\t\t",
              "Invalid input. Please, use options above.")
def edit_staff_menu(*args):
    """
    Edits the current user: password or contact.
    Updates spreadsheet and returns an updated user
    dictionary.
    """
    user_input, user = (args)
    if user_input in ["1", "2"]:
        if user_input == "2":
            attr = "CONTACT"
            new_value = input("\n\t\tEnter new contact: ")
        if user_input == "1":
            attr = "PASSWORD"
            new_value = getpass.getpass("\n\t\tNew password: ")
        update_data("staff", user, attr, new_value)
        return True
    return False


@pretty_print
def print_staff_info(user_input, staff):
    """
    Prints a name and a contact number of a member
    of staff. Takes user input and staff data as params.
    """
    if user_input == "all":
        for item in staff:
            print(f"\t{item['NAME']} : {item['CONTACT']}")
    else:
        result = search(user_input, "NAME", staff)
        print(f"\t{result['NAME']} : {result['CONTACT']}")
