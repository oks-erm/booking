import sys
from google.oauth2.service_account import Credentials
import gspread


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CRED = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CRED)
SHEET = GSPREAD_CLIENT.open('My_booking')


def get_worksheet(worksheet):
    """
    Fetches staff data from Google Spreadsheet
    """
    try:
        data = SHEET.worksheet(worksheet).get_all_values()
        # data reorganised by columns
        return data[1:]
    except gspread.exceptions.GSpreadException:
        print("\nSorry, something went wrong accessing database.")
        inp = input("press 1 - Try again\npress x - Exit\n")
        if inp == "1":
            get_worksheet(worksheet)
        if inp == "x":
            sys.exit()


def update_worksheet(data, worksheet):
    """
    Writes data passed as an argument to a worksheet passed as an argument.
    """
    try:
        SHEET.worksheet(worksheet).append_row(data)
    except gspread.exceptions.GSpreadException:
        print("\nDatabase is not available, I couldn't save your data")
    else:
        print("Saved successfully!")


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
    print("\t\tStaff info was successfully updated!")