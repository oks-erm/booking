"""
Decorators used throughout the package.
"""


def loop_menu_qx(indentation, qx_text, input_prompt, warning):
    """
    Places a function inside a While Loop, which goes one step
    back if input is "x" and goes back to the start menu input
    is "q". Warns the user about invalid input if a function
    returns False.
    Required parameters:
        indentation(str),
        qx_text(str, navigation instructions at the top of the block,
        leave empty if it repeats too often)
        input_prompt(str, text for input method)
        warning(str, text to warn the user if input is invalid)
    """
    def decorator(func):
        def wrap_func(*args):
            while True:
                result = None
                print("\n" + indentation + qx_text)
                user_input = input(indentation + input_prompt)
                if user_input in ["x", "q"]:
                    break
                result = func(user_input, *args)
                if result == "q":
                    return result
                if result is False:
                    print(indentation + warning)
                    continue
                if result in [None, "x"]:
                    continue
                break
            if user_input in ["x", "q"]:
                return user_input
            if result is not True:
                return result
            return None
        return wrap_func
    return decorator


def pretty_print(func):
    """
    A decorator to print output framed with lines of * symbol.
    """
    def wrap_func(*args, **kwargs):
        print("")
        print('*' * 65)
        func(*args, **kwargs)
        print("*" * 65)
    return wrap_func
