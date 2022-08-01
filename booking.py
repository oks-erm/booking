"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from spreadsheet import get_data, update_worksheet


KEYS = get_data("bookings")[0]


def change_date_format(my_date):
    """
    Changes date format from YYYY-MM-DD to DD-MM-YYYY
    """
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)


def pretty_print(func):
    """
    Frames print output with lines of * symbol.
    """
    def wrap_func(*args, **kwargs):
        print('*' * 65)
        func(*args, **kwargs)
        print("*" * 65)
    return wrap_func


@pretty_print
def print_bookings(data, period, string):
    """
    Select bookings data out of given range and prints it.
    Accepts an object defining time range and a string to name
    it in the output.
    """
    # upd_bookings = get_data("bookings")[1:]
    yesterday = date.today()-timedelta(days=1) 
    bookings = [x for x in data if (x["DATE"] == period or x["DATE"] in period)
                and (datetime.strptime(x["DATE"], "%d-%m-%Y").date()
                     > yesterday)]

    bookings.sort(key=lambda x: datetime.strptime(x["DATE"], "%d-%m-%Y"))
    print(f"\tYou have {len(bookings)} booking(s) for {string}:\n")
    for item in bookings:
        print(f"\t{item['DATE'][:5]} - {item['TIME']} - \
{item['CUSTOMER']} ({item['PEOPLE']} ppl) added by {item['CREATED']}")


def new_booking(user, customer):
    """
    Creates a new booking acepting the user's
    input and writes it to the spreadsheet.
    """
    name = customer["NAME"]
    created = user["NAME"]
    new_date = input("\n\tEnter booking date in dd-mm-yyyy format: ")
    new_time = input("\tEnter date in hh:mm format: ")
    ppl = input("\tHow many people: ")
    new = [new_date, new_time, name, ppl, created]
    update_worksheet(new, "bookings")
    return new

