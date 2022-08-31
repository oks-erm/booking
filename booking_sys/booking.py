"""
Includes bookings specific functions.
"""
import re
from datetime import datetime, date, timedelta
from booking_sys.spreadsheet import get_data, update_worksheet, update_data
from booking_sys.customer import find_customer, get_customer, search
from booking_sys import validation as valid
from booking_sys.decorators import pretty_print, loop_menu_qx


def dd_mm_yyyy(my_date):
    """
    Changes date format from YYYY-MM-DD to DD-MM-YYYY.
    Takes in a string as an argument.
    Returns a date(str) in new format.
    """
    try:
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)
    except TypeError:
        print(f"{my_date} is {type(my_date)}. This method requires str.")


def active(data):
    """
    Filters out past and cancelled bookings.
    Takes in a list of dictionaries as an argument.
    Returns a list of dictionaries.
    """
    try:
        filtered = [item for item in data if
                    (valid.to_date(item["DATE"]) >= date.today()) and
                    (item["CANC"] != "yes")]
        return filtered
    except (TypeError, ValueError):
        print(f"{data} is {type(data)}. Argument should be a list.")


def confirmed(booking):
    """
    Checks if booking is confirmed. Takes in a dictionary and
    returns a corresponding symbol "\\/" or "--".
    """
    try:
        if booking["CONF"] == "yes":
            return "\\/"
        return "--"
    except (TypeError, ValueError):
        print(f"{booking} is {type(booking)}. Argument should be a dict.")


def cust_bookings(name):
    """
    Selects all active bookings of a customer.
    Takes in a customer's name(str) and returns a
    list of dictionaries.
    """
    bookings = get_data("bookings")
    return [item for item in active(bookings) if item["NAME"] == name]


@loop_menu_qx("\t",
              "x - <== ",
              "press 1 - View bookings\n\t"
              "press 2 - Add a booking\n\t"
              "press 3 - Edit bookings\n\t",
              "Invalid input. Please, use options above.")
def bookings_menu(*args):
    """
    Displays booking menu. Takes in a user(dict) and
    user_input(str) as arguments.
    """
    (user_input, user) = args
    if user_input == "1":
        return view_bookings_menu()
    if user_input == "2":
        customer = find_customer()
        if customer in [None, "q", "x"]:
            return customer
        return new_booking(user, customer)
    if user_input == "3":
        return edit_bookings()
    return False  # for invalid input


@loop_menu_qx("\t\t",
              "x - <== // q - home",
              "press 1 - Today\n\t\t"
              "press 2 - Tomorrow\n\t\t"
              "press 3 - Next 7 days\n\t\t"
              "press 4 - All\n\t\t",
              "Invalid input. Please, use options above.")
def view_bookings_menu(*args):
    """
    Displays menu to choose bookings for what period
    you want to print out. Takes in user_input(str) as an
    argument.
    """
    (user_input, ) = args
    bookings_data = active(get_data("bookings"))
    # time periods
    tomorrow = dd_mm_yyyy(str(date.today() + timedelta(days=1)))
    week = [today]
    for i in range(1, 7):
        week.append(dd_mm_yyyy(str(date.today() + timedelta(days=i))))
    all_time = [dct['DATE'] for dct in bookings_data]

    if user_input == "1":
        print_bookings(bookings_data, today, "today")
    elif user_input == "2":
        print_bookings(bookings_data, tomorrow, "tomorrow")
    elif user_input == "3":
        print_bookings(bookings_data, week, "the upcoming week")
    elif user_input == "4":
        print_bookings(bookings_data, all_time, "all time")
    else:
        return False  # for invalid input
    return True
    # to make decorator return None and stay
    # in the loop of the parent menu


@pretty_print
def print_bookings(data, period, string):
    """
    Selects bookings data out of given range and prints it.
    Takes in data(list of dictionaries), time range(str) and
    a string to name it in the print output.
    """
    # filter booking for the period
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


@loop_menu_qx("\t",
              "",
              "Enter a booking date (dd-/.mm-/.yyyy): ",
              "Invalid date.")
