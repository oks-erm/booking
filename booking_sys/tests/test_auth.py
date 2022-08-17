"""
Tests for auth module.
"""
from unittest import mock
from booking_sys.auth import authorise, check_password, staff_login


def test_check_password():
    """
    Test check_password on different values.
    """
    user = {'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': '001111111111'}
    password = "123"
    assert check_password(user, password) is True

    password = '111'
    assert check_password(user, password) is False

    password = ''
    assert check_password(user, password) is False


@mock.patch("getpass.getpass")
def test_authorise_seq(getpass):
    """
    Test authorisation on different sequences of values.
    """
    user = {'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': '001111111111'}
    getpass.side_effect = ["11", "123", "12"]
    assert authorise(user) is True

    getpass.side_effect = ["11", "12", "123"]
    assert authorise(user) is True

    getpass.side_effect = ["11", "12", "113"]
    assert authorise(user) is False


@mock.patch("booking_sys.staff.create_staff",
            return_value={'NAME': 'B', 'PASSWORD': '1', 'CONTACT': ''})
@mock.patch('builtins.input', return_value='new')
def test_staff_login_for_new(input, create_staff):
    """
    Tests a function for a new user.
    """
    data = [{'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': '001111111111'}]
    result = staff_login(data)
    assert isinstance(result, dict) is True
    assert result == create_staff.return_value


@mock.patch("booking_sys.auth.authorise", return_value=True)
@mock.patch('builtins.input', return_value='Bob')
def test_staff_login_for_existing(*args):
    """
    Tests a function for an existing user.
    """
    data = [{'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': '001111111111'}]
    result = staff_login(data)
    assert isinstance(result, dict) is True
    assert result == data[0]
