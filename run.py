import gspread
import getpass
from google.oauth2.service_account import Credentials

# constant variables for google spreadsheet api
SCOPE = [ 
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CRED = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CRED)
SHEET = GSPREAD_CLIENT.open('My_booking')


class Staff:
    """
    Creates instance of Staff
    """
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

    def describe(self):
        """
        Prints info about a member of staff
        """
        return f"User: {self.name}, contact: {self.contact}\n"


def update_worksheet(data, worksheet):
    """
    Writes data passed as an argument to a worksheet passed as an argument.
    """
    SHEET.worksheet(worksheet).append_row(data)


def write_new_staff_data(new_staff):
    """
    Writes the new user's data to the speadsheet
    """
    try:
        update_worksheet(new_staff, "staff")
    except gspread.exceptions.GSpreadException:
        print(
            f"\nDatabase is not available, I couldn't save user {new_staff[0]}"
            )
        print("You can continue, but you will need to create this user again")


def create_staff():
    """
    Creates a new member of Staff
    """
    new_name = input("Enter a name for a new member of staff:\n")
    print(f"Hi, {new_name}!")
    password = getpass.getpass("Create a password:")
    contact = input("Awesome! Enter your contact number:")
    write_new_staff_data([new_name, password, contact])
    return Staff(new_name, contact)


def get_staff():
    """
    Fetches staff data from Google Spreadsheet
    """
    try:
        staff_data = SHEET.worksheet('staff').get_all_values()
        # data reorganised by columns
        return [[row[i] for row in staff_data[1:]] for i in range(3)]
    except gspread.exceptions.GSpreadException:
        print("Sorry, something went wrong accessing database")
        yes_or_no = input("press 1 - Try again?\npress 2 - Enter as new\n")
        if yes_or_no == "1":
            get_staff()
        else:
            create_staff()


def authorise(name):
    """
    Checks the user's password
    """
    idx = staff[0].index(name)
    for i in range(4):
        print(f"Attempt {i+1} of 4")
        password = getpass.getpass("Password:")
        if staff[0][idx] == name and staff[1][idx] == password:
            print("All good!\n")
            return True
        print("The password is not correct! Try again!\n")


def staff_login():
    """
    Logs in a member of staff
    """
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input(
            "Enter your name or enter 'new' if you are a new member of staff: "
        )
        if entered_name in staff[0]:
            if authorise(entered_name) is not True:
                continue
            current_user = Staff(entered_name, staff[2][staff[0].index(entered_name)])
            break
        if entered_name.lower() == "new":
            current_user = create_staff()
            break
        print(f"Sorry, there is no user '{entered_name}'.")
        print("If you want to create a new user, enter 'new'\n")

    return current_user


def staff_menu():
    """
    Displays staff menu
    """
    while True:
        user_inp = input(
            "\n\tpress 1 - Staff info\n\
        press 2 - Edit your info\n\
        press x - <==\n\t")
        if user_inp == "1":
            staff_info()
            break
        if user_inp == "2":
            edit_staff(the_user)
            break
        if user_inp == "x":
            start_menu(the_user)
            break


def staff_info():
    """
    Prints info about members of staff: search by name of a full list.
    """
    while True:
        print("\nEnter 'all' to see the full list")
        request = input("Or enter name to search by name: ")
        if request == "all":
            for i in range(len(staff[0])):
                print(f"\n{staff[0][i]} : {staff[2][i]}")
            break
        if request in staff[0]:
            i = staff[0].index(request)
            print(f"\n{staff[0][i]} : {staff[2][i]}")
            break
        print("Nothing found, try again or view the full list")
    staff_menu()


def edit_staff(user):
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
                new_value = input("\nEnter new contact: ")
            if user_inp == "1":
                attr = "PASSWORD"
                new_value = getpass.getpass("\nNew password: ")
            change_staff_attr(user, attr, new_value)
            break
        if user_inp == "x":
            staff_menu()
            break


def change_staff_attr(user, attr, value):
    """
    Updates attributes of instance of Staff and
    writes updates to spreadsheet. Takes three
    arguments: (object to update, attribute to update,
    new value)).
    """
    setattr(user, attr, value)
    row = SHEET.worksheet('staff').find(user.name).row
    col = SHEET.worksheet('staff').find(attr).col
    SHEET.worksheet('staff').update_cell(row, col, ("'"+value))


def bookings_menu():
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
            start_menu(the_user)
            break
        print("\tInvalid input. Use one of the options above")


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
            bookings_menu()
            break
        if user_inp == "2":
            # customers_menu()
            print("Customers")
            break
        if user_inp == "3":
            staff_menu()
            break

        print("Incorrect input. Please, choose 1,2 or 3\n")


staff = get_staff()
print(staff)
the_user = staff_login()
print(the_user.describe())
start_menu(the_user)
