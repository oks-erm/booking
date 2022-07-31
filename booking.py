import re
from datetime import datetime
from spreadsheet import get_worksheet


bookings_data = get_worksheet("bookings")


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
        print('*' * 55)
        func(*args, **kwargs)
        print("*" * 55)
    return wrap_func


@pretty_print
def print_bookings(period, string):
    """
    Select bookings data out of given range and prints it.
    Accepts a period as a variable or list and a string to name 
    it in the output.
    """
    bookings = [x for x in bookings_data if x[0] == period or x[0] in period]
    bookings.sort(key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"))
    print(bookings)
    print(f"\tYou have {len(bookings)} booking(s) for {string}:\n")
    for item in bookings:
        print(f"\t{item[0]} {item[1]}: {item[2]} ({item[3]} people)")

