import getpass
from staff import Staff, create_staff, staff_data
from spreadsheet import change_staff_attr


def authorise(name, data_list):
    """
    Checks the user's password
    """
    idx = data_list[0].index(name)
    for i in range(4):
        print(f"Attempt {i+1} of 4")
        password = getpass.getpass("Password:")
        if data_list[0][idx] == name and data_list[1][idx] == password:
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
        if entered_name in data[0]:
            if authorise(entered_name, data) is not True:
                continue
            current_user = Staff(
                entered_name, data[2][data[0].index(entered_name)]
                )
            break
        if entered_name.lower() == "new":
            current_user = create_staff()
            break
        print(f"Sorry, there is no user '{entered_name}'.")
        print("If you want to create a new user, enter 'new'\n")

    return current_user


def start_menu(user):
    """
    Displays start menu after the user is logged in
    """
    print(f"\nWhat do you want to do, {user.name}?")
    while True:
        user_inp = input(
            "press 1 - Bookings\npress 2 - Customers\npress 3 - Staff info\n"
            )
        if user_inp == "1":
            bookings_menu(user)
            break
        if user_inp == "2":
            # customers_menu()
            print("Customers")
            break
        if user_inp == "3":
            staff_menu(user)
            break

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
            # view_bookings()
            print("View")
            break
        if user_inp == "2":
            # new_booking()
            print("Add")
            break
        if user_inp == "3":
            # edit_booking()
            print("Edit")
            break
        if user_inp == "x":
            start_menu(user)
            break
        print("\tInvalid input. Use one of the options above")


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
            staff_info_menu(all_staff, user)
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
        if request == "all":
            for i in range(len(staff_list[0])):
                print(f"\n{staff_list[0][i]} : {staff_list[2][i]}")
            break
        if request in staff_list[0]:
            i = staff_list[0].index(request)
            print(f"\n{staff_list[0][i]} : {staff_list[2][i]}")
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
            change_staff_attr(user, attr, new_value)
            break
        if user_inp == "x":
            break
        print("\t\tInvalid input. Use one of the options above")
    staff_menu(user)


all_staff = staff_data()
print(all_staff)
the_user = staff_login(all_staff)
print(the_user.describe())
start_menu(the_user)

