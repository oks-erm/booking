"""
Tests for run module.
"""
import os
from unittest.mock import patch
from run import start_menu, cleanup


@patch("sys.exit")
@patch("builtins.input")
@patch("builtins.print")
def test_start_menu_invalid_input(*args):
    """
    Tests start_menu() if user input is invalid.
    """
    (mock_print, mock_input, mock_exit) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    msg = "Computer says no. Please, use options above."
    mock_exit.return_value = False
    mock_input.side_effect = ["invalid", "x"]

    start_menu(user)
    mock_print.assert_called_with(msg)


@patch("sys.exit")
@patch("run.booking.bookings_menu")
@patch("builtins.input")
@patch("builtins.print")
def test_start_menu_input_1(*args):
    """
    Tests start_menu() if user input is "1".
    """
    (mock_print, mock_input, mock_bookings, mock_exit) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    msg = f"What do you want to do, {user['NAME']}?"
    mock_exit.return_value = False
    mock_input.side_effect = ["1", "x"]

    start_menu(user)
    mock_print.assert_called_with(msg)
    mock_bookings.assert_called_with(user)


@patch("sys.exit")
@patch("run.customer.customers_menu")
@patch("builtins.input")
@patch("builtins.print")
def test_start_menu_input_2(*args):
    """
    Tests start_menu() if user input is "2".
    """
    (mock_print, mock_input, mock_customer, mock_exit) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    msg = f"What do you want to do, {user['NAME']}?"
    mock_exit.return_value = False
    mock_input.side_effect = ["2", "x"]

    start_menu(user)
    mock_print.assert_called_with(msg)
    mock_customer.assert_called_with()


@patch("sys.exit")
@patch("booking_sys.staff.staff_menu")
@patch("builtins.input")
@patch("builtins.print")
def test_start_menu_input_3(*args):
    """
    Tests start_menu() if user input is "3".
    """
    (mock_print, mock_input, mock_staff, mock_exit) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    msg = f"What do you want to do, {user['NAME']}?"
    mock_exit.return_value = False
    mock_input.side_effect = ["3", "x"]

    start_menu(user)
    mock_print.assert_called_with(msg)
    mock_staff.assert_called_with(user)


@patch("sys.exit")
@patch("run.cleanup")
@patch("builtins.input")
@patch("builtins.print")
def test_start_menu_input_x(*args):
    """
    Tests start_menu() if user input is "2".
    """
    (mock_print, mock_input, mock_cleanup, mock_exit) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    msg = f"What do you want to do, {user['NAME']}?"
    mock_exit.return_value = False
    mock_input.return_value = "x"

    start_menu(user)
    mock_print.assert_called_with(msg)
    mock_cleanup.assert_called()
    mock_exit.assert_called()


def test_cleanup():
    """
    Tests cleanup().
    """
    cleanup()
    assert os.path.exists("stats.csv") is False
    assert os.path.exists("stats.pdf") is False
