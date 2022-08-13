"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from booking_sys import spreadsheet as spsheet
from booking_sys import customer as cust
from booking_sys import validation as valid
import run


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
                (valid.to_date(item["DATE"]) >= date.today()) and
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
    bookings = spsheet.get_data("bookings")
    return [item for item in active(bookings) if item["NAME"] == name]


def bookings_menu(user):
    """
    Displays booking menu
    """
    while True:
        user_inp = input("\n\tpress x - <==\n"
                         "\tpress 1 - View bookings\n"
                         "\tpress 2 - Add a booking\n"
                         "\tpress 3 - Edit bookings\n\t")
        if user_inp == "1":
            view_bookings_menu(user)
            continue
        if user_inp == "2":
            customer = cust.find_customer(user)
            if customer is None:
                continue
            new_booking(user, customer)
            continue
        if user_inp == "3":
            edit_bookings(user)
            continue
        if user_inp == "x":
            run.start_menu(user)
            break
        print("\tInvalid input. Please, use options above.")
    return True


@run.loop_menu_qx("\t\t",
                  "x - <== // q - home",
                  "\t\tpress 1 - Today\n"
                  "\t\tpress 2 - Tomorrow\n"
                  "\t\tpress 3 - Next 7 days\n"
                  "\t\tpress 4 - All\n\t\t",
                  "Invalid input. Please, use options above.")
def view_bookings_menu(*args):
    """
    Displays menu to choose bookings for what period
    you want to print. Accepts the user's choice.
    """
    # get the latest bookings data
    bookings_data = active(spsheet.get_data("bookings"))
    # time periods
    tomorrow = dd_mm_yyyy(str(date.today() + timedelta(days=1)))
    week = [today]
    for i in range(1, 7):
        week.append(dd_mm_yyyy(str(date.today() + timedelta(days=i))))
    all_time = [dct['DATE'] for dct in bookings_data]
    #  unpack args
    user_input, user = (args)

    if user_input == "1":
        print_bookings(bookings_data, today, "today")
    elif user_input == "2":
        print_bookings(bookings_data, tomorrow, "tomorrow")
    elif user_input == "3":
        print_bookings(bookings_data, week, "the upcoming week")
    elif user_input == "4":
        print_bookings(bookings_data, all_time, "all time")
    else:
        return user
    return True


@cust.pretty_print
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
                  f"{cust.get_customer(item['NAME'])['PHONE']}\n")


@run.loop_menu_qx("\t",
                  "",
                  "\tEnter a booking date (dd-mm-yyyy): ",
                  "Invalid date.")
def new_date(*args):
    """
    Accepts user input and validates date,
    checking if it's correect format, not from the past
    and a customer doesn't have duplicate bookings for
    the same date.
    """
    user_input, customer, user = (args)
    valid_date = valid.date_input(user_input)
    if valid_date and has_duplicates(valid_date, customer["NAME"]) is False:
        bookings = active(spsheet.get_data("bookings"))
        print_bookings(bookings, valid_date, valid_date)
        return valid_date
    return user


@run.loop_menu_qx("\t",
                  "",
                  "\tNew time (hh:mm): ",
                  "Invalid time.")
def new_time(*args):
    """
    Accepts user input and validates time,
    checking if it's correect format.
    """
    user_input, user = (args)
    if valid.time_input(user_input) is True:
        return user_input
    return user


@run.loop_menu_qx("\t",
                  "",
                  "\tHow many people: ",
                  "Not a number. Please, use a number.")
def num_of_people(*args):
    """
    Accepts number of people, validates that
    it is a number.
    """
    user_input, user = (args)
    try:
        num = int(user_input)
    except ValueError:
        return user
    else:
        return num


def new_booking(user, customer):
    """
    Creates a new booking acepting the user's
    input and writes it to the spreadsheet.
    """
    name = customer["NAME"]
    created = user["NAME"]
    while True:
        date = new_date(customer, user)
        if date is None:
            break
        time = new_time(user)
        if time is None:
            break
        num = num_of_people(user)
        if num is None:
            break
        new = [date, time, name, num, created, "-", ""]
        spsheet.update_worksheet(new, "bookings")
        increment_bookings(customer)
        print_bookings([dict(zip(KEYS, new))], date, date)
        break


def edit_bookings(user):
    """
    Displays Edit Bookings menu.
    """
    while True:
        bookings_data = active(spsheet.get_data("bookings"))
        user_inp = input("\n\t\tx - <== // q - home"
                         "\n\t\tpress 1 - Confirm"
                         "\n\t\tpress 2 - Reschedule"
                         "\n\t\tpress 3 - Cancel\n\t\t")
        if user_inp == "1":
            not_confirmed = ([item for item in bookings_data if (item["CONF"]
                             != "yes" and item["DATE"] == today)])
            if len(not_confirmed) == 0:
                print("\n\t\tAll bookings are confirmed! Chill!")
            confirm(not_confirmed, user)
            continue
        if user_inp == "2":
            booking = find_bookings(user)
            if booking is None:
                continue
            reschedule(booking, user)
            continue
        if user_inp == "3":
            booking = find_bookings(user)
            if booking is None:
                continue
            cancel(booking)
            continue
        if user_inp == "x":
            break
        if user_inp == "q":
            run.start_menu(user)
        print("\t\tInvalid input. Please, use options above.")


