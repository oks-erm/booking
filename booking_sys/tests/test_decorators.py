"""
Tests for decorators module.
"""
from unittest import mock
from booking_sys.decorators import loop_menu_qx


def test_loop_menu_qx_for_x():
    """
    if user input is "x".
    """
    @mock.patch('builtins.input', return_value='x')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func():
        return True

    assert func() == "x"


def test_loop_menu_qx_for_q():
    """
    if user input is "q".
    """
    @mock.patch('builtins.input', return_value='q')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func():
        return True

    assert func() == "q"


def test_loop_menu_qx_for_input_return_true():
    """
    if user input is not "x" or "q" and function returns True.
    """
    @mock.patch('builtins.input', return_value='1')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return True

    assert func() is None


def test_loop_menu_qx_for_input_return_q():
    """
    if user input is not "x" or "q" and function returns "q".
    """
    @mock.patch('builtins.input', return_value='1')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return "q"

    assert func() == "q"


def test_loop_menu_qx_for_return_string():
    """
    if user input is not "x" or "q" and function returns a string.
    """
    @mock.patch('builtins.input', return_value='1')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return "string"

    assert func() == "string"


def test_loop_menu_qx_for_return_int():
    """
    if user input is not "x" or "q" and function returns an integer.
    """
    @mock.patch('builtins.input', return_value='1')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return 42

    assert func() == 42


def test_loop_menu_qx_for_return_list():
    """
    if user input is not "x" or "q" and function returns a list.
    """
    @mock.patch('builtins.input', return_value='1')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return ["li", "st"]

    assert func() == ["li", "st"]


def test_loop_menu_qx_for_return_dict():
    """
    if user input is not "x" or "q" and function returns a dictionary.
    """
    @mock.patch('builtins.input', return_value='1')
    @loop_menu_qx("indentation", "qx_text", "input_prompt", "warning")
    def func(*args):
        return {"dict": "ionary"}

    assert func() == {"dict": "ionary"}
