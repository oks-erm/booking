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
    Returns date in the new format.
    """
    try:
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', my_date)
    except TypeError:
        print(f"{my_date} is {type(my_date)}. This method requires str.")


def active(data):
    """
    Filters out past and cancelled bookings.
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
    Checks if booking is confirmed and
    returns a corresponding symbol.
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
    Displays booking menu
    """
    user_input, user = (args)
    if user_input == "1":
        return view_bookings_menu(user)
    if user_input == "2":
        customer = find_customer()
        if customer in [None, "q", "x"]:
            return customer
        return new_booking(user, customer)
    if user_input == "3":
        return edit_bookings()
    return False


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
    you want to print. Accepts the user's choice.
    """
    # get the latest bookings data
    bookings_data = active(get_data("bookings"))
    # time periods
    tomorrow = dd_mm_yyyy(str(date.today() + timedelta(days=1)))
    week = [today]
    for i in range(1, 7):
        week.append(dd_mm_yyyy(str(date.today() + timedelta(days=i))))
    all_time = [dct['DATE'] for dct in bookings_data]
    user_input = args[0]

    if user_input == "1":
        print_bookings(bookings_data, today, "today")
    elif user_input == "2":
        print_bookings(bookings_data, tomorrow, "tomorrow")
    elif user_input == "3":
        print_bookings(bookings_data, week, "the upcoming week")
    elif user_input == "4":
        print_bookings(bookings_data, all_time, "all time")
    else:
        return False
    return True


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


@loop_menu_qx("\t",
              "",
              "Enter a booking date (dd-mm-yyyy): ",
              "Invalid date.")
def new_date(*args):
    """
    Accepts user input and validates date,
    checking if it's correect format, not from the past
    and a customer doesn't have duplicate bookings for
    the same date.
    """
    user_input, customer = (args)
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
    Accepts user input and validates time,
    checking if it's correect format.
    """
    user_input = args[0]
    if valid.time_input(user_input) is True:
        return user_input
    return False


@loop_menu_qx("\t\t",
              "",
              "How many people: ",
              "Not a number. Please, use a number.")
def num_of_people(*args):
    """
    Accepts number of people, validates that
    it is a number.
    """
    user_input = args[0]
    try:
        num = int(user_input)
    except ValueError:
        return False
    else:
        return num


def new_booking(user, customer):
    """
    Creates a new booking acepting the user's
    input and writes it to the spreadsheet.
    """
    name = customer["NAME"]
    created = user["NAME"]

    day = new_date(customer)
    if day in ["x", "q"]:
        return day
    time = new_time(user)
    if time in ["x", "q"]:
        return time
    num = num_of_people(user)
    if num in ["x", "q"]:
        return num

    new = [day, time, name, num, created, "-", ""]
    update_worksheet(new, "bookings")
    increment_bookings(customer)
    print_bookings([dict(zip(KEYS, new))], day, day)
    return None  # to stay in the loop of bookings_menu


def to_confirm(data):
    """
    Picks bookings to confirm from active data.
    """
    not_confirmed = ([item for item in data if (item["CONF"]
                     != "yes" and item["DATE"] == today)])
    if len(not_confirmed) == 0:
        print("\n\t\tAll bookings are confirmed! Chill!")
        return None
    return not_confirmed


@loop_menu_qx("\t\t",
              "x - <== // q - home",
              "press 1 - Confirm\n\t\t"
              "press 2 - Reschedule\n\t\t"
              "press 3 - Cancel\n\t\t",
              "Invalid input. Please, use options above.")
def edit_bookings(*args):
    """
    Displays Edit Bookings menu.
    """
    user_input = args[0]
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
    return False


def confirm(bookings):
    """
    Finds not confirmed bookings and prints them
    with contact numbers one by one to confirm or
    skip.
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
    return None


@loop_menu_qx("\t\t",
              "",
              "Enter a new date(dd-/.mm-/.yyyy) "
              "(leave empty if no change): ",
              "Invalid date.")
def update_date(*args):
    """
    Accepts user input and validates date,
    checking if it's correect format, not from the past
    and a customer doesn't have duplicate bookings for
    the same date.
    """
    user_input, booking = (args)
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
    Updates booking data about date or time.
    """
    user_date = update_date(booking)
    if user_date in ["x", "q"]:
        return user_date
    bookings = active(get_data("bookings"))
    print_bookings(bookings, user_date, user_date)

    user_time = new_time()
    if user_time in ["x", "q"]:
        return user_time
    update_data("bookings", booking, "DATE", user_date)
    update_data("bookings", booking, "TIME", user_time)
    return None


@loop_menu_qx("\t\t",
              "~ ~ x - <== // q - home ~ ~",
              "Enter a customer's name: ",
              "Computer says no. Customer does not exist.")
def find_bookings(*args):
    """
    Finds and returns all bookings of a customer,
    accepts user input with a name to search.
    """
    customers = get_data("customers")
    user_input = args[0]
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
    return False


@loop_menu_qx("\t\t",
              "",
              "Date of a booking to edit (dd-mm-yyyy): ",
              "There are no bookings for this date.")
def pick_booking(*args):
    """
    Picks one booking from the list based on
    user input.
    """
    target = None
    user_input, bookings = (args)
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
    Updates bookings spreadsheet with new booking status
    and increments the customer's stats of cancelled bookings.
    """
    update_data("bookings", booking, "CANC", "yes")
    customer = get_customer(booking["NAME"])
    new_value = str(int(customer["CANCELLED"]) + 1)
    update_data("customers", customer, "CANCELLED", new_value)


def has_duplicates(user_date, name):
    """
    Checks if a customer already has a booking for
    this date.
    """
    customer_bookings = cust_bookings(name)
    if user_date in [dct["DATE"] for dct in customer_bookings]:
        print(f"\n\t\t!!!Booking for {user_date} already exists!!!")
        print_bookings(customer_bookings, user_date, user_date)
        return True
    return False


def increment_bookings(customer):
    """
    Increments number of bookings a customer has, when
    a new booking is created.
    """
    new_number = str(int(customer["NUM OF BOOKINGS"]) + 1)
    update_data("customers", customer, "NUM OF BOOKINGS", new_number)


today = dd_mm_yyyy(str(date.today()))
KEYS = get_data("bookings")[0]
