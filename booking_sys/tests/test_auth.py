"""
Tests for auth module.
"""
from unittest import mock
from booking_sys.auth import authorise, check_password, staff_login


def test_check_password():
    """
    Tests check_password on different values.
    """
    user = {'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': ''}
    password = "123"
    assert check_password(user, password) is True

    password = '111'
    assert check_password(user, password) is False

    password = ''
    assert check_password(user, password) is False


@mock.patch("getpass.getpass")
def test_authorise_seq(getpass):
    """
    Tests authorisation on different sequences of values.
    """
    user = {'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': ''}
    getpass.side_effect = ["11", "123", "12"]
    assert authorise(user) is True

    getpass.side_effect = ["11", "12", "123"]
    assert authorise(user) is True

    getpass.side_effect = ["11", "12", "113"]
    assert authorise(user) is False


@mock.patch("booking_sys.staff.create_staff")
@mock.patch('builtins.input')
def test_staff_login_for_new(*args):
    """
    Tests a function for a new user.
    """
    (mock_input, mock_create) = args
    mock_input.return_value = 'new'
    mock_create.return_value = {'NAME': 'B', 'PASSWORD': '1', 'CONTACT': ''}
    data = [{'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': ''}]
    result = staff_login(data)

    assert isinstance(result, dict) is True
    mock_input.assert_called()
    mock_create.assert_called()
    assert result == mock_create.return_value


@mock.patch("booking_sys.auth.authorise")
@mock.patch('builtins.input')
def test_staff_login_for_existing(*args):
    """
    Tests a function for an existing user.
    """
    (mock_input, mock_auth) = args
    mock_input.return_value = 'Bob'
    mock_auth.return_value = True
    data = [{'NAME': 'Bob', 'PASSWORD': '123', 'CONTACT': ''}]
    result = staff_login(data)

    assert isinstance(result, dict) is True
    mock_input.assert_called()
    mock_auth.assert_called()
    assert result == data[0]
