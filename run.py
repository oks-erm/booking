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
    except gspread.exceptions.WorksheetNotFound:
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
        return staff_data[1:]
    except gspread.exceptions.WorksheetNotFound:
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
    for item in staff:
        if name in item:
            user = item

    while True:
        password = getpass.getpass("Password:")
        if user[0] == name and user[1] == password:
            print("All good!\n")
            return user
        else:
            print("The password is not correct! Try again!\n")
            continue
        break


def staff_login():
    """
    Logs in a member of staff
    """
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input(
            "Enter your name or enter 'new' if you are a new member of staff: "
        )
        if entered_name in staff_names:
            # global current_user
            user = authorise(entered_name)
            if len(user) == 3:
                current_user = Staff(user[0], user[2])
                # print(current_user.describe())
                break
        elif entered_name.lower() == "new":
            create_staff()
            break
        else:
            print(f"Sorry, there is no user '{entered_name}'.")
            print("If you want to create a new user, enter 'new'\n")

    return current_user


def staff_info():
    """
    Prints info about members of staff: search by name of a full list.
    """
    while True:
        print("\nEnter 'all' to see the full list")
        request = input("Or enter name to search by name: ")
        if request == "all":
            for member in staff:
                print(f"\n{member[0]} : {member[2]}")
            break
        elif request in staff_names:
            i = staff_names.index(request)
            print(f"\n{staff[i][0]} : {staff[i][2]}")
            break
        print("Nothing found, try again or view the full list")


def start_menu(user):
    """
    Displays start menu after the user is logged in
    """
    print(f"What do you want to do, {user.name}?")
    while True:
        choose = input(
            "press 1 - Bookings\npress 2 - Customers\npress 3 - Staff info\n"
            )
        if choose == "1":
            # bookings_menu()
            print("Bookings")
            break
        elif choose == "2":
            # customers_menu()
            print("Customers")
            break
        elif choose == "3":
            staff_info()
            break
        
        print("Incorrect input. Please, choose 1,2 or 3\n")


staff = get_staff()
staff_names = [x[0] for x in staff]
the_user = staff_login()
start_menu(the_user)
