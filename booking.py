"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from spreadsheet import get_data, update_worksheet
from customer import pretty_print, get_customer


KEYS = get_data("bookings")[0]


def change_date_format(my_date):
    """
    Changes date format from YYYY-MM-DD to DD-MM-YYYY
    """
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)


def confirmed(booking):
    """
    Checks if booking is confirmed and 
    returns a corresponding symbol.
    """
    if booking["CONF"] == "yes":
        return "\/"
    else:
        return "--"


@pretty_print
def print_bookings(data, period, string):
    """
    Select bookings data out of given range and prints it.
    Accepts an object defining time range and a string to name
    it in the output.
    """
    yesterday = date.today()-timedelta(days=1) 
    bookings = [x for x in data if (x["DATE"] == period or x["DATE"] in period)
                and (datetime.strptime(x["DATE"], "%d-%m-%Y").date()
                     > yesterday)]

    bookings.sort(key=lambda x: datetime.strptime(x["DATE"], "%d-%m-%Y"))
    print(f"\tYou have {len(bookings)} booking(s) for {string}:\n")
    for item in bookings:
        print(f"\t{item['DATE'][:5]} - {item['TIME']} - \
{item['CUSTOMER']} ({item['PEOPLE']} ppl) added by {item['CREATED']} \
{confirmed(item)}")
        if string == "today" and item["CONF"] != "yes":
            print(f"\t!!! confirm this booking: \
{get_customer(item['CUSTOMER'])['PHONE']}\n")


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
    print_bookings([dict(zip(KEYS, new))], new_date, "".join(new_date))
    return new
