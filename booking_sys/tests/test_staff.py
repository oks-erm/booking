from unittest.mock import patch, call
from booking_sys.staff import (create_staff, get_name, staff_menu,
                               staff_info_menu, edit_staff_menu,
                               print_staff_info)


def test_create_staff_name_returns_x():
    """
    Tests create_staff if get_name returns "x".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("booking_sys.staff.get_name",
               return_value="x") as mock_get_name:
        with patch("builtins.print") as mock_print:
            create_staff(test_data)
            mock_get_name.assert_called()
            mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~")])
            assert create_staff(test_data) is None


def test_create_staff_password_returns_x():
    """
    Tests create_staff if input for password is "x".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("booking_sys.staff.get_name",
               return_value="name") as mock_get_name:
        with patch("getpass.getpass", return_value="x") as mock_getpass:
            with patch("builtins.print") as mock_print:
                name = mock_get_name.return_value
                create_staff(test_data)
                mock_get_name.assert_called()
                mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                            call(f"Hi, {name}!")],
                                            any_order=False)
                mock_getpass.assert_called()
                assert create_staff(test_data) is None


def test_create_staff_phone_returns_x():
    """
    Tests create_staff if new_phone returns "x".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("booking_sys.staff.get_name",
               return_value="name") as mock_get_name:
        with patch("getpass.getpass", return_value="1") as mock_getpass:
            with patch("booking_sys.staff.new_phone",
                       return_value="x") as mock_phone:
                with patch("builtins.print") as mock_print:
                    name = mock_get_name.return_value
                    create_staff(test_data)
                    mock_get_name.assert_called()
                    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                                call(f"Hi, {name}!")],
                                                any_order=False)
                    mock_getpass.assert_called()
                    mock_phone.assert_called()
                    assert create_staff(test_data) is None


def test_create_staff_phone_returns_q():
    """
    Tests create_staff if new_phone returns "q".
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("booking_sys.staff.get_name",
               return_value="name") as mock_get_name:
        with patch("getpass.getpass", return_value="1") as mock_getpass:
            with patch("booking_sys.staff.new_phone",
                       return_value="q") as mock_phone:
                with patch("builtins.print") as mock_print:
                    name = mock_get_name.return_value
                    create_staff(test_data)
                    mock_get_name.assert_called()
                    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                                call(f"Hi, {name}!")],
                                                any_order=False)
                    mock_getpass.assert_called()
                    mock_phone.assert_called()
                    assert create_staff(test_data) is None


@patch("booking_sys.staff.update_worksheet", autospec=True)
def test_create_staff_completed(*args):
    """
    Tests create_staff if completed successfully.
    """
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("booking_sys.staff.get_name",
               return_value="name") as mock_get_name:
        with patch("getpass.getpass", return_value="1") as mock_getpass:
            with patch("booking_sys.staff.new_phone",
                       return_value="2") as mock_phone:
                with patch("builtins.print") as mock_print:
                    name = mock_get_name.return_value
                    create_staff(test_data)
                    result = create_staff(test_data)
                    mock_get_name.assert_called()
                    mock_print.assert_has_calls([call("\n~ ~ x - <== ~ ~"),
                                                call(f"Hi, {name}!")],
                                                any_order=False)
                    mock_getpass.assert_called()
                    mock_phone.assert_called()

                    assert mock_get_name.return_value in result.values()
                    assert mock_phone.return_value in result.values()
                    assert mock_getpass.return_value in result.values()
                    assert isinstance(create_staff(test_data), dict)


def test_get_name_empty_string():
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("builtins.input", side_effect=["", "break_loop"]) as mock_input:
        with patch("builtins.print") as mock_print:
            get_name(test_data)
            mock_input.assert_called()
            mock_print.assert_called_with("Please, enter your name!\n")


def test_get_name_existing_name():
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("builtins.input",
               side_effect=["Name1", "break_loop"]) as mock_input:
        with patch("builtins.print") as mock_print:
            get_name(test_data)
            mock_input.assert_called()
            mock_print.assert_called_with("'Name1' already "
                                          "exists. Try something else.\n")


def test_get_name_valid_name():
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    with patch("builtins.input", return_value="TestName") as mock_input:
        get_name(test_data)
        mock_input.assert_called()
        assert get_name(test_data) == mock_input.return_value


def test_staff_menu_invalid_input():
    with patch("builtins.input", return_value="0") as mock_input:
        user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
        user_input = mock_input.return_value
        assert staff_menu.__wrapped__(user_input, user) is False


def test_staff_menu_input_1():
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    with patch("builtins.input", return_value="1") as mock_input:
        with patch("booking_sys.staff.staff_info_menu") as mock_staff_info:
            with patch('booking_sys.staff.get_data') as mock_get_data:
                user_input = mock_input.return_value
                result = mock_staff_info.return_value = [{}, {}, {}]
                assert staff_menu.__wrapped__(user_input, user) == result
                mock_get_data.assert_called()


def test_staff_menu_input_2():
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    with patch("builtins.input", return_value="2") as mock_input:
        with patch("booking_sys.staff.edit_staff_menu") as mock_edit_info:
            user_input = mock_input.return_value
            result = mock_edit_info.return_value = True
            assert staff_menu.__wrapped__(user_input, user) == result


def test_staff_info_menu_invalid_input():
    with patch("builtins.input", return_value="invalid_value") as mock_input:
        test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                     {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
        user_input = mock_input.return_value
        assert staff_info_menu.__wrapped__(user_input, test_data) is False


def test_staff_info_menu_valid_input():
    with patch("builtins.input", return_value="Name1") as mock_input:
        with patch("booking_sys.staff.print_staff_info") as mock_print_info:
            test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                         {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
            user_input = mock_input.return_value
            assert staff_info_menu.__wrapped__(user_input, test_data) is True
            mock_print_info.assert_called_once()

    with patch("builtins.input", return_value="all") as mock_input:
        assert staff_info_menu.__wrapped__(user_input, test_data) is True
        mock_print_info.assert_called_once()


def test_edit_staff_menu_invalid_input():
    with patch("builtins.input", return_value="0") as mock_input:
        user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
        user_input = mock_input.return_value
        assert edit_staff_menu.__wrapped__(user_input, user) is False


def test_edit_staff_menu_input_1():
    with patch("builtins.input", return_value="1") as mock_input:
        user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
        user_input = mock_input.return_value
        with patch('booking_sys.staff.update_data') as mock_update:
            with patch('getpass.getpass') as mock_getpass:
                assert edit_staff_menu.__wrapped__(user_input, user) is True
                mock_update.assert_called()
                mock_getpass.assert_called()


def test_edit_staff_menu_input_2():
    with patch("builtins.input", return_value="2") as mock_input:
        user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
        user_input = mock_input.return_value
        with patch('booking_sys.staff.update_data') as mock_update:
            with patch('builtins.input') as mock_input:
                assert edit_staff_menu.__wrapped__(user_input, user) is True
                mock_update.assert_called()
                mock_input.assert_called()


def test_print_staff_info():
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': ''}]
    user_input = "Name1"
    all = "all"
    with patch("builtins.print") as mock_print:
        print_staff_info.__wrapped__(all, test_data)
        assert mock_print.call_count == len(test_data)

        print_staff_info.__wrapped__(user_input, test_data)
        mock_print.assert_called_with(f"\t{test_data[0]['NAME']} "
                                      f": {test_data[0]['CONTACT']}")
