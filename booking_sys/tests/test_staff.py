from unittest.mock import patch, call
from booking_sys.staff import (create_staff, get_name, staff_menu,
                               staff_info_menu, edit_staff_menu,
                               print_staff_info)


@patch("booking_sys.staff.get_name")
@patch("builtins.print")
def test_create_staff_name_returns_x(*args):
    """
    Tests create_staff() if get_name returns "x".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_print, mock_get_name) = args
    mock_get_name.return_value = "x"

    assert create_staff(test_data) is None
    mock_get_name.assert_called()
    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~")])


@patch("getpass.getpass")
@patch("booking_sys.staff.get_name")
@patch("builtins.print")
def test_create_staff_password_returns_x(*args):
    """
    Tests create_staff() if input for password is "x".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_print, mock_get_name, mock_getpass) = args

    name = mock_get_name.return_value = "name"
    mock_getpass.return_value = "x"

    assert create_staff(test_data) is None
    mock_get_name.assert_called()
    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                call(f"Hi, {name}!")],
                                any_order=False)
    mock_getpass.assert_called()


@patch("booking_sys.staff.new_phone")
@patch("getpass.getpass")
@patch("booking_sys.staff.get_name")
@patch("builtins.print")
def test_create_staff_phone_returns_x(*args):
    """
    Tests create_staff() if new_phone returns "x".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_print, mock_get_name, mock_getpass, mock_phone) = args

    name = mock_get_name.return_value = "name"
    mock_getpass.return_value = "1"
    mock_phone.return_value = "x"

    assert create_staff(test_data) is None
    mock_get_name.assert_called()
    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                call(f"Hi, {name}!")],
                                any_order=False)
    mock_getpass.assert_called()
    mock_phone.assert_called()


@patch("booking_sys.staff.new_phone")
@patch("getpass.getpass")
@patch("booking_sys.staff.get_name")
@patch("builtins.print")
def test_create_staff_phone_returns_q(*args):
    """
    Tests create_staff() if new_phone returns "x".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_print, mock_get_name, mock_getpass, mock_phone) = args

    name = mock_get_name.return_value = "name"
    mock_getpass.return_value = "1"
    mock_phone.return_value = "q"

    assert create_staff(test_data) is None
    mock_get_name.assert_called()
    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                call(f"Hi, {name}!")],
                                any_order=False)
    mock_getpass.assert_called()
    mock_phone.assert_called()


@patch("booking_sys.staff.update_worksheet", autospec=True)
@patch("booking_sys.staff.new_phone")
@patch("getpass.getpass")
@patch("booking_sys.staff.get_name")
@patch("builtins.print")
def test_create_staff_completed(*args):
    """
    Tests create_staff() if completed successfully.
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_print, mock_get_name, mock_getpass, mock_phone, mock_update) = args

    name = mock_get_name.return_value = "name"
    mock_getpass.return_value = "1"
    mock_phone.return_value = "001111111111"
    result = create_staff(test_data)

    assert isinstance(result, dict) is True
    assert mock_get_name.return_value in result.values()
    assert mock_phone.return_value in result.values()
    assert mock_getpass.return_value in result.values()
    mock_get_name.assert_called()
    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                call(f"Hi, {name}!")],
                                any_order=False)
    mock_getpass.assert_called()
    mock_phone.assert_called()
    mock_update.assert_called()


@patch("builtins.print")
@patch("builtins.input")
def test_get_name_empty_string(*args):
    """
    Test get_name() if user input is an empty string.
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_input, mock_print) = args
    mock_input.side_effect = ["", "break_loop"]

    get_name(test_data)
    mock_input.assert_called()
    mock_print.assert_called_with("Please, enter your name!\n")


@patch("builtins.print")
@patch("builtins.input")
def test_get_name_existing_name(*args):
    """
    Test get_name() if user input is an existing name.
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_input, mock_print) = args
    mock_input.side_effect = ["Name1", "break_loop"]

    get_name(test_data)
    mock_input.assert_called()
    mock_print.assert_called_with("'Name1' already "
                                  "exists. Try something else.\n")


@patch("builtins.print")
@patch("builtins.input")
def test_get_name_valid_name(*args):
    """
    Test get_name() if user input is valid and
    name does not exist in provided data.
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    (mock_input, mock_print) = args
    mock_input.return_value = "TestName"

    assert get_name(test_data) == mock_input.return_value
    mock_input.assert_called()
    mock_print.assert_not_called()


