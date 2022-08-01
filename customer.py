"""
Includes customers specific functions.
"""
import csv
from datetime import date, datetime
from spreadsheet import get_data, update_worksheet, get_worksheet
from booking import pretty_print



KEYS = get_data("customers")[0]


def search(name, data):
    """
    Find and returns an element from data
    that has a requested value of NAME.
    """
    for element in data:
        if element['NAME'] == name:
            return element


def create_customer(name):
    """
    Creates a new customer with a parameter 'name' and writes
    it to the spreadsheet.
    """
    new_name = name
    print("\tThis customer is not in the list! Create a new customer:\n")
    phone = input("\tEnter contact number: ")
    email = input("\tEnter email to receive reminders: ").encode('utf-8')
    bday = input("\tEnter date of birth in dd-mm-yyyy format: ")
    new_data = [new_name, phone, email.decode('utf-8'), bday, 1, ""]
    update_worksheet(new_data, "customers")
    return dict(zip(KEYS, new_data))


def get_customer(user_inp):
    """
    Checks if the customer exists and returns
    customer ductionary.
    """
    customers = get_data("customers")[1:]
    names = [dct['NAME'] for dct in customers]
    if user_inp in names:
        return search(user_inp, customers)
    return create_customer(user_inp)


@pretty_print
def view_customer(name):
    """
    Checks the request and to print out the customer
    and calls print_customer.
    """
    customers = get_data("customers")[1:]  # Do i need a function for 2 lines?
    names = [dct['NAME'] for dct in customers]
    if name in names:
        cust = search(name, customers)
        print_customer(cust)
    elif name == "all":
        for item in customers:
            print_customer(item)
            print("-" * 50)
    else:
        print("\tThis customer doesn't exist")


def print_customer(cust):
    """
    Prints out information about the requested customer.
    """
    print(f"\t{cust.get('NAME')} - {cust.get('PHONE')} BD: {cust.get('BD')}")
    print(f"\tbookings history: {cust.get('NUM OF BOOKINGS')},\
 cancelled: {cust.get('CANCELLED')}")


def age(birthdate):
    """
    Calculates age based on birthdate.
    """
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def data_for_stats():
    """
    Prepares data for stats and writes it to csv
    """
    data = get_worksheet("customers")
    for item in data[1:]:
        item[3] = age(datetime.strptime(item[3], "%d-%m-%Y").date())
    with open("stats.csv", "w", newline="") as f:
        f.truncate()
        writer = csv.writer(f)
        writer.writerows(data)


data_for_stats()

# def customers_stats():
#     """
#     Shows customers stats
#     """
#     data_frame = pd.read_csv('stats.csv')
#     data_frame[""].hist()