"""
Includes customers specific functions.
"""
from booking_sys.spreadsheet import get_data, update_worksheet
from booking_sys import validation as valid
from booking_sys import stats
from booking_sys.decorators import pretty_print, loop_menu_qx


KEYS = get_data("customers")[0]


def search(value, attr, data):
    """
    Finds and returns an element from data
    that has a requested value of attr or
    None if there are none.
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


@loop_menu_qx("\t",
              "press x - <==",
              "press 1 - View customers\n\t"
              "press 2 - Stats\n\t",
              "Invalid input. Please, use options above.")
def customers_menu(*args):
    """
    Displays Customers Menu. Takes in user_input(str).
    """
    (user_input, ) = args
    if user_input == "1":
        return view_customer()
    if user_input == "2":
        stats.data_for_stats()
        stats.customers_stats()
        print("\tYour stats is ready! Check your Reports folder.")
        return None  # to stay in the loop of the current menu
    return False  # for invalid input


@loop_menu_qx("\t\t",
              "x - <== // q - home",
              "Enter 'all' to see the full list\n\t\t"
              "Or enter a name to search by name: ",
              "Customer doesn't exist.")
def view_customer(*args):
    """
    Takes in a name(str). Checks the request and prints
    out the customer info.
    """
    (name, ) = args
    customers = get_data("customers")
    customer = get_customer(name)
    if customer is not None:
        print_customer(customer)
        return True
        # to make decorator return None and stay
        # in the loop of the parent menu
    if name == "all":
        for item in customers:
            print_customer(item)
        return True
        # to make decorator return None and stay
        # in the loop of the parent menu
    return False  # for invalid input


@pretty_print
def print_customer(customer):
    """
    Takes in a customer(dict). Prints out information
    about the requested customer.
    """
    print(f"\t{customer['NAME']} - {customer['PHONE']}, "
          f"birthday: {customer['BD']}\n"
          f"\tbookings history: {customer['NUM OF BOOKINGS']},"
          f"cancelled: {customer['CANCELLED']}")


@loop_menu_qx("\t",
              "~'x' - one level up // 'q' - to the start menu ~\n\t",
              "Enter a customer's name: ",
              "Invalid input. Please, use options above.")
def find_customer(*args):
    """
    Takes in iser_input(str). Returns a customer if exists
    or offers to create a new one.
    """
    (name, ) = args
    customer = get_customer(name)
    if customer is None:
        print(f"\tCustomer '{name}' does not exist.")
        while True:
            user_input = input(f"\tCreate a new customer '{name}'? y/n\n\t")
            if user_input == "y":
                customer = create_customer(name)
                if customer == "x":
                    return True
                    # if it returns x, the loop continues
                    # to make decorator return None and stay
                    # in the loop of the parent menu
                return customer
            if user_input == "n":
                return None  # to stay in the current loop
            print("\n\tInvalid input. Please, use options above.\n")
    return customer


@loop_menu_qx("\t\t",
              "",
              "Contact number: ",
              "Invalid input. Please, enter a valid phone number.")
def new_phone(*args):
    """
    Takes in user_input(str) and validates phone number.
    Returns valid phone number or False for invalid input.
    """
    (user_input, ) = args
    if valid.phone_num(user_input):
        return user_input
    return False


@loop_menu_qx("\t\t",
              "",
              "Email to receive reminders: ",
              "Invalid input. Please, enter a valid email.")
def new_email(*args):
    """
    Takes in user_input(str) and validates email.
    Returns valid phone number or False for invalid input.
    """
    (user_input, ) = args
    if valid.email(user_input):
        return user_input
    return False


@loop_menu_qx("\t\t",
              "",
              "Date of birth (dd-/.mm-/.yyyy): ",
              "Invalid input. Please, enter a valid date.")
def new_birthdate(*args):
    """
    Takes in user_input(str) and validates birthdate.
    Returns valid phone number or False for invalid input.
    """
    (user_input, ) = args
    bday = valid.birthdate(user_input)
    if bday:
        return bday
    return False


def create_customer(name):
    """
    Takes in a name(str). Creates a new customer with
    a parameter 'name' and writes it to the Spreadsheet.
    Returns a new customer(dict).
    """
    print("\n\t\tCreate a new customer:")
    phone = new_phone()
    if phone in ["x", "q"]:
        return phone
    email = new_email()
    if email in ["x", "q"]:
        return email
    birthday = new_birthdate()
    if birthday in ["x", "q"]:
        return birthday
    # process data and update spreadsheet
    new_data = [name, phone, email, birthday, 1, 0]
    update_worksheet(new_data, "customers")
    return dict(zip(KEYS, new_data))
