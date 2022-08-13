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
            staff_info_menu(all_staff, user)
            continue
        if user_input == "2":
            edit_staff_menu(user)
            continue
        if user_input == "x":
            run.start_menu(user)
            break
        print("\tInvalid input. Please, use options above.")
    return True


@run.loop_menu_x("",
                 "Enter a name for a new member of staff: ")
def create_staff(*args):
    """
    Creates a new member of Staff
    """
    print(f"Hi, {args[0]}!")
    password = getpass.getpass("Create a password: ")
    contact = input("Awesome! Enter your contact number: ")
    user = [args[0], password, contact]
    update_worksheet(user, "staff")
    return dict(zip(KEYS, user))


@run.loop_menu_qx("\t\t",
                  "x - <== // q - home",
                  "\t\tEnter 'all' to see the full list\n"
                  "\t\tOr enter a name to search by name: ",
                  "Invalid input. Please, use options above.")
def staff_info_menu(*args):
    """
    Prints info about members of staff: search by name of a full list.
    """
    if args[0] in [dict['NAME'] for dict in args[1]] or args[0] == "all":
        print_staff_info(args[0], args[1])
        return True
    return args[2]


@run.loop_menu_qx("\t\t",
                  "x - <== // q - home",
                  "\t\tpress 1 - Change password\n"
                  "\t\tpress 2 - Change contact\n\t\t",
                  "Invalid input. Please, use options above.")
def edit_staff_menu(*args):
    """
    Edits instance of the current user. If the user wants
    to change a password or contact"
    """
    if args[0] in ["1", "2"]:
        if args[0] == "2":
            attr = "CONTACT"
            new_value = input("\n\t\tEnter new contact: ")
        if args[0] == "1":
            attr = "PASSWORD"
            new_value = getpass.getpass("\n\t\tNew password: ")
        update_data("staff", args[1], attr, new_value)
        return True
    return args[1]


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
