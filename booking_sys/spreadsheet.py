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
    Fetches staff data from Google Spreadsheet
    """
    try:
        data = SHEET.worksheet(worksheet).get_all_values()
        # data reorganised by columns
        return data
    except (gspread.exceptions.GSpreadException, gspread.exceptions.APIError):
        print("\nSorry, something went wrong accessing database.")
        user_input = input("press 1 - Try again\npress x - Exit\n")
        if user_input == "1":
            get_worksheet(worksheet)
        if user_input == "x":
            sys.exit()


def update_worksheet(data, worksheet):
    """
    Writes data passed as an argument to a worksheet passed as an argument.
    """
    try:
        SHEET.worksheet(worksheet).append_row(data)
    except (gspread.exceptions.GSpreadException, gspread.exceptions.APIError):
        print("\nDatabase is not available, I couldn't save your data")
        user_input = input("press 1 - Try again\n"
                           "press x - Continue without saving\n")
        if user_input == "1":
            update_worksheet(data, worksheet)
        if user_input == "x":
            pass
    else:
        print("\n\t\tSaved successfully!\n")


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
    Updates attributes of instance of Staff and
    writes updates to spreadsheet. Takes three
    arguments: (object to update, attribute to update,
    new value)).
    """
    row = SHEET.worksheet(worksheet).find(obj["NAME"]).row
    col = SHEET.worksheet(worksheet).find(attr).col
    if worksheet == "bookings":
        cell_list = SHEET.worksheet(worksheet).findall(obj["NAME"])
        rows = [cell.row for cell in cell_list]
        for r in rows:
            if obj["DATE"] in SHEET.worksheet(worksheet).row_values(r):
                row = r
    SHEET.worksheet(worksheet).update_cell(row, col, ("'"+value))
    print(f"\t\t{worksheet.capitalize()} info was successfully updated!")
    obj[attr] = value
    return obj
