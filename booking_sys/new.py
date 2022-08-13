import os
import sys
# from booking_sys.spreadsheet import get_data
import booking_sys.booking as booking
import booking_sys.customer as customer
# import booking_sys.auth as auth


# def start_menu(user):
#     """
#     Displays start menu after the user is logged in.
#     """
#     print(f"\nWhat do you want to do, {user['NAME']}?")
#     while True:
#         user_inp = input("press 1 - Bookings\n"
#                          "press 2 - Customers\n"
#                          "press 3 - Staff info\n"
#                          "press x - Exit\n")
#         if user_inp == "1":
#             booking.bookings_menu(user)
#             break
#         if user_inp == "2":
#             customer.customers_menu(user)
#             print("Customers")
#             break
#         if user_inp == "3":
#             from booking_sys.staff import staff_menu
#             staff_menu(user)
#             break
#         if user_inp == "x":
#             cleanup()
#             sys.exit()
#         print("Invalid input. Please, use options above.\n")


# def cleanup():
#     """
#     Deletes not needed files.
#     """
#     files = ['stats.pdf', 'stats.csv']
#     for file in files:
#         if os.path.exists(file):
#             os.remove(file)


def start_menu(user):
    """
    Displays start menu after the user is logged in.
    """
    print(f"\nWhat do you want to do, {user['NAME']}?")
    while True:
        user_inp = input("press 1 - Bookings\n"
                         "press 2 - Customers\n"
                         "press 3 - Staff info\n"
                         "press x - Exit\n")
        if user_inp == "1":
            booking.bookings_menu(user)
            break
        if user_inp == "2":
            customer.customers_menu(user)
            print("Customers")
            break
        if user_inp == "3":
            from booking_sys.staff import staff_menu
            staff_menu(user)
            break
        if user_inp == "x":
            cleanup()
            sys.exit()
        print("Invalid input. Please, use options above.\n")


def loop_menu(indentation, text):
    """
    Places a function inside a While Loop,
    which breaks if input is "x" and warns
    about invalid input if a function doesn't
    return True.
    """
    def decorator(func):
        def wrap_func(*args):
            while True:
                print("\n" + indentation + "x - <== // q - home")
                user_inp = input(text)
                result = func(user_inp, *args)
                if user_inp in ["x", "q"]:
                    break
                # function returns a dict with the user instead False
                # so it can be used to call start_menu when q is pressed
                if isinstance(result, dict):
                    print("\t\tInvalid input. Please, use options above.\n")
                else:
                    break
            if user_inp == "x":
                return None
            if user_inp == "q":
                start_menu(result)
                return None
            return result
        return wrap_func
    return decorator


def cleanup():
    """
    Deletes not needed files.
    """
    files = ['stats.pdf', 'stats.csv']
    for file in files:
        if os.path.exists(file):
            os.remove(file)