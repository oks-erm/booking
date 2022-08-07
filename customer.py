"""
Includes customers specific functions.
"""
from spreadsheet import get_data, update_worksheet
from validation import validate_birthdate, validate_email


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


def get_customer(name):
    """
    Returns a dictionary with a customer of a given name.
    """
    customers = get_data("customers")
    return search(name, "NAME", customers)


def create_customer(name):
    """
    Creates a new customer with a parameter 'name' and writes
    it to the spreadsheet.
    """
    new_name = name
    print("\n\tCreate a new customer:\n")
    while True:
        phone = input("\tContact number: ")
        if phone == "x":
            break
        while True:
            email = input("\tEmail to receive reminders: ").encode('utf-8')
            if validate_email(email.decode('utf-8')) is True or email == "x":
                break
            print(f"\tInvalid input: '{email.decode('utf-8')}'. Enter a valid email.\n")
            if email.decode('utf-8') == "x":
                break
        if email.decode('utf-8') == "x":
            break
        while True:
            bday = input("\tDate of birth (dd-mm-yyyy): ")
            if validate_birthdate(bday) is True or bday == "x":
                break
            print(f"\tInvalid input: '{bday}'. Enter a valid date.\n")
        if bday == "x":
            break
        new_data = [new_name, phone, email.decode('utf-8'), bday, 1, 0]
        update_worksheet(new_data, "customers")
        return dict(zip(KEYS, new_data))


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
    customers = get_data("customers")
    customer = get_customer(name)
    if customer is not None:
        print_customer(customer)
    elif name == "all":
        for item in customers:
            print_customer(item)
            print("-" * 50)
    else:
        print(f"\tCustomer '{name}' doesn't exist.")


def print_customer(cust):
    """
    Prints out information about the requested customer.
    """
    print(f"\t{cust['NAME']} - {cust['PHONE']} BD: {cust['BD']}")
    print(f"\tbookings history: {cust['NUM OF BOOKINGS']},\
 cancelled: {cust['CANCELLED']}")


def find_customer():
    """
    Returns a customer if exists or offers to create a new one.
    Allows to input again in case of a typo.
    """
    customer = None
    while True:
        print("\n\t~ Enter 'x' at any point to go back ~")
        name = input("\n\tEnter a customer's name: ")
        customer = get_customer(name)
        if name == "x":
            break
        if customer is None:
            print(f"\tCustomer '{name}' does not exist.")
            while True:
                user_inp = input(f"\tCreate a new customer '{name}'? y/n\n\t")
                if user_inp == "y":
                    customer = create_customer(name)
                    break
                if user_inp == "n":
                    break
                print("\n\tInvalid input. Please, use options above.\n")
        else:
            break
        if user_inp == "n":
            continue
        if user_inp == "y":
            break

    return customer
