"""
Main module, includes main logic flow and menus.
"""
import sys
import os
import getpass
from staff import create_staff, edit_staff_menu, staff_info_menu
from spreadsheet import get_data
from booking import new_booking, view_bookings_menu, edit_bookings
from customer import search, view_customer, find_customer
from stats import customers_stats, data_for_stats


def authorise(user):
    """
    Checks the user's password
    """
    for i in range(4):
        print(f"Attempt {i+1} of 4")
        password = getpass.getpass("Password:")
        if user["PASSWORD"] == password:
            print("All good!\n")
            return True
        print("The password is not correct! Try again!\n")


def staff_login(data):
    """
    Logs in a member of staff.
    """
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input("Enter your name or enter 'new' \
if you are a new member of staff: ")
        user = search(entered_name, "NAME", data)
        if user is not None:
            if authorise(user) is not True:
                continue
            break
        if entered_name.lower() == "new":
            user = create_staff()
            break
        print(f"Sorry, there is no user '{entered_name}'.")
        print("If you want to create a new user, enter 'new'.\n")

    return user


def start_menu(user):
    """
    Displays start menu after the user is logged in.
    """
    print(f"\nWhat do you want to do, {user['NAME']}?")
    while True:
        user_inp = input(
            "press 1 - Bookings\npress 2 - Customers\n\
press 3 - Staff info\npress x - Exit\n"
            )
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
        user_inp = input(
            "\n\tpress 1 - View bookings\n\
        press 2 - Add a booking\n\
        press 3 - Edit bookings\n\
        press x - <==\n\t")
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
        user_inp = input(
            "\n\tpress 1 - View a customer\n\
        press 2 - List of customers\n\
        press 3 - Stats\n\
        press x - <==\n\t")
        if user_inp == "1":
            user_inp = input("\n\tEnter name: ")
            view_customer(user_inp)
        elif user_inp == "2":
            view_customer("all")
        elif user_inp == "3":
            data_for_stats()
            customers_stats()
            print("\tYour stats is ready! Check your Google Drive folder.")
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
        user_inp = input(
            "\n\tpress 1 - Staff info\n\
        press 2 - Edit your info\n\
        press x - <==\n\t")
        if user_inp == "1":
            staff_info_menu(staff)
            continue
        if user_inp == "2":
            upd_staff = get_data("staff")  # new staff data if it got updated
            edit_staff_menu(upd_staff, user)
            continue
        if user_inp == "x":
            start_menu(user)
            break
        print("\tInvalid input. Please, use options above.")


def cleanup():
    """
    Deletes not needed files.
    """
    file = 'stats.csv'
    if os.path.exists(file):
        os.remove(file)


if __name__ == '__main__':
    staff = get_data("staff")
    the_user = staff_login(staff)
    print(f"{the_user['NAME']} : {the_user['CONTACT']}")
    start_menu(the_user)
