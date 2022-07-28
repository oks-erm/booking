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
    print("New")


def get_staff():
    """
    Fetches staff data from Google Spreadsheet
    """
    try:
        staff_data = SHEET.worksheet('staff').get_all_values()
        staff = [x[0] for x in staff_data[1:]]
        print(staff)
    except gspread.exceptions.WorksheetNotFound:
        print("Sorry, something went wrong accessing database")
        yes_or_no = input("press 1 - Try again?\npress 2 - Enter as new\n")
        if yes_or_no == "1":
            get_staff()
        else:
            create_staff()      


get_staff()