"""
Includes customers specific functions.
"""
from booking_sys import spreadsheet as spsheet
from booking_sys import validation as valid
from booking_sys import stats
import run


KEYS = spsheet.get_data("customers")[0]


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
    customers = spsheet.get_data("customers")
    return search(name, "NAME", customers)


def customers_menu(user):
    """
    Displays Customers Menu.
    """
    while True:
        user_input = input("\n\tpress x - <=="
                           "\n\tpress 1 - View a customer"
                           "\n\tpress 2 - List of customers"
                           "\n\tpress 3 - Stats\n\t")
        if user_input == "1":
            user_input = input("\n\tEnter name or leave empty to go back: ")
            view_customer(user_input, user)
        elif user_input == "2":
            view_customer("all", user)
        elif user_input == "3":
            stats.data_for_stats()
            stats.customers_stats()
            print("\tYour stats is ready! Check your Reports folder.")
        elif user_input == "x":
            run.start_menu(user)
            break
        else:
            print("\tInvalid input. Please, use options above.")
    return True


def create_customer(name, user):
    """
    Creates a new customer with a parameter 'name' and writes
    it to the spreadsheet.
    """
    new_name = name
    print("\n\tCreate a new customer:\n")
    while True:
        # input contact number
        phone = input("\tContact number: ")
        # escape
        if phone == "x":
            break
        if phone == "q":
            run.start_menu(user)
        # input and validate email
        while True:
            email = input("\tEmail to receive reminders: ").encode('utf-8')
            if valid.email(email.decode('utf-8')) is True or email == "x":
                break
            print(f"\tInvalid input: '{email.decode('utf-8')}'."
                  "\tEnter a valid email.\n")
            if email.decode('utf-8') == "x":
                break
        # escape
        if email.decode('utf-8') == "x":
            break
        if email.decode('utf-8') == "q":
            run.start_menu(user)
        # input and validate birthdate
        while True:
            bday = input("\tDate of birth (dd-mm-yyyy): ")
            valid_date = valid.birthdate(bday)
            if valid_date is True or bday == "x":
                break
            print(f"\tInvalid input: '{bday}'. Enter a valid date.\n")
        # escape
        if bday == "x":
            break
        if bday == "q":
            run.start_menu(user)
        # process data and update spreadsheet 
        new_data = [new_name, phone, email.decode('utf-8'), valid_date, 1, 0]
        spsheet.update_worksheet(new_data, "customers")
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


def view_customer(name, user):
    """
    Checks the request and to print out the customer
    and calls print_customer.
    """
    if name == "q":
        from run import start_menu
        start_menu(user)
    customers = spsheet.get_data("customers")
    customer = get_customer(name)
    if customer is not None:
        print_customer(customer)
    elif name == "all":
        for item in customers:
            print_customer(item)
    else:
        print(f"\tCustomer '{name}' doesn't exist.")


@pretty_print
def print_customer(customer):
    """
    Prints out information about the requested customer.
    """
    print(f"\t{customer['NAME']} - {customer['PHONE']}, "
          f"birthday: {customer['BD']}\n"
          f"\tbookings history: {customer['NUM OF BOOKINGS']},"
          f"cancelled: {customer['CANCELLED']}")


def find_customer(user):
    """
    Returns a customer if exists or offers to create a new one.
    Allows to input again in case of a typo.
    """
    customer = None
    while True:
        print("\n\t~'x' - one level up // 'q' - to the start menu ~")
        name = input("\n\tEnter a customer's name: ")
        customer = get_customer(name)
        if name == "x":
            break
        if name == "q":
            run.start_menu(user)
        if customer is None:
            print(f"\tCustomer '{name}' does not exist.")
            while True:
                user_inp = input(f"\tCreate a new customer '{name}'? y/n\n\t")
                if user_inp == "y":
                    customer = create_customer(name, user)
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
