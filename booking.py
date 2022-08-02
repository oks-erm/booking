"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from spreadsheet import get_data, update_worksheet
from customer import pretty_print, get_customer


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


def view_bookings_menu():
    """
    Displays menu to choose bookings for what period
    you want to print. Accepts the user's choice.
    """
    bookings_data = get_data("bookings")
    tomorrow = change_date_format(str(date.today() + timedelta(days=1)))
    week = [today]
    for i in range(1, 7):
        week.append(change_date_format(str(date.today() + timedelta(days=i))))
    all_time = [dct['DATE'] for dct in bookings_data]    # change here!!!
    while True:
        user_inp = input("\n\t\tpress 1 - Today\n\t\tpress 2 - Tomorrow\n\
                press 3 - Next 7 days\n\t\tpress 4 - All\n\t\t")
        if user_inp == "1":
            print_bookings(bookings_data, today, "today")
            break
        if user_inp == "2":
            print_bookings(bookings_data, tomorrow, "tomorrow")
            break
        if user_inp == "3":
            print_bookings(bookings_data, week, "the upcoming week")
            break
        if user_inp == "4":
            print_bookings(bookings_data, all_time, "all time")
            break
        print("\t\tInvalid input! Use one of the options above")


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
{item['NAME']} ({item['PEOPLE']} ppl) added by {item['CREATED']} \
{confirmed(item)}")
        if string == "today" and item["CONF"] != "yes":
            print(f"\t!!! confirm this booking: \
{get_customer(item['NAME'])['PHONE']}\n")


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
    new = [new_date, new_time, name, ppl, created, "--"]
    update_worksheet(new, "bookings")
    increment_bookings(customer)
    print_bookings([dict(zip(KEYS, new))], new_date, "".join(new_date))


def increment_bookings(customer):
    pass


today = change_date_format(str(date.today()))
KEYS = get_data("bookings")[0]
