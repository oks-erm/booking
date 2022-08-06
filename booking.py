"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from spreadsheet import get_data, update_worksheet, update_data
from customer import pretty_print, search, get_customer


def change_date_format(my_date):
    """
    Changes date format from YYYY-MM-DD to DD-MM-YYYY.
    """
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)


def to_date(string):
    """
    Converts string date data to date format.
    """
    return datetime.strptime(string, "%d-%m-%Y").date()


def active(data):
    """
    Filters out past and cancelled bookings.
    """
    filtered = [item for item in data
                if (to_date(item["DATE"]) >= date.today())
                and (item["CANC"] != "yes")]
    return filtered


def confirmed(booking):
    """
    Checks if booking is confirmed and
    returns a corresponding symbol.
    """
    if booking["CONF"] == "yes":
        return "\\/"
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
        print("\t\tInvalid input. Please, use options above.")


@pretty_print
def print_bookings(data, period, string):
    """
    Select bookings data out of given range and prints it.
    Accepts an object defining time range and a string to name
    it in the output.
    """
    bookings = [bkng for bkng in active(data)
                if (bkng["DATE"] == period or bkng["DATE"] in period)]

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
    while True:
        new_date = input("\n\tEnter a booking date (dd-mm-yyyy): ")
        if validate_date_input(new_date) is True:
            break
        print(f"\t\tInvalid input: '{new_date}'.\n\
                Please, enter a correct date.")

    new_time = input("\tEnter time (hh:mm): ")
    ppl = input("\tHow many people: ")
    new = [new_date, new_time, name, ppl, created, "-", ""]
    update_worksheet(new, "bookings")
    increment_bookings(customer)
    print_bookings([dict(zip(KEYS, new))], new_date, "".join(new_date))


def edit_bookings():
    """
    Displays Edit Bookings menu.
    """
    while True:
        bookings_data = get_data("bookings")
        user_inp = input(
            "\n\t\tpress 1 - Confirm\n\
                press 2 - Reschedule\n\
                press 3 - Cancel\n\
                press x - <==\n\t\t")
        if user_inp == "1":
            not_confirmed = ([item for item in bookings_data if (item["CONF"]
                             != "yes" and item["DATE"] == today)])
            if len(not_confirmed) == 0:
                print("\n\t\tAll bookings are confirmed! Chill!")
            confirm(not_confirmed)
            continue
        if user_inp == "2":
            booking = find_bookings(bookings_data)
            if booking is None:
                continue
            reschedule(booking)
            continue
        if user_inp == "3":
            booking = find_bookings(bookings_data)
            if booking is None:
                continue
            cancel(booking)
            continue
        if user_inp == "x":
            break
        print("\t\tInvalid input. Please, use options above.")


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
            print("\t\t\tInvalid input. Please, use options above.")
        if user_inp == "x":
            break


def increment_bookings(customer):
    """
    Increments number of bookings a customer has, when
    a new booking is created.
    """
    new_number = str(int(customer["NUM OF BOOKINGS"]) + 1)
    update_data("customers", customer, "NUM OF BOOKINGS", new_number)


def find_bookings(bookings):
    """
    Finda and returns all bookings of a customer,
    accepts user input with a name to search.
    """
    customers = get_data("customers")
    while True:
        print("\n\t\t\tpress x - <==")
        user_inp = input("\n\t\t\tEnter a customer's name: ")
        if user_inp == "x":
            break
        if user_inp in [dct["NAME"] for dct in customers]:
            cust_bookings = ([item for item in active(bookings)
                             if item["NAME"] == user_inp])
            all_time = [dct["DATE"] for dct in cust_bookings]
            print_bookings(cust_bookings, all_time, "all time")
            if len(cust_bookings) == 0:
                break
            return pick_booking(cust_bookings)

        print(f"\t\t\tCustomer '{user_inp}' does not exist. Try again.")


def pick_booking(bookings):
    """
    Picks one booking from the list based on
    user input.
    """
    target = None
    while True:
        user_inp = input("\n\t\tpress x - <==\n\
                Date of a booking to edit (dd-mm-yyyy): ")
        if user_inp == "x":
            break
        if validate_date_input(user_inp) is False:
            print(f"\t\tInvalid input: '{user_inp}'.\n\
                Please, enter a correct date.")
            continue
        target = search(user_inp, "DATE", bookings)
        if target is not None:
            break
        print(f"There are no bookings for {user_inp}")
    return target


def cancel(booking):
    """
    Updates bookings spreadsheet with new booking status
    and increments the customer's stats of cancelled bookings.
    """
    update_data("bookings", booking, "CANC", "yes")
    customer = get_customer(booking["NAME"])
    new_value = str(int(customer["CANCELLED"]) + 1)
    update_data("customers", customer, "CANCELLED", new_value)


def reschedule(booking):
    """
    Updates booking data about date or time.
    """
    while True:
        new_date = input("\n\t\tNew date (dd-mm-yyyy)\
(leave empty if no change): ")
        if validate_date_input(new_date) is True:
            break
        print(f"\t\tInvalid input: '{new_date}'.\n\
                Please, enter a correct date.")
    new_time = input("\t\tNew time (hh:mm): ")
    if new_date != "":
        update_data("bookings", booking, "DATE", new_date)
    update_data("bookings", booking, "TIME", new_time)


def validate_date_input(inp):
    """
    Validates if date is correct dd-mm-yyyy format and
    it's not from the past.
    """
    try:
        if inp != (datetime.strptime(inp, "%d-%m-%Y").strftime("%d-%m-%Y")
                   or to_date(inp) < date.today()):
            raise ValueError
        return True
    except ValueError:
        return False


today = change_date_format(str(date.today()))
KEYS = get_data("bookings")[0]
