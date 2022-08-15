"""
Main module, includes ...
"""
import sys
import os
from booking_sys.spreadsheet import get_data
from booking_sys import booking
from booking_sys import customer
from booking_sys import auth


def start_menu(user):
    """
    Displays start menu after the user is logged in.
    """
    print(f"\nWhat do you want to do, {user['NAME']}?")
    while True:
        user_inp = input("\npress 1 - Bookings\n"
                         "press 2 - Customers\n"
                         "press 3 - Staff info\n"
                         "press x - Exit\n")
        if user_inp == "1":
            booking.bookings_menu(user)
            continue
        if user_inp == "2":
            customer.customers_menu()
            continue
        if user_inp == "3":
            from booking_sys.staff import staff_menu
            staff_menu(user)
            continue
        if user_inp == "x":
            cleanup()
            sys.exit()
        print("Computer says no. Please, use options above.")


def loop_menu_qx(indentation, qx_text, input_prompt, warning):
    """
    Places a function inside a While Loop, which goes one step
    back if input is "x" and goes back to the start menu input
    is "q". Warns the user about invalid input if a function
    returns False.
    Required parameters:
        indentation(str),
        qx_text(str, navigation instructions at the top of the block,
        leave empty if it repeats too often)
        input_prompt(str, text for input method)
        warning(str, text to warn the user if input is invalid)
    """
    def decorator(func):
        def wrap_func(*args):
            while True:
                result = None
                print("\n" + indentation + qx_text)
                user_inp = input(indentation + input_prompt)
                if user_inp in ["x", "q"]:
                    break
                result = func(user_inp, *args)
                if result == "q":
                    return result
                if result is False:
                    print(indentation + warning)
                    continue
                if result in [None, "x"]:
                    continue
                break
            if user_inp in ["x", "q"]:
                return user_inp
            if result is not True:
                return result
            return None
        return wrap_func
    return decorator


def cleanup():
    """
    Deletes not needed files.
    """
    files = ['stats.pdf', 'stats.csv']
    for file in files:
        if os.path.exists(file):
            os.remove(file)


if __name__ == '__main__':
    all_staff = get_data("staff")
    the_user = auth.staff_login(all_staff)
    start_menu(the_user)
