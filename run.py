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


def write_new_staff_data(new_staff):
    """
    Writes the new user's data to the speadsheet
    """
    try:
        SHEET.worksheet('staf').append_row(new_staff)
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
    new_staff = [new_name, password, contact]
    write_new_staff_data(new_staff)
    return new_staff


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
    Checks user's password
    """
    for item in staff:
        if name in item:
            user = item

    while True:
        password = getpass.getpass("Password:")
        if user[0] == name and user[1] == password:
            print("All good!")
            return True
        else:
            print("The password is not correct! Try again!")
            continue
        break


def staff_login():
    """
    Logs in a member of staff
    """
    staff_names = [x[0] for x in staff]
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input(
            "Enter your name or enter 'new' if you are a new member of staff: "
        )
        if entered_name in staff_names:
            if authorise(entered_name):
                print(f"Hi, {entered_name}!")
                break
        elif entered_name.lower() == "new":
            create_staff()
            break
        else:
            print(f"Sorry, there is no user '{entered_name}'.")
            print("If you want to create a new user, enter 'new'\n")


staff = get_staff()
staff_login()
print("Move on")