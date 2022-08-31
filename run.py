"""
Main module.
"""
import sys
import os
from booking_sys.spreadsheet import get_data
from booking_sys import booking
from booking_sys import customer
from booking_sys import auth


def start_menu(user):
    """
    Takes in a user(dict). Displays start menu after 
    the user is logged in.
    """
    print(f"What do you want to do, {user['NAME']}?")
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
            return sys.exit()
        print("Computer says no. Please, use options above.")


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
