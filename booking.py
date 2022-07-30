import re
from datetime import date
from spreadsheet import get_worksheet


bookings_data = get_worksheet("bookings")


def change_date_format(my_date):
    """
    ...
    """
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)


def pretty_print(func):
    def wrap_func(*args, **kwargs):
        print('*' * 55)
        func(*args, **kwargs)
        print("*" * 55)
    return wrap_func


@pretty_print
def view_bookings(user_input):
    """
    ...
    """
    if user_input == "1":
        today = change_date_format(str(date.today()))
        today_bookings = [x for x in bookings_data if x[0] == today]
        print(f"\tYou have {len(today_bookings)} booking(s) today {today}:\n")
        for item in today_bookings:
            print(f"\t{item[1]}: {item[2]} ({item[3]} people)")
    