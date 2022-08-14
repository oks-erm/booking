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
                print(indentation + xq_text)
                user_inp = input(indentation + input_prompt)
                if user_inp in ["x", "q"]:
                    break
                result = func(user_inp, *args)
                if result is None:
                    continue
                if result is False:
                    print(indentation + warning)
                else:
                    break
            if user_inp in ["x", "q"]:
                return user_inp
            return result
        return wrap_func
    return decorator


def loop_menu_x(input_prompt):
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
                print("\nx - <==")
                user_inp = input(input_prompt)
                if user_inp == "x":
                    break
                result = func(user_inp, *args)
                if result is False:
                    print("Invalid input. "
                          "Please, use options above.")
                else:
                    break
            if user_inp == "x":
                return user_inp
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
