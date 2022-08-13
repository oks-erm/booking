"""
Main module, includes ...
"""
import sys
import os
# import pdb
from booking_sys.spreadsheet import get_data
import booking_sys.booking as booking
import booking_sys.customer as customer
import booking_sys.auth as auth
# from booking_sys import new


def start_menu(user):
    """
    Displays start menu after the user is logged in.
    """
    print(f"\nWhat do you want to do, {user['NAME']}?")
    while True:
        user_inp = input("press 1 - Bookings\n"
                         "press 2 - Customers\n"
                         "press 3 - Staff info\n"
                         "press x - Exit\n")
        if user_inp == "1":
            booking.bookings_menu(user)
            break
        if user_inp == "2":
            customer.customers_menu(user)
            print("Customers")
            break
        if user_inp == "3":
            from booking_sys.staff import staff_menu
            staff_menu(user)
            break
        if user_inp == "x":
            cleanup()
            sys.exit()
        print("Invalid input. Please, use options above.\n")


def loop_menu_qx(indentation, xq_text, input_prompt, warning):
    """
    Places a function inside a While Loop,
    which breaks if input is "x" and goes back
    to the start menu in input is "q". Also warns
    about invalid input if a function doesn't
    return a dictionary.
    """
    def decorator(func):
        def wrap_func(*args):
            while True:
                result = None
                print("\n" + indentation + xq_text)
                user_inp = input(input_prompt)
                if user_inp in ["x", "q"]:
                    break
                result = func(user_inp, *args)
                # function returns a dict with the user instead False
                # so it can be used to call start_menu when q is pressed
                if isinstance(result, dict) or result is False:
                    print(indentation + warning)
                else:
                    break
            if user_inp == "x":
                return None
            if user_inp == "q":
                result = func(user_inp, *args)
                start_menu(result)
                return None
            return result
        return wrap_func
    return decorator


def loop_menu_x(indentation, input_prompt):
    """
    Places a function inside a While Loop,
    which breaks if input is "x" and warns
    about invalid input if a function doesn't
    return True.
    """
    def decorator(func):
        def wrap_func(*args):
            while True:
                result = None
                print("\n" + indentation + "x - <==")
                user_inp = input(input_prompt)
                if user_inp == "x":
                    break
                result = func(user_inp, *args)
                if result is False:
                    print(indentation + "Invalid input. "
                          "Please, use options above.")
                else:
                    break
            if user_inp == "x":
                return None
            return result
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


def main():
    all_staff = get_data("staff")
    the_user = auth.staff_login(all_staff)
    start_menu(the_user)


if __name__ == '__main__':
    main()
