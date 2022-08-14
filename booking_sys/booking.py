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
            result = view_bookings_menu(user)
            if result == "q":
                break
        elif user_inp == "2":
            customer = cust.find_customer()
            if customer is None:
                continue
            if customer == "q":
                break
            result = new_booking(user, customer)
            if result == "q":
                break
        elif user_inp == "3":
            result = edit_bookings()
            if result == "q":
                break
        elif user_inp == "x":
            break
        else:
            print("\tInvalid input. Please, use options above.")
    return True


@run.loop_menu_qx("\t\t",
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
    bookings_data = active(spsheet.get_data("bookings"))
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
        bookings = active(spsheet.get_data("bookings"))
        print_bookings(bookings, valid_date, valid_date)
        return valid_date
    if duplicates:
        return None
    return False


@run.loop_menu_qx("\t\t",
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


@run.loop_menu_qx("\t",
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
    while True:
        day = new_date(customer)
        if day == "x":
            break
        if day == "q":
            return day

        time = new_time(user)
        if time == "x":
            break
        if time == "q":
            return time

        num = num_of_people(user)
        if num == "x":
            break
        if num == "q":
            return num

        new = [day, time, name, num, created, "-", ""]
        spsheet.update_worksheet(new, "bookings")
        increment_bookings(customer)
        print_bookings([dict(zip(KEYS, new))], day, day)
        return True


def to_confirm(data):
    """
    Picks bookings to confirm from active data.
    """
    not_confirmed = ([item for item in data if (item["CONF"]
                     != "yes" and item["DATE"] == today)])
    if len(not_confirmed) == 0:
        print("\n\t\tAll bookings are confirmed! Chill!")
        return False
    return not_confirmed


@run.loop_menu_qx("\t\t",
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
    bookings_data = active(spsheet.get_data("bookings"))

    if user_input == "1":
        not_confirmed = to_confirm(bookings_data)
        result = confirm(not_confirmed)
        if result == "q":
            return result
        if result == "x":
            return None
    if user_input in ["2", "3"]:
        booking = find_bookings()
        if booking in ["x", 0]:
            return None
        if booking == "q":
            return booking
        if user_input == "2":
            reschedule(booking)
        else:
            cancel(booking)
        return None
    return False


def confirm(bookings):
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
            if user_inp in ["2", "x"]:
                break
            if user_inp == "3":
                cancel(booking)
                break
            if user_inp == "q":
                return user_inp
            print("\t\t\tInvalid input. Please, use options above.")
        if user_inp == "x":
            break


@run.loop_menu_qx("\t\t",
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
    while True:
        user_date = update_date(booking)
        if user_date == "x":
            break
        if user_date == "q":
            return user_date
        bookings = active(spsheet.get_data("bookings"))
        print_bookings(bookings, user_date, user_date)

        user_time = new_time()
        if user_time == "x":
            break
        if user_time == "q":
            return user_time
        spsheet.update_data("bookings", booking, "DATE", user_date)
        spsheet.update_data("bookings", booking, "TIME", user_time)
        return True


@run.loop_menu_qx("\t\t",
                  "~ ~ x - <== // q - home ~ ~",
                  "Enter a customer's name: ",
                  "Computer says no. Customer does not exist.")
def find_bookings(*args):
    """
    Finds and returns all bookings of a customer,
    accepts user input with a name to search.
    """
    customers = spsheet.get_data("customers")
    user_input = args[0]
    if user_input in [dct["NAME"] for dct in customers]:
        bookings = cust_bookings(user_input)
        all_time = [dct["DATE"] for dct in bookings]
        print_bookings(bookings, all_time, "all time")
        if len(bookings) == 0:
            print("There are no active bookings for this customer.")
            return 0
        return pick_booking(bookings)
    return False


@run.loop_menu_qx("\t\t",
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
              "Please, enter a correct date.")
        return None
    target = cust.search(valid_date, "DATE", bookings)
    if target is None:
        return False
    return target


# def pick_booking(bookings):
#     """
#     Picks one booking from the list based on
#     user input.
#     """
#     target = None
#     while True:
#         user_date = input("\n\t\tDate of a booking to edit (dd-mm-yyyy): ")
#         if user_date == "x":
#             break
#         if user_date == "q":
#             return user_date
#         valid_date = valid.date_input(user_date)
#         if valid_date is False:
#             print(f"\t\tInvalid input: '{user_date}'. "
#                   "Please, enter a correct date.")
#             continue
#         target = cust.search(valid_date, "DATE", bookings)
#         if target is not None:
#             break
#         print(f"There are no bookings for {valid_date}.")
#     return target


def cancel(booking):
    """
    Updates bookings spreadsheet with new booking status
    and increments the customer's stats of cancelled bookings.
    """
    spsheet.update_data("bookings", booking, "CANC", "yes")
    customer = cust.get_customer(booking["NAME"])
    new_value = str(int(customer["CANCELLED"]) + 1)
    spsheet.update_data("customers", customer, "CANCELLED", new_value)
    return True


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
    spsheet.update_data("customers", customer, "NUM OF BOOKINGS", new_number)


today = dd_mm_yyyy(str(date.today()))
KEYS = spsheet.get_data("bookings")[0]
