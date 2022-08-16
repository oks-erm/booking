"""
Tests for decorators module.
"""
from unittest import mock
from booking_sys.decorators import loop_menu_qx


@mock.patch('builtins.input', return_value='x')
def test_loop_menu_qx_for_x(input):
    """
    if user input is "x".
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func():
        return True

    assert func() == "x"


@mock.patch('builtins.input', return_value='q')
def test_loop_menu_qx_for_q(input):
    """
    if user input is "q".
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func():
        return True

    assert func() == "q"


@mock.patch('builtins.input', return_value='1')
def test_loop_menu_qx_for_input_return_true(input):
    """
    if user input is not "x" or "q" and function returns True.
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return True

    assert func() is None


@mock.patch('builtins.input', return_value='1')
def test_loop_menu_qx_for_input_return_q(input):
    """
    if user input is not "x" or "q" and function returns "q".
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return "q"

    assert func() == "q"


@mock.patch('builtins.input', return_value='1')
def test_loop_menu_qx_for_return_string(input):
    """
    if user input is not "x" or "q" and function returns a string.
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return "string"

    assert func() == "string"


@mock.patch('builtins.input', return_value='1')
def test_loop_menu_qx_for_return_int(input):
    """
    if user input is not "x" or "q" and function returns an integer.
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return 42

    assert func() == 42


@mock.patch('builtins.input', return_value='1')
def test_loop_menu_qx_for_return_list(input):
    """
    if user input is not "x" or "q" and function returns a list.
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return ["li", "st"]
  
    assert func() == ["li", "st"]


@mock.patch('builtins.input', return_value='1')
def test_loop_menu_qx_for_return_dict(input):
    """
    if user input is not "x" or "q" and function returns a dictionary.
    """
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return {"dict": "ionary"}

    assert func() == {"dict": "ionary"}