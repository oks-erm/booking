"""
Authorisation.
"""
import getpass
import booking_sys.customer as customer


def authorise(user):
    """
    Checks the user's password
    """
    for i in range(4):
        print(f"Attempt {i+1} of 4")
        password = getpass.getpass("Password:")
        if user["PASSWORD"] == password:
            print("All good!\n")
            return True
        print("The password is not correct! Try again!\n")


def staff_login(data):
    """
    Logs in a member of staff.
    """
    print("\n\n\t\tWelcome to Your Booking System!\n")
    while True:
        entered_name = input("Enter your name or enter 'new' "
                             "if you are a new member of staff: ")
        user = customer.search(entered_name, "NAME", data)
        if user is not None:
            if authorise(user) is not True:
                continue
            break
        if entered_name.lower() == "new":
            from booking_sys.staff import create_staff
            user = create_staff()
            if user == "x":
                continue
            break
        print(f"Sorry, there is no user '{entered_name}'.")
        print("If you want to create a new user, enter 'new'.\n")
        
    print(f"{user['NAME']} : {user['CONTACT']}")
    return user