@patch("builtins.input")
def test_staff_menu_invalid_input(*args):
    """
    Test staff_menu() if user input is invalid.
    """
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    (mock_input, ) = args
    user_input = mock_input.return_value = "0"

    assert staff_menu.__wrapped__(user_input, user) is False


@patch("booking_sys.staff.staff_info_menu")
@patch('booking_sys.staff.get_data')
@patch("builtins.input")
def test_staff_menu_input_1(*args):
    """
    Test staff_menu() if user input is "1".
    """
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    (mock_input, mock_get_data, mock_staff_info) = args
    user_input = mock_input.return_value = "1"
    result = mock_staff_info.return_value = [{}, {}, {}]

    assert staff_menu.__wrapped__(user_input, user) == result
    mock_get_data.assert_called()


@patch("booking_sys.staff.edit_staff_menu")
@patch("builtins.input")
def test_staff_menu_input_2(*args):
    """
    Test staff_menu() if user input is "2".
    """
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    (mock_input, mock_edit_info) = args
    user_input = mock_input.return_value = "2"
    result = mock_edit_info.return_value = True

    assert staff_menu.__wrapped__(user_input, user) == result
    mock_edit_info.assert_called()


@patch("builtins.input")
def test_staff_info_menu_invalid_input(*args):
    """
    Test staff_info_menu() if user input is invalid.
    """
    (mock_input, ) = args
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    user_input = mock_input.return_value = "invalid_value"

    assert staff_info_menu.__wrapped__(user_input, test_data) is False


@patch("booking_sys.staff.print_staff_info")
@patch("builtins.input")
def test_staff_info_menu_valid_input(*args):
    """
    Test staff_info_menu() if user input is valid.
    """
    (mock_input, mock_print_info) = args
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]

    user_input = mock_input.return_value = "Name1"
    assert staff_info_menu.__wrapped__(user_input, test_data) is True
    mock_print_info.assert_called()

    user_input = mock_input.return_value = "all"
    assert staff_info_menu.__wrapped__(user_input, test_data) is True
    mock_print_info.assert_called()


@patch("builtins.input")
def test_edit_staff_menu_invalid_input(*args):
    """
    Test edit_staff_menu() if user input is invalid.
    """
    (mock_input, ) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}

    user_input = mock_input.return_value = "0"
    assert edit_staff_menu.__wrapped__(user_input, user) is False


@patch('booking_sys.staff.update_data')
@patch('getpass.getpass')
@patch("builtins.input")
def test_edit_staff_menu_input_1(*args):
    """
    Test edit_staff_menu() if user input is "1".
    """
    (mock_input, mock_getpass, mock_update) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    user_input = mock_input.return_value = "1"

    assert edit_staff_menu.__wrapped__(user_input, user) is True
    mock_update.assert_called()
    mock_getpass.assert_called()


@patch('booking_sys.staff.update_data')
@patch("builtins.input", return_value="2")
def test_edit_staff_menu_input_2(*args):
    """
    Test edit_staff_menu() if user input is "2".
    """
    (mock_input, mock_update) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}

    user_input = mock_input.return_value
    assert edit_staff_menu.__wrapped__(user_input, user) is True
    mock_update.assert_called()
    mock_input.assert_called_with("\n\t\tEnter new contact: ")


@patch('booking_sys.staff.search')
@patch("builtins.print")
def test_print_staff_info(*args):
    """
    Test print_staff_info() with differetn arguments.
    """
    (mock_print, mock_search) = args
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    user_input = "Name1"
    all_ = "all"
    mock_search.return_value = test_data[0]

    print_staff_info.__wrapped__(all_, test_data)
    assert mock_print.call_count == len(test_data)

    print_staff_info.__wrapped__(user_input, test_data)
    mock_search.assert_called()
    mock_print.assert_called_with(f"\t{test_data[0]['NAME']} "
                                  f": {test_data[0]['CONTACT']}")