def new_date(*args):
    """
    Takes in user_input(str) and a customer(dict) and
    validates date, checking if it's correect format,
    not from the past and a customer doesn't have duplicate
    bookings for the same date. Returns a valid date if it
    is valid and has no duplicates, returns None if it has
    duplicates. Returns False for invalid input.
    """
    (user_input, customer) = args
    valid_date = valid.date_input(user_input)
    duplicates = has_duplicates(valid_date, customer["NAME"])
    if valid_date and duplicates is False:
        bookings = active(get_data("bookings"))
        print_bookings(bookings, valid_date, valid_date)
        return valid_date
    if duplicates:
        return None
    return False


@loop_menu_qx("\t\t",
              "",
              "New time (hh:mm): ",
              "Invalid time.")
def new_time(*args):
    """
    Takes in user_input(str) and validates time: if it's
    correect format. Returns valid time or False for invalid
    input.
    """
    (user_input, ) = args
    if valid.time_input(user_input) is True:
        return user_input
    return False


@loop_menu_qx("\t\t",
              "",
              "How many people: ",
              "Not a number. Please, use a number.")
def num_of_people(*args):
    """
    Takes in user_input(str), validates that it is a number.
    Returns valid value(str) or False for invalid input.
    """
    (user_input, ) = args
    try:
        num = int(user_input)
    except ValueError:
        return False
    else:
        return str(num)


def new_booking(user, customer):
    """
    Creates a new booking, takes in user_input(str)
    and writes it to the spreadsheet.
    """
    name = customer["NAME"]
    created = user["NAME"]

    day = new_date(customer)
    if day in ["x", "q"]:
        return day
    time = new_time()
    if time in ["x", "q"]:
        return time
    num = num_of_people()
    if num in ["x", "q"]:
        return num

    new = [day, time, name, num, created, "-", ""]
    update_worksheet(new, "bookings")
    increment_bookings(customer)
    print_bookings([dict(zip(KEYS, new))], day, day)
    return None  # to stay in the loop of the current menu


def to_confirm(data):
    """
    Picks bookings to confirm from active data. Takes in a list of
    dictionaries and returns a filterd list of dictionaries.
    """
    not_confirmed = ([item for item in data if
                      (item["CONF"] != "yes" and item["DATE"] == today)])
    if len(not_confirmed) == 0:
        print("\n\t\tAll bookings are confirmed! Chill!")
        return None  # to stay in the loop of the current menu
    return not_confirmed


@loop_menu_qx("\t\t",
              "x - <== // q - home",
              "press 1 - Confirm\n\t\t"
              "press 2 - Reschedule\n\t\t"
              "press 3 - Cancel\n\t\t",
              "Invalid input. Please, use options above.")
def edit_bookings(*args):
    """
    Displays Edit Bookings menu. Takes in user_input(str).
    """
    (user_input, ) = args
    if user_input == "1":
        bookings_data = active(get_data("bookings"))
        return confirm(to_confirm(bookings_data))
    if user_input in ["2", "3"]:
        booking = find_bookings()
        if booking in ["x", 0, None]:
            return None
        if booking == "q":
            return booking
        if user_input == "2":
            return reschedule(booking)
        return cancel(booking)
    return False  # for invalid input


def confirm(bookings):
    """
    Finds not confirmed bookings and prints them with customer's
    contact information one by one to confirm, skip or cancel.
    Takes in a list of dictionaries.
    """
    if bookings is None:
        return bookings
    for booking in bookings:
        print_bookings([booking], today, "today")
        user_inp = input("\n\t\t\t" + "x - <== // q - home\n\t\t\t"
                         "press 1 - Confirmed\n\t\t\t"
                         "press 2 - Skip\n\t\t\t"
                         "press 3 - Cancel\n\t\t\t")
        if user_inp == "1":
            booking.update({"CONF": "yes"})
            update_data("bookings", booking, "CONF", "yes")
        elif user_inp == "2":
            continue
        elif user_inp == "3":
            cancel(booking)
        elif user_inp in ["q", "x"]:
            return user_inp
        else:
            print("\t\t\tInvalid input. Please, use options above.")
    return None  # to stay in the loop of the current menu


@loop_menu_qx("\t\t",
              "",
              "Enter a new date(dd-/.mm-/.yyyy)\n"
              "(leave empty if no change): ",
              "Invalid date.")
