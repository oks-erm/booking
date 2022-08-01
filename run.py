"""
Main module, includes main logic flow and menus.
"""
import sys
import getpass
from datetime import date, timedelta
from staff import create_staff, print_staff_info
from spreadsheet import update_staff_data, get_data
from booking import change_date_format, print_bookings, new_booking
from customer import get_customer, search, view_customer


def authorise(name, data):
    """
    Checks the user's password
    """
    for i in range(4):
        print(f"Attempt {i+1} of 4")
        password = getpass.getpass("Password:")
        check_user = search(name, data)
        if check_user["PASSWORD"] == password:
            print("All good!\n")
            return True
        print("The password is not correct! Try again!\n")
        

def staff_login(data):
    """
    Logs in a member of staff
    """
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input(
            "Enter your name or enter 'new' if you are a new member of staff: "
        )
        names = [dct['NAME'] for dct in data]
        if entered_name in names:
            if authorise(entered_name, data) is not True:
                continue
            user = search(entered_name, data)
            break
        if entered_name.lower() == "new":
            user = create_staff()
            break
        print(f"Sorry, there is no user '{entered_name}'.")
        print("If you want to create a new user, enter 'new'\n")

    return user


def start_menu(user):
    """
    Displays start menu after the user is logged in
    """
    print(f"\nWhat do you want to do, {user.get('NAME')}?")
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
            sys.exit()

        print("Incorrect input. Please, choose 1,2 or 3\n")


def bookings_menu(user):
    """
    Displays booking menu
    """
    while True:
        user_inp = input(
            "\n\tpress 1 - View bookings\n\
        press 2 - Add a booking\n\
        press 3 - Edit a booking\n\
        press x - <==\n\t")
        if user_inp == "1":
            view_bookings_menu(user)
            break
        if user_inp == "2":
            user_inp = input("\n\tEnter customer's name: ")
            customer = get_customer(user_inp)
            new_booking(user, customer)
            break
        if user_inp == "3":
            # edit_booking()
            print("Edit")
            break
        if user_inp == "x":
            start_menu(user)
            break
        print("\tInvalid input. Use one of the options above")
    start_menu(user)


def view_bookings_menu(user):
    """
    Displays menu to choose bookings for what period
    you want to print. Accepts the user's choice.
    """
    bookings_data = get_data("bookings")[1:]
    today = change_date_format(str(date.today()))
    tomorrow = change_date_format(str(date.today() + timedelta(days=1)))
    week = [today]
    for i in range(1, 7):
        week.append(change_date_format(str(date.today() + timedelta(days=i))))
    all_time = [dct['DATE'] for dct in bookings_data]    # change here!!!
    while True:
        user_inp = input("\n\t\tpress 1 - Today\n\t\tpress 2 - Tomorrow\n\
                press 3 - Next 7 days\n\t\tpress 4 - All\n\t\t")
        if user_inp == "1":
            print_bookings(bookings_data, today, "today")
            break
        if user_inp == "2":
            print_bookings(bookings_data, tomorrow, "tomorrow")
            break
        if user_inp == "3":
            print_bookings(bookings_data, week, "the upcoming week")
            break
        if user_inp == "4":
            print_bookings(bookings_data, all_time, "all time")
            break
        print("\t\tInvalid input! Use one of the options above")
    bookings_menu(user)


def customers_menu(user):
    """
    Displays customers menu.
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
            # customers_stats()
            break
        elif user_inp == "x":
            start_menu(user)
            break
        else:
            print("\tInvalid input. Use one of the options above")
    start_menu(user)


def staff_menu(user):
    """
    Displays staff menu
    """
    while True:
        user_inp = input(
            "\n\tpress 1 - Staff info\n\
        press 2 - Edit your info\n\
        press x - <==\n\t")
        if user_inp == "1":
            staff_info_menu(staff, user)
            break
        if user_inp == "2":
            edit_staff_menu(user)
            break
        if user_inp == "x":
            start_menu(user)
            break
        print("\tInvalid input. Use one of the options above")


def staff_info_menu(staff_list, user):
    """
    Prints info about members of staff: search by name of a full list.
    """
    while True:
        print("\nEnter 'all' to see the full list")
        request = input("Or enter name to search by name: ")
        if request in [dct['NAME'] for dct in staff_list] or request == "all":
            print_staff_info(request, staff_list)
            break
        print("Nothing found, try again or view the full list")
    staff_menu(user)


def edit_staff_menu(user):
    """
    Edits instance of the current user. If the user wants
    to change a password or contact"
    """
    while True:
        user_inp = input("\t\tpress 1 - Change password\n\
                press 2 - Change contact\n\
                press x - <==\n\t\t")
        if user_inp == "1" or user_inp == "2":
            if user_inp == "2":
                attr = "CONTACT"
                new_value = input("\n\t\tEnter new contact: ")
            if user_inp == "1":
                attr = "PASSWORD"
                new_value = getpass.getpass("\n\t\tNew password: ")
            updated_user = update_staff_data(user, attr, new_value)
            for dict in staff:
                if dict["NAME"] == updated_user["NAME"]:
                    dict.update(updated_user)
            
            break
        if user_inp == "x":
            break
        print("\t\tInvalid input. Use one of the options above")
    staff_menu(user)


if __name__ == '__main__':
    staff = get_data("staff")
    the_user = staff_login(staff)
    print(f"{the_user['NAME']} : {the_user['CONTACT']}")
    start_menu(the_user)
