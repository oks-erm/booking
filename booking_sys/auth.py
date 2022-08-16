"""
Authorisation.
"""
import getpass


def check_password(user, password):
    """
    Checks the user's password. Takes user(dict) and
    string with a password.
    """
    if user["PASSWORD"] == password:
        print("All good!\n")
        return True
    return False


def authorise(user):
    """
    Accepts the user's input and runs the loop for 3 attempts.
    Takes user(dict).
    """
    for i in range(3):
        print(f"Attempt {i+1} of 3")
        password = getpass.getpass("Password:")
        if check_password(user, password):
            return True
        print("The password is not correct! Try again!\n")
    return False


def staff_login(data):
    """
    Logs in a member of staff. Takes staff data
    list of dictionaries.
    """
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input("\nEnter your name or enter 'new' "
                             "if you are a new member of staff: ")
        import booking_sys.customer as customer
        user = customer.search(entered_name, "NAME", data)
        if user is not None:
            if authorise(user) is not True:
                continue
            break
        if entered_name.lower() == "new":
            from booking_sys.staff import create_staff
            user = create_staff(data)
            if user is None:
                continue
            break
        print(f"Sorry, there is no user '{entered_name}'.")
        print("If you want to create a new user, enter 'new'.\n")

    return user
