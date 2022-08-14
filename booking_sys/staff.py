"""
Includes staff specific functions.
"""
import getpass
from booking_sys.spreadsheet import update_worksheet, get_data, update_data
from booking_sys.customer import pretty_print
import run


KEYS = get_data("staff")[0]


def staff_menu(user):
    """
    Displays staff menu.
    """
    while True:
        user_input = input("\n\tpress x - <=="
                           "\n\tpress 1 - Staff info"
                           "\n\tpress 2 - Edit your info\n\t")
        if user_input == "1":
            all_staff = get_data("staff")
            result = staff_info_menu(all_staff)
            if result == "q":
                break
        elif user_input == "2":
            result = edit_staff_menu(user)
            if result == "q":
                break
        elif user_input == "x":
            break
        else:
            print("\tInvalid input. Please, use options above.")
    return True


@run.loop_menu_x("",
                 "Enter a name for a new member of staff: ")
def create_staff(*args):
    """
    Creates a new member of Staff
    """
    user_name = args[0]
    print(f"Hi, {user_name}!")
    password = getpass.getpass("Create a password: ")
    contact = input("Awesome! Enter your contact number: ")
    user = [user_name, password, contact]
    update_worksheet(user, "staff")
    return dict(zip(KEYS, user))


@run.loop_menu_qx("\t\t",
                  # new line is necessary here, in most cases
                  # it is not needed but for a couple occasions
                  # it is needed, so after a new line, additional
                  # indentation is required
                  "\n\t\tx - <== // q - home",
                  "Enter 'all' to see the full list\n\t\t"
                  "Or enter a name to search by name: ",
                  "Invalid input. Please, use options above.")
def staff_info_menu(*args):
    """
    Prints info about members of staff: search by name of a full list.
    """
    user_input, data = (args)
    if user_input in [dict['NAME'] for dict in data] or user_input == "all":
        print_staff_info(user_input, data)
        return True
    return False


@run.loop_menu_qx("\t\t",
                  # new line is necessary here, in most cases
                  # it is not needed but for a couple occasions
                  # it is needed, so after a new line, additional
                  # indentation is required
                  "\n\t\tx - <== // q - home",
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
        result = [item for item in staff if item["NAME"] == user_input]
        print(f"\t{result[0]['NAME']} : {result[0]['CONTACT']}")
