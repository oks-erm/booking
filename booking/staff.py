"""
Includes staff specific functions.
"""
import getpass
from booking.spreadsheet import update_worksheet, get_data, update_data
from booking.booking import pretty_print


KEYS = get_data("staff")[0]


def loop_menu(indentation, text):
    """
    Places a function inside a While Loop,
    which breaks if input is "x" and warns
    about invalid input if a function doesn't
    return True.
    """
    def decorator(func):
        def wrap_func(*args):
            while True:
                print("\n" + indentation + "press x - <==")
                user_inp = input(text)
                if user_inp == "x":
                    break
                result = func(user_inp, *args)
                if result is False:
                    print("\t\tInvalid input. Please, use options above.\n")
                else:
                    break
            if user_inp == "x":
                return None
            return result
        return wrap_func
    return decorator


@loop_menu("", "Enter a name for a new member of staff: ")
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


@loop_menu("\t\t", "\t\tEnter 'all' to see the full list\n"
           "\t\tOr enter a name to search by name: ")
def staff_info_menu(*args):
    """
    Prints info about members of staff: search by name of a full list.
    """
    if args[0] in [dct['NAME'] for dct in args[1]] or args[0] == "all":
        print_staff_info(args[0], args[1])
        return True
    return False


@loop_menu("\t\t", "\t\tpress 1 - Change password\n"
           "\t\tpress 2 - Change contact\n\t\t")
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
    return False


@pretty_print
def print_staff_info(inp, staff):
    """
    Prints a name and a contact number of a member
    of staff. Takes user input and staff data as params.
    """
    if inp == "all":
        for item in staff:
            print(f"\t{item['NAME']} : {item['CONTACT']}")
    else:
        result = [item for item in staff if item["NAME"] == inp]
        print(f"\t{result[0]['NAME']} : {result[0]['CONTACT']}")
