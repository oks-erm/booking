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
        return f"User: {self.name}, contact: {self.contact}"


def transpose_data(data_list):
    """
    ...
    """
    return [[row[i] for row in data_list] for i in range(3)]


def get_staff_data():
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


def print_staff_info(inp, staff_list):
    """
    ...
    """
    if inp == "all":
        for i in range(len(staff_list[0])):
            print(f"{staff_list[0][i]} : {staff_list[2][i]}")
    if inp in staff_list[0]:
        i = staff_list[0].index(inp)
        print(f"{staff_list[0][i]} : {staff_list[2][i]}")
