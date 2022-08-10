"""
Main module, includes main logic flow and menus.
"""
import sys
import os
from booking.auth import staff_login
from booking.staff import edit_staff_menu, staff_info_menu
from booking.spreadsheet import get_data
from booking.booking import new_booking, view_bookings_menu, edit_bookings
from booking.customer import view_customer, find_customer
from booking.stats import customers_stats, data_for_stats


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
            bookings_menu(user)
            break
        if user_inp == "2":
            customers_menu(user)
            print("Customers")
            break
        if user_inp == "3":
            staff_menu(user)
            break
        if user_inp == "x":
            cleanup()
            sys.exit()
        print("Invalid input. Please, use options above.\n")


def bookings_menu(user):
    """
    Displays booking menu
    """
    while True:
        user_inp = input("\n\tpress 1 - View bookings"
                         "\n\tpress 2 - Add a booking"
                         "\n\tpress 3 - Edit bookings"
                         "\n\tpress x - <==\n\t")
        if user_inp == "1":
            view_bookings_menu()
            continue
        if user_inp == "2":
            customer = find_customer()
            if customer is None:
                continue
            new_booking(user, customer)
            continue
        if user_inp == "3":
            edit_bookings()
            continue
        if user_inp == "x":
            start_menu(user)
            break
        print("\tInvalid input. Please, use options above.")
    start_menu(user)


def customers_menu(user):
    """
    Displays Customers Menu.
    """
    while True:
        user_inp = input("\n\tpress 1 - View a customer"
                         "\n\tpress 2 - List of customers"
                         "\n\tpress 3 - Stats"
                         "\n\tpress x - <==\n\t")
        if user_inp == "1":
            user_inp = input("\n\tEnter name: ")
            view_customer(user_inp)
        elif user_inp == "2":
            view_customer("all")
        elif user_inp == "3":
            data_for_stats()
            customers_stats()
            print("\tYour stats is ready! Check your Reports folder.")
        elif user_inp == "x":
            start_menu(user)
            break
        else:
            print("\tInvalid input. Please, use options above.")
    start_menu(user)


def staff_menu(user):
    """
    Displays staff menu.
    """
    while True:
        user_inp = input("\n\tpress 1 - Staff info"
                         "\n\tpress 2 - Edit your info"
                         "\n\tpress x - <==\n\t")
        if user_inp == "1":
            staff_info_menu(staff)
            continue
        if user_inp == "2":
            edit_staff_menu(user)
            continue
        if user_inp == "x":
            start_menu(user)
            break
        print("\tInvalid input. Please, use options above.")


def cleanup():
    """
    Deletes not needed files.
    """
    files = ['stats.pdf', 'stats.csv']
    for file in files:
        if os.path.exists(file):
            os.remove(file)


if __name__ == '__main__':
    staff = get_data("staff")
    the_user = staff_login(staff)
    print(f"{the_user['NAME']} : {the_user['CONTACT']}")
    start_menu(the_user)
