"""
Includes customers specific functions.
"""
from booking_sys import spreadsheet as spsheet
from booking_sys import validation as valid
from booking_sys import stats
from booking_sys.decorators import pretty_print, loop_menu_qx


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


@loop_menu_qx("\t",
              "press x - <==",
              "press 1 - View customers\n\t"
              "press 2 - Stats\n\t",
              "Invalid input. Please, use options above.")
def customers_menu(*args):
    """
    Displays Customers Menu.
    """
    user_input = args[0]
    if user_input == "1":
        return view_customer(user_input)
    if user_input == "2":
        stats.data_for_stats()
        stats.customers_stats()
        print("\tYour stats is ready! Check your Reports folder.")
        return None
    return False


@loop_menu_qx("\t\t",
              "x - <== // q - home",
              "Enter 'all' to see the full list\n\t\t"
              "Or enter a name to search by name: ",
              "Customer doesn't exist.")
def view_customer(*args):
    """
    Checks the request and to print out the customer
    and calls print_customer.
    """
    name = args[0]
    customers = spsheet.get_data("customers")
    customer = get_customer(name)
    if customer is not None:
        print_customer(customer)
        return True
    if name == "all":
        for item in customers:
            print_customer(item)
        return True
    return False


@pretty_print
def print_customer(customer):
    """
    Prints out information about the requested customer.
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
    Returns a customer if exists or offers to create a new one.
    Allows to input again in case of a typo.
    """
    name = args[0]
    customer = get_customer(name)
    if customer is None:
        print(f"\tCustomer '{name}' does not exist.")
        while True:
            user_input = input(f"\tCreate a new customer '{name}'? y/n\n\t")
            if user_input == "y":
                customer = create_customer(name)
                if customer == "x":
                    return True  # if it returns x, the loop continues
                return customer
            if user_input == "n":
                return None
            print("\n\tInvalid input. Please, use options above.\n")
    return customer


@loop_menu_qx("\t\t",
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


@loop_menu_qx("\t\t",
              "",
              "Email to receive reminders: ",
              "Invalid input. Please, enter a valid email.")
def new_email(*args):
    """
    Accepts user input and validates email.
    """
    if valid.email(args[0]):
        return args[0].encode('utf-8')
    return False


@loop_menu_qx("\t\t",
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
    new_data = [new_name, phone, email.decode('utf-8'), birthday, 1, 0]
    spsheet.update_worksheet(new_data, "customers")
    return dict(zip(KEYS, new_data))
