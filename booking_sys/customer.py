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


def customers_menu():
    """
    Displays Customers Menu.
    """
    while True:
        user_input = input("\n\tpress x - <=="
                           "\n\tpress 1 - View a customer"
                           "\n\tpress 2 - List of customers"
                           "\n\tpress 3 - Stats\n\t")
        if user_input == "1":
            user_input = input("\n\tx - <== // q - home\n\tEnter name: ")
            if user_input == "q":
                break
            if user_input == "x":
                continue
            view_customer(user_input)
        elif user_input == "2":
            view_customer("all")
        elif user_input == "3":
            stats.data_for_stats()
            stats.customers_stats()
            print("\tYour stats is ready! Check your Reports folder.")
        elif user_input == "x":
            break
        else:
            print("\tInvalid input. Please, use options above.")
    return True


def view_customer(name):
    """
    Checks the request and to print out the customer
    and calls print_customer.
    """
    customers = spsheet.get_data("customers")
    customer = get_customer(name)
    if customer is not None:
        print_customer(customer)
    elif name == "all":
        for item in customers:
            print_customer(item)
    else:
        print(f"\tCustomer '{name}' doesn't exist.")


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
def print_customer(customer):
    """
    Prints out information about the requested customer.
    """
    print(f"\t{customer['NAME']} - {customer['PHONE']}, "
          f"birthday: {customer['BD']}\n"
          f"\tbookings history: {customer['NUM OF BOOKINGS']},"
          f"cancelled: {customer['CANCELLED']}")


def find_customer():
    """
    Returns a customer if exists or offers to create a new one.
    Allows to input again in case of a typo.
    """
    customer = None
    while True:
        print("\n\t~'x' - one level up // 'q' - to the start menu ~")
        name = input("\n\tEnter a customer's name: ")
        if name == "x":
            break
        if name == "q":
            return name
        customer = get_customer(name)
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


@run.loop_menu_qx("\t",
                  "",
                  "Contact number: ",
                  "Invalid input. Please, enter a valid phone number.")
def new_phone(*args):
    """
    Accepts user input and validates phone number.
    """
    if valid.phone_num(args[0]):
        return args[0]
    return False


@run.loop_menu_qx("\t",
                  "",
                  "Email to receive reminders: ",
                  "Invalid input. Please, enter a valid email.")
def new_email(*args):
    """
    Accepts user input and validates email.
    """
    if valid.email(args[0]):
        return args[0]
    return False


@run.loop_menu_qx("\t",
                  "",
                  "Date of birth: ",
                  "Invalid input. Please, enter a valid date.")
def new_birthdate(*args):
    """
    Accepts user input and validates email.
    """
    bday = valid.birthdate(args[0])
    if bday:
        return bday
    return False


def create_customer(name):
    """
    Creates a new customer with a parameter 'name' and writes
    it to the spreadsheet.
    """
    new_name = name
    print("\n\tCreate a new customer:")
    while True:
        phone = new_phone()
        if phone == "x":
            break
        if phone == "q":
            return phone
        email = new_email()
        if email == "x":
            break
        if email == "q":
            return email
        birthday = new_birthdate()
        if birthday == "x":
            break
        if birthday == "q":
            return birthday
        # process data and update spreadsheet
        new_data = [new_name, phone, email, birthday, 1, 0]
        spsheet.update_worksheet(new_data, "customers")
        return dict(zip(KEYS, new_data))
