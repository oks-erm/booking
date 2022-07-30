import re
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
    """
    bookings = [x for x in bookings_data if x[0] == period or x[0] in period]
    print(f"\tYou have {len(bookings)} booking(s) for {string}:\n")
    for item in bookings:
        print(f"\t{item[0]} {item[1]}: {item[2]} ({item[3]} people)")