def update_date(*args):
    """
    Takes in user_input(str) and a booking(dict) and validates date,
    checking if it's correect format, not from the past and a customer
    doesn't have duplicate bookings for the same date. Returns a valid
    new date, old date if the input is an empty string or False for
    invalid input.
    """
    (user_input, booking) = args
    old_date = booking["DATE"]
    if user_input != "":
        valid_date = valid.date_input(user_input)
        duplicates = has_duplicates(valid_date, booking["NAME"])
        if (valid_date and duplicates is False):
            return valid_date
        return False
    return old_date


def reschedule(booking):
    """
    Updates booking data about date, time or number of people.
    Takes in a booking(dict) and writes changes to the Spreadsheet.
    """
    user_date = update_date(booking)
    if user_date in ["x", "q"]:
        return user_date
    bookings = active(get_data("bookings"))
    print_bookings(bookings, user_date, user_date)

    user_time = new_time()
    if user_time in ["x", "q"]:
        return user_time

    num = num_of_people()
    if num in ["x", "q"]:
        return num

    print("\t\tSaving .....")
    if user_date != booking["DATE"]:
        update_data("bookings", booking, "DATE", user_date)
    update_data("bookings", booking, "TIME", user_time)
    update_data("bookings", booking, "PEOPLE", num)
    return None  # to stay in the loop of the current menu


@loop_menu_qx("\t\t",
              "~ ~ x - <== // q - home ~ ~",
              "Enter a customer's name: ",
              "Computer says no. Customer does not exist.")
def find_bookings(*args):
    """
    Finds and returns all bookings of a customer,
    accepts user input(str) with a name to search.
    Returns a list of dictionaries or False for
    invalid input.
    """
    (user_input, ) = args
    customers = get_data("customers")
    if user_input in [dct["NAME"] for dct in customers]:
        bookings = cust_bookings(user_input)
        all_time = [dct["DATE"] for dct in bookings]
        print_bookings(bookings, all_time, "all time")
        if len(bookings) == 0:
            print("\t\tThere are no active bookings for this customer.")
            return 0
        result = pick_booking(bookings)
        if result != "x":
            return result
        return True
        # to make decorator return None and stay
        # in the loop of the parent menu
    return False


@loop_menu_qx("\t\t",
              "",
              "Date of a booking to edit (dd-/.mm-/.yyyy): ",
              "There are no bookings for this date.")
def pick_booking(*args):
    """
    Takes in user_input(str) and bookings(list of dictionaries).
    Picks one booking from the list based on the user input.
    Returns a dictionary or False if there are no bookings
    for this date.
    """
    (user_input, bookings) = args
    target = None
    valid_date = valid.date_input(user_input)
    if valid_date is False:
        print(f"\t\tInvalid input: '{user_input}'. "
              "Please, enter a valid date.")
        return None
    target = search(valid_date, "DATE", bookings)
    if target is None:
        return False
    return target


def cancel(booking):
    """
    Takes in a booking(dict). Updates bookings spreadsheet with
    new booking status and increments the customer's stats of
    cancelled bookings.
    """
    update_data("bookings", booking, "CANC", "yes")
    customer = get_customer(booking["NAME"])
    new_value = str(int(customer["CANCELLED"]) + 1)
    update_data("customers", customer, "CANCELLED", new_value)


def has_duplicates(user_date, name):
    """
    Takes in a date(str) and a name(str). Checks if a customer
    already has a booking for this date. Returns boolean.
    """
    customer_bookings = cust_bookings(name)
    if user_date in [dct["DATE"] for dct in customer_bookings]:
        print(f"\n\t\t!!!Booking for {user_date} already exists!!!")
        print_bookings(customer_bookings, user_date, user_date)
        return True
    return False


def increment_bookings(customer):
    """
    Takes in a customer(dict). Increments number of bookings
    a customer has, when a new booking is created.
    """
    new_number = str(int(customer["NUM OF BOOKINGS"]) + 1)
    update_data("customers", customer, "NUM OF BOOKINGS", new_number)


today = dd_mm_yyyy(str(date.today()))
KEYS = get_data("bookings")[0]
