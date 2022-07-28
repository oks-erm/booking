import gspread
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


def create_staff():
    """
    Creates a new member of Staff
    """
    new_name = input("Enter a name for a new member of staff:\n")
    print(f"Hi, {new_name}!")


def get_staff():
    """
    Fetches staff data from Google Spreadsheet
    """
    try:
        staff_data = SHEET.worksheet('staff').get_all_values()
        staff = [x[0] for x in staff_data[1:]]
        return staff
    except gspread.exceptions.WorksheetNotFound:
        print("Sorry, something went wrong accessing database")
        yes_or_no = input("press 1 - Try again?\npress 2 - Enter as new\n")
        if yes_or_no == "1":
            get_staff()
        else:
            create_staff()      


def validate_user(name):
    return True


def staff_login():
    """
    Logs in a member of staff
    """
    staff = get_staff()
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input(
            "Enter your name or enter 'new' if you are a new member of staff: "
        )
        if entered_name in staff:
            if validate_user(entered_name):
                print(f"Hi, {entered_name}!")
                break
        elif entered_name.lower() == "new":
            create_staff()
            break
        else:
            print(f"Sorry, there is no user '{entered_name}'.")
            print("If you want to create a new user, enter 'new'\n")


staff_login()
print("Move on")