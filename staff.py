import getpass
from spreadsheet import get_worksheet, update_worksheet


class Staff:
    """
    Creates instance of Staff
    """
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

    def describe(self):
        """
        Prints info about a member of staff
        """
        return f"User: {self.name}, contact: {self.contact}\n"


def transpose_data(data_list):
    """
    ...
    """
    return [[row[i] for row in data_list] for i in range(3)]


def staff_data():
    """
    ...
    """
    staff = get_worksheet("staff")
    return transpose_data(staff)


def create_staff():
    """
    Creates a new member of Staff
    """
    new_name = input("Enter a name for a new member of staff:\n")
    print(f"Hi, {new_name}!")
    password = getpass.getpass("Create a password:")
    contact = input("Awesome! Enter your contact number:")
    update_worksheet([new_name, password, contact], "staff")
    return Staff(new_name, contact)

