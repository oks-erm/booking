"""
Includes customers specific functions.
"""
from spreadsheet import get_data, update_worksheet


KEYS = get_data("customers")[0]


def search(value, attr, data):
    """
    Find and returns an element from data
    that has a requested value of NAME.
    """
    for element in data:
        if element.get(attr) == value:
            return element
    return None


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
    new_data = [new_name, phone, email.decode('utf-8'), bday, 1, 0]
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
        return search(user_inp, "NAME", customers)
    return create_customer(user_inp)


def pretty_print(func):
    """
    Frames print output with lines of * symbol.
    """
    def wrap_func(*args, **kwargs):
        print("")
        print('*' * 65)
        func(*args, **kwargs)
        print("*" * 65)
    return wrap_func


@pretty_print
def view_customer(name):
    """
    Checks the request and to print out the customer
    and calls print_customer.
    """
    customers = get_data("customers")[1:]  # Do i need a function for 2 lines?
    names = [dct['NAME'] for dct in customers]
    if name in names:
        cust = search(name, "NAME", customers)
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
