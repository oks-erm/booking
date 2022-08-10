"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from booking.spreadsheet import get_data, update_worksheet, update_data
from booking.customer import pretty_print, search, get_customer
from booking.validation import (to_date, validate_date_input,
                                validate_time_input)


def dd_mm_yyyy(my_date):
    """
    Changes date format from YYYY-MM-DD to DD-MM-YYYY.
    Returns date in the new format.
    """
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)


def active(data):
    """
    Filters out past and cancelled bookings.
    """
    filtered = [item for item in data if
                (to_date(item["DATE"]) >= date.today()) and
                (item["CANC"] != "yes")]
    return filtered


def confirmed(booking):
    """
    Checks if booking is confirmed and
    returns a corresponding symbol.
    """
    if booking["CONF"] == "yes":
        return "\\/"
    return "--"


def cust_bookings(name):
    """
    Selects all active bookings of a customer.
    """
    bookings = get_data("bookings")
    return [item for item in active(bookings) if item["NAME"] == name]


def view_bookings_menu():
    """
    Displays menu to choose bookings for what period
    you want to print. Accepts the user's choice.
    """
    bookings_data = active(get_data("bookings"))
    tomorrow = dd_mm_yyyy(str(date.today() + timedelta(days=1)))
    week = [today]
    for i in range(1, 7):
        week.append(dd_mm_yyyy(str(date.today() + timedelta(days=i))))
    all_time = [dct['DATE'] for dct in bookings_data]
    while True:
        user_inp = input("\n\t\tpress 1 - Today"
                         "\n\t\tpress 2 - Tomorrow"
                         "\n\t\tpress 3 - Next 7 days"
                         "\n\t\tpress 4 - All"
                         "\n\t\tpress x - <==\n\t\t")
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
    bookings = [bkng for bkng in data if
                (bkng["DATE"] == period or
                 bkng["DATE"] in period)]
    bookings.sort(key=lambda booking:
                  (datetime.strptime(booking["DATE"], "%d-%m-%Y"),
                   datetime.strptime(booking['TIME'], '%H:%M')))
    print(f"\tYou have {len(bookings)} booking(s) for {string}:\n")

    for item in bookings:
        print(f"\t{item['DATE'][:5]} - {item['TIME']} - "
              f"{item['NAME']} ({item['PEOPLE']} ppl) "
              f"added by {item['CREATED']} "
              f"{confirmed(item)}")
        if string == "today" and item["CONF"] != "yes":
            print(f"\t!!! confirm this booking: "
                  f"{get_customer(item['NAME'])['PHONE']}\n")


def new_booking(user, customer):
    """
    Creates a new booking acepting the user's
    input and writes it to the spreadsheet.
    """
    name = customer["NAME"]
    created = user["NAME"]
    while True:
        while True:
            new_date = input("\tEnter a booking date (dd-mm-yyyy): ")
            if new_date == "x":
                break
            valid_date = validate_date_input(new_date)
            if valid_date and check_duplicates(valid_date, name) is False:
                bookings = active(get_data("bookings"))
                print_bookings(bookings, valid_date, valid_date)
                break
            print(f"\tInvalid input: '{new_date}'.\n"
                  "\tPlease, enter a valid date.\n")
        if new_date == "x":
            break
        while True:
            new_time = input("\tNew time (hh:mm): ")
            if new_time == "x":
                break
            if validate_time_input(new_time) is True:
                break
            print(f"\tInvalid input: '{new_time}'.\n"
                  "\tPlease, enter valid time.\n")
        if new_time == "x":
            break
        ppl = input("\tHow many people: ")
        if ppl == "x":
            break
        new = [valid_date, new_time, name, ppl, created, "-", ""]
        update_worksheet(new, "bookings")
        increment_bookings(customer)
        print_bookings([dict(zip(KEYS, new))], valid_date, valid_date)
        break


def edit_bookings():
    """
    Displays Edit Bookings menu.
    """
    while True:
        bookings_data = active(get_data("bookings"))
        user_inp = input("\n\t\tpress 1 - Confirm"
                         "\n\t\tpress 2 - Reschedule"
                         "\n\t\tpress 3 - Cancel"
                         "\n\t\tpress x - <==\n\t\t")
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
            user_inp = input("\n\t\t\tpress 1 - Confirmed"
                             "\n\t\t\tpress 2 - Skip"
                             "\n\t\t\tpress 3 - Cancel"
                             "\n\t\t\tpress x - <==\n\t\t\t")
            if user_inp == "1":
                booking.update({"CONF": "yes"})
                update_data("bookings", booking, "CONF", "yes")
                break
            if user_inp == "2":
                break
            if user_inp == "3":
                cancel(booking)
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
        print("\n\t\t~ Enter 'x' at any point to go back ~\n")
        user_inp = input("\t\tEnter a customer's name: ")
        if user_inp == "x":
            break
        if user_inp in [dct["NAME"] for dct in customers]:
            bookings = cust_bookings(user_inp)
            all_time = [dct["DATE"] for dct in bookings]
            print_bookings(bookings, all_time, "all time")
            if len(bookings) == 0:
                break
            return pick_booking(bookings)

        print(f"\t\t\tCustomer '{user_inp}' does not exist. Try again.")


def pick_booking(bookings):
    """
    Picks one booking from the list based on
    user input.
    """
    target = None
    while True:
        user_date = input("\n\t\tDate of a booking to edit (dd-mm-yyyy): ")
        if user_date == "x":
            break
        valid_date = validate_date_input(user_date)
        if valid_date is False:
            print(f"\t\tInvalid input: '{user_date}'. "
                  "Please, enter a correct date.")
            continue
        target = search(valid_date, "DATE", bookings)
        if target is not None:
            break
        print(f"There are no bookings for {valid_date}.")
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
        while True:
            new_date = input("\t\tNew date (dd-mm-yyyy) "
                             "(leave empty if no change): ")
            if new_date == "x":
                break
            if ((validate_date_input(new_date) is True or new_date == "") and
                    check_duplicates(new_date, booking["NAME"]) is False):
                bookings = active(get_data("bookings"))
                if new_date != "":
                    print_bookings(bookings, new_date, new_date)
                else:
                    print_bookings(bookings, booking["DATE"], booking["DATE"])
                break
            print(f"\t\tInvalid input: '{new_date}'.\n"
                  "\t\tPlease, enter a valid date.\n")
        if new_date == "x":
            break
        while True:
            new_time = input("\t\tNew time (hh:mm): ")
            if new_time == "x":
                break
            if validate_time_input(new_time) is True:
                break
            print(f"\t\tInvalid input: '{new_time}'.\n"
                  "\t\tPlease, enter valid time.\n")
        if new_time == "x":
            break
        if new_date != "":
            update_data("bookings", booking, "DATE", new_date)
        update_data("bookings", booking, "TIME", new_time)
        break


def check_duplicates(user_date, name):
    """
    Checks if a customer already has a booking for
    this date.
    """
    customer_bookings = cust_bookings(name)
    if user_date in [dct["DATE"] for dct in customer_bookings]:
        print(f"\n\t!!!Booking for {user_date} already exists!!!")
        print_bookings(customer_bookings, user_date, user_date)
        return True
    return False


today = dd_mm_yyyy(str(date.today()))
KEYS = get_data("bookings")[0]