def confirm(bookings, user):
    """
    Finds not confirmed bookings and prints them
    with contact numbers one by one to confirm or
    skip.
    """
    for booking in bookings:
        while True:
            print_bookings([booking], today, "today")
            user_inp = input("\n\t\t\tx - <== // q - home"
                             "\n\t\t\tpress 1 - Confirmed"
                             "\n\t\t\tpress 2 - Skip"
                             "\n\t\t\tpress 3 - Cancel\n\t\t\t")
            if user_inp == "1":
                booking.update({"CONF": "yes"})
                spsheet.update_data("bookings", booking, "CONF", "yes")
                break
            if user_inp == "2":
                break
            if user_inp == "3":
                cancel(booking)
                break
            if user_inp == "x":
                break
            if user_inp == "q":
                run.start_menu(user)
            print("\t\t\tInvalid input. Please, use options above.")
        if user_inp == "x":
            break


def increment_bookings(customer):
    """
    Increments number of bookings a customer has, when
    a new booking is created.
    """
    new_number = str(int(customer["NUM OF BOOKINGS"]) + 1)
    spsheet.update_data("customers", customer, "NUM OF BOOKINGS", new_number)


@run.loop_menu_qx("\t\t",
                  "~ ~ x - <== // q - home ~ ~",
                  "\t\tEnter a customer's name: ",
                  "Computer says no. Customer does not exist.")
def find_bookings(*args):
    """
    Finds and returns all bookings of a customer,
    accepts user input with a name to search.
    """
    customers = spsheet.get_data("customers")
    user_input, user = (args)
    if user_input in [dct["NAME"] for dct in customers]:
        bookings = cust_bookings(user_input)
        all_time = [dct["DATE"] for dct in bookings]
        print_bookings(bookings, all_time, "all time")
        if len(bookings) == 0:
            return None
        return [pick_booking(bookings, user)]
    return user


def pick_booking(bookings, user):
    """
    Picks one booking from the list based on
    user input.
    """
    target = None
    while True:
        user_date = input("\n\t\tDate of a booking to edit (dd-mm-yyyy): ")
        if user_date == "x":
            break
        if user_date == "q":
            run.start_menu(user)
        valid_date = valid.date_input(user_date)
        if valid_date is False:
            print(f"\t\tInvalid input: '{user_date}'. "
                  "Please, enter a correct date.")
            continue
        target = cust.search(valid_date, "DATE", bookings)
        if target is not None:
            break
        print(f"There are no bookings for {valid_date}.")
    return target


def cancel(booking):
    """
    Updates bookings spreadsheet with new booking status
    and increments the customer's stats of cancelled bookings.
    """
    spsheet.update_data("bookings", booking, "CANC", "yes")
    customer = cust.get_customer(booking["NAME"])
    new_value = str(int(customer["CANCELLED"]) + 1)
    spsheet.update_data("customers", customer, "CANCELLED", new_value)


def reschedule(booking, user):
    """
    Updates booking data about date or time.
    """
    while True:
        while True:
            user_date = input("\t\tNew date (dd-mm-yyyy) "
                              "(leave empty if no change): ")
            if user_date in ["x", "q"]:
                break
            if ((valid.date_input(user_date) is True or user_date == "") and
                    has_duplicates(user_date, booking["NAME"]) is False):
                bookings = active(spsheet.get_data("bookings"))
                if user_date != "":
                    print_bookings(bookings, user_date, user_date)
                else:
                    print_bookings(bookings, booking["DATE"], booking["DATE"])
                break
            print(f"\t\tInvalid input: '{user_date}'.\n"
                  "\t\tPlease, enter a valid date.\n")
        if user_date == "x":
            break
        if user_date == "q":
            run.start_menu(user)
        while True:
            user_time = input("\t\tNew time (hh:mm): ")
            if user_time in ["x", "q"]:
                break
            if valid.time_input(user_time) is True:
                break
            print(f"\t\tInvalid input: '{user_time}'.\n"
                  "\t\tPlease, enter valid time.\n")
        if user_time == "x":
            break
        if user_time == "q":
            run.start_menu(user)
        if user_date != "":
            spsheet.update_data("bookings", booking, "DATE", user_date)
        spsheet.update_data("bookings", booking, "TIME", user_time)
        break


def has_duplicates(user_date, name):
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
KEYS = spsheet.get_data("bookings")[0]
