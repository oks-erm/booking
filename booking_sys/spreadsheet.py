"""
Includes functions related to interactions with Goggle Spreadsheets API.
"""
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
    Fetches staff data from Google Spreadsheet. Returns
    a list of dictionaries.
    """
    try:
        data = SHEET.worksheet(worksheet).get_values()
        if data is None:
            raise ValueError
        return data
    except (gspread.exceptions.GSpreadException, gspread.exceptions.APIError,
            gspread.exceptions.WorksheetNotFound, ValueError, TypeError):
        print("\nSorry, something went wrong accessing database.")
        user_input = input("press 1 - Try again\npress x - Exit\n")
        if user_input == "1":
            print("Trying...")
            get_worksheet(worksheet)
        if user_input == "x":
            sys.exit()


def update_worksheet(data, worksheet):
    """
    Writes data passed as an argument to a worksheet
    passed as an argument.
    """
    try:
        SHEET.worksheet(worksheet).append_row(data)
    except (gspread.exceptions.GSpreadException, gspread.exceptions.APIError,
            gspread.exceptions.WorksheetNotFound):
        print("\nDatabase is not available, I couldn't save your data")
        user_input = input("press 1 - Try again\n"
                           "press x - Continue without saving\n")
        if user_input == "1":
            print("Trying...")
            update_worksheet(data, worksheet)
        if user_input == "x":
            print("Your data was not saved.")
    else:
        print("\n\t\tSaved successfully!")


def get_data(worksheet):
    """
    Creates a list of dictionaries from data.
    """
    response = get_worksheet(worksheet)
    keys = response[0]
    data = []
    for item in response[1:]:
        data.append(dict(zip(keys, item)))
    return data


def update_data(worksheet, obj, attr, value):
    """
    Updates values of given objects on given worksheet.
    Takes three arguments: (object to update, attribute to update,
    new value).
    """
    try:
        row = SHEET.worksheet(worksheet).find(obj["NAME"]).row
        col = SHEET.worksheet(worksheet).find(attr).col
        if worksheet == "bookings":
            cell_list = SHEET.worksheet(worksheet).findall(obj["NAME"])
            # find a row
            rows = [cell.row for cell in cell_list]
            for r in rows:
                if obj["DATE"] in SHEET.worksheet(worksheet).row_values(r):
                    row = r
        SHEET.worksheet(worksheet).update_cell(row, col, ("'"+value))
        print(f"\t\t{worksheet.capitalize()}({attr}) info was "
              "successfully updated!")
        obj[attr] = value
        return obj
    except (gspread.exceptions.GSpreadException, gspread.exceptions.APIError,
            gspread.exceptions.WorksheetNotFound):
        print("\nDatabase is not available, I couldn't save your data")
        user_input = input("press 1 - Try again\n"
                           "press x - Continue without saving\n")
        if user_input == "1":
            print("Trying...")
            update_data(worksheet, obj, attr, value)
        if user_input == "x":
            print("Your data was not saved.")
