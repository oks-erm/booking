"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from spreadsheet import get_data, update_worksheet, update_data
from customer import pretty_print, get_customer


def change_date_format(my_date):
    """
    Changes date format from YYYY-MM-DD to DD-MM-YYYY
    """
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)


def to_date(string):
    """
    Converts string date data to date format.
    """
    return datetime.strptime(string, "%d-%m-%Y").date()


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
    all_time = [dct['DATE'] for dct in bookings_data] 
    while True:
        user_inp = input("\n\t\tpress 1 - Today\n\
                press 2 - Tomorrow\n\
                press 3 - Next 7 days\n\
                press 4 - All\n\t\tpress x - <==\n\t\t")
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
        if user_inp == "x":
            break
        print("\t\tInvalid input! Use one of the options above")


@pretty_print
def print_bookings(data, period, string):
    """
    Select bookings data out of given range and prints it.
    Accepts an object defining time range and a string to name
    it in the output.
    """
    bookings = [x for x in data if (x["DATE"] == period or x["DATE"] in period)
                and (to_date(x["DATE"]) >= date.today())]

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
    new = [new_date, new_time, name, ppl, created, "-"]
    update_worksheet(new, "bookings")
    increment_bookings(customer)
    print_bookings([dict(zip(KEYS, new))], new_date, "".join(new_date))


def edit_bookings():
    """
    Displays Edit Bookings menu.
    """
    while True:
        user_inp = input(
            "\n\t\tpress 1 - Confirm\n\
                press 2 - Reschedule\n\
                press 3 - Cancel\n\
                press x - <==\n\t\t")
        if user_inp == "1":
            bookings_data = get_data("bookings")
            not_confirmed = ([item for item in bookings_data if (item["CONF"]
                             != "yes" and item["DATE"] == today)])
            if len(not_confirmed) == 0:
                print("\n\t\tAll bookings are confirmed! Chill!")
            confirm(not_confirmed)
            continue
        if user_inp == "2":
            # reschedule()
            continue
        if user_inp == "3":
            # cancel()
            continue
        if user_inp == "x":
            break
        print("\t\tInvalid input. Use one of the options above")


def confirm(bookings):
    """
    Finds not confirmed bookings and prints them
    with contact numbers one by one to confirm or
    skip.
    """
    for booking in bookings:
        while True:
            print_bookings([booking], today, "today")
            user_inp = input("\n\t\t\tpress 1 - Confirmed\n\
                        press 2 - Skip\n\t\t\tpress x - <==\n\t\t\t")
            if user_inp == "1":
                booking.update({"CONF": "yes"})
                update_data("bookings", booking, "CONF", "yes")
                break
            if user_inp == "2":
                break
            if user_inp == "x":
                break
            print("\t\t\tInvalid input! Use one of the options above")
        if user_inp == "x":
            break


def increment_bookings(customer):
    """
    Increments number of bookings a customer has, when
    a new booking is created.
    """
    new_number = int(customer.get("NUM OF BOOKINGS")) + 1
    update_data("customers", customer, "NUM OF BOOKINGS", str(new_number))


def find_bookings(bookings):
    """
    Find all bookings of a customer,
    accepts user input with a name to search.
    """
    user_inp = input("\n\t\t\tEnter customer's name: ")
    customers_bookings = ([item for item in bookings if (item["NAME"]
                          == user_inp and to_date(item["DATE"]) >= today)])
    all_time = [dct['DATE'] for dct in customers_bookings
                if to_date(dct['DATE']) >= date.today()]
    print_bookings(customers_bookings, all_time, "all time")


today = change_date_format(str(date.today()))
KEYS = get_data("bookings")[0]
