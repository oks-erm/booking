from unittest.mock import patch, call
from booking_sys.customer import (search, customers_menu, view_customer,
                                  print_customer, find_customer, new_phone,
                                  new_email, new_birthdate, create_customer)


def test_search():
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': '001'},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': '002'},
                 {'NAME': 'Name3', 'PASSWORD': '333', 'CONTACT': '003'}]

    assert search("Name1", "NAME", test_data) == test_data[0]
    assert search("222", "PASSWORD", test_data) == test_data[1]
    assert search("003", "CONTACT", test_data) == test_data[2]
    assert search("Test", "NAME", test_data) is None


def test_customers_menu_invalid_input():
    with patch("builtins.input", return_value="0") as mock_input:
        assert customers_menu.__wrapped__(mock_input.return_value) is False


def test_customers_menu_input_1():
    with patch("builtins.input", return_value="1") as mock_input:
        with patch("booking_sys.customer.view_customer") as mock_view_customer:
            user_input = mock_input.return_value
            result = mock_view_customer.return_value = True
            assert customers_menu.__wrapped__(user_input) == result


def test_customers_menu_input_2():
    msg = "\tYour stats is ready! Check your Reports folder."
    with patch("builtins.input", return_value="2") as mock_input:
        with patch("booking_sys.stats.data_for_stats") as mock_data_for_stats:
            with patch("booking_sys.stats.customers_stats") as mock_stats:
                with patch("builtins.print") as mock_print:
                    user_input = mock_input.return_value
                    assert customers_menu.__wrapped__(user_input) is None
                    mock_data_for_stats.assert_called()
                    mock_stats.assert_called()
                    mock_print.assert_called_once_with(msg)


def test_view_customer_invalid_input():
    with patch("builtins.input", return_value="0") as mock_input:
        with patch("booking_sys.customer.get_data") as mock_data:
            with patch("booking_sys.customer.get_customer") as mock_customer:
                user_input = mock_input.return_value
                mock_customer.return_value = None
                assert view_customer.__wrapped__(user_input) is False
                mock_data.assert_called()
                mock_customer.assert_called()


def test_view_customer_valid_input_single():
    with patch("builtins.input", return_value="Name") as mock_input:
        with patch("booking_sys.customer.get_customer") as mock_customer:
            with patch("booking_sys.customer.print_customer") as mock_print:
                with patch("booking_sys.customer.get_data") as mock_data:
                    customer = mock_customer.return_value = {}
                    user_input = mock_input.return_value
                    assert view_customer.__wrapped__(user_input) is True
                    mock_data.assert_called()
                    mock_customer.assert_called()
                    mock_print.assert_called_with(customer)


def test_view_customer_valid_input_all():
    test_data = [{'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': '001'},
                 {'NAME': 'Name2', 'PASSWORD': '222', 'CONTACT': '002'}]
    with patch("builtins.input", return_value="all") as mock_input:
        with patch("booking_sys.customer.get_customer") as mock_customer:
            with patch("booking_sys.customer.print_customer") as mock_print:
                with patch("booking_sys.customer.get_data") as mock_data:
                    mock_customer.return_value = None
                    customers = mock_data.return_value = test_data
                    user_input = mock_input.return_value
                    assert view_customer.__wrapped__(user_input) is True
                    mock_data.assert_called()
                    mock_customer.assert_called()
                    assert mock_print.call_count == len(customers)


def test_print_customer():
    test_data = {'NAME': 'Test Name', 'PHONE': '00 11111111111',
                 'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
                 'NUM OF BOOKINGS': '14', 'CANCELLED': '8'}
    text = (f"\t{test_data['NAME']} - {test_data['PHONE']}, "
            f"birthday: {test_data['BD']}\n"
            f"\tbookings history: {test_data['NUM OF BOOKINGS']},"
            f"cancelled: {test_data['CANCELLED']}")
    with patch("builtins.print") as mock_print:
        print_customer.__wrapped__(test_data)
        mock_print.assert_called_with(text)


def test_find_customer_none_y():
    with patch("builtins.input") as mock_input:
        with patch("booking_sys.customer.get_customer") as mock_customer:
            with patch("booking_sys.customer.create_customer") as mock_create:
                with patch("builtins.print") as mock_print:
                    mock_customer.return_value = None
                    user_input = mock_input.return_value = "y"
                    new = mock_create.return_value = {"test": "test"}
                    print_1 = f"\tCustomer '{user_input}' does not exist."

                    assert find_customer.__wrapped__(user_input) == new
                    mock_print.assert_called_with(print_1)

                    new = mock_create.return_value = "x"
                    assert find_customer.__wrapped__(user_input) is True


def test_find_customer_none_n():
    with patch("builtins.input") as mock_input:
        with patch("booking_sys.customer.get_customer") as mock_customer:
            with patch("builtins.print") as mock_print:
                mock_customer.return_value = None
                user_input = mock_input.return_value = "n"
                print_1 = f"\tCustomer '{user_input}' does not exist."

                assert find_customer.__wrapped__(user_input) is None
                mock_print.assert_called_with(print_1)


def test_find_customer_exist():
    with patch("builtins.input", return_value="test") as mock_input:
        with patch("booking_sys.customer.get_customer") as mock_customer:
            res = mock_customer.return_value = {"test": "test"}
            assert find_customer.__wrapped__(mock_input.return_value) == res


def test_new_phone():
    with patch("builtins.input", return_value="test") as mock_input:
        with patch("booking_sys.validation.phone_num") as mock_phone:
            user_input = mock_input.return_value

            mock_phone.return_value = True
            assert new_phone.__wrapped__(user_input) == user_input

            mock_phone.return_value = False
            assert new_phone.__wrapped__(user_input) is False


def test_new_email():
    with patch("builtins.input", return_value="test") as mock_input:
        with patch("booking_sys.validation.email") as mock_email:
            user_input = mock_input.return_value

            mock_email.return_value = True
            assert new_email.__wrapped__(user_input) == user_input.encode('utf-8')

            mock_email.return_value = False
            assert new_email.__wrapped__(user_input) is False


def test_new_birthdate():
    with patch("builtins.input") as mock_input:
        with patch("booking_sys.validation.birthdate") as mock_bd:
            result = mock_bd.return_value = "10-10-2000"
            assert new_birthdate.__wrapped__(mock_input) == result

            mock_bd.return_value = False
            assert new_birthdate.__wrapped__(mock_input) is False


def test_create_customer_phone_returns_xq():
    """
    Tests create_customer if get_name returns "x" or "q".
    """
    name = "test"
    with patch("booking_sys.customer.new_phone") as mock_new_phone:
        with patch("builtins.print") as mock_print:
            phone = mock_new_phone.return_value = "x"
            assert create_customer(name) == phone
            mock_new_phone.assert_called()
            mock_print.assert_has_calls([call("\n\t\tCreate a new customer:")])

            phone = mock_new_phone.return_value = "q"
            assert create_customer(name) == phone


def test_create_customer_email_returns_xq():
    """
    Tests create_customer if mew_email returns "x" or "q".
    """
    name = "test"
    with patch("booking_sys.customer.new_phone") as mock_new_phone:
        with patch("booking_sys.customer.new_email") as mock_new_email:
            with patch("builtins.print") as mock_print:
                mock_new_phone.return_value = "0011111111"
                email = mock_new_email.return_value = "x"
                assert create_customer(name) == email
                mock_new_email.assert_called()
                mock_new_phone.assert_called()
                mock_print.assert_called_with("\n\t\tCreate a new customer:")

                email = mock_new_email.return_value = "q"
                assert create_customer(name) == email


def test_create_customer_birthdate_returns_xq():
    """
    Tests create_customer if new_birthdate returns "x" and "q".
    """
    name = "test"
    text = "\n\t\tCreate a new customer:"
    with patch("booking_sys.customer.new_phone") as mock_new_phone:
        with patch("booking_sys.customer.new_email") as mock_new_email:
            with patch("booking_sys.customer.new_birthdate") as mock_birthdate:
                with patch("builtins.print") as mock_print:
                    mock_new_phone.return_value = "0011111111"
                    mock_new_email.return_value = "test@te.st"
                    birthdate = mock_birthdate.return_value = "x"
                    assert create_customer(name) == birthdate
                    mock_new_email.assert_called()
                    mock_new_phone.assert_called()
                    mock_birthdate.assert_called()
                    mock_print.assert_called_with(text)

                    birthdate = mock_birthdate.return_value = "q"
                    assert create_customer(name) == birthdate


@patch("booking_sys.customer.update_worksheet", autospec=True)
def test_create_customer_completed(*args):
    """
    Tests create_customer if completed successfully.
    """
    name = "Name"
    text = "\n\t\tCreate a new customer:"
    with patch("booking_sys.customer.new_phone") as mock_new_phone:
        with patch("booking_sys.customer.new_email") as mock_new_email:
            with patch("booking_sys.customer.new_birthdate") as mock_birthdate:
                with patch("builtins.print") as mock_print:
                    phone = mock_new_phone.return_value = "0011111111"
                    email = mock_new_email.return_value = "test@te.st".encode('utf-8')
                    birthdate = mock_birthdate.return_value = "10-10-2000"
                    result = create_customer(name)

                    assert name in result.values()
                    assert phone in result.values()
                    assert email.decode('utf-8') in result.values()
                    assert birthdate in result.values()
                    assert isinstance(result, dict)
                    mock_new_email.assert_called()
                    mock_new_phone.assert_called()
                    mock_birthdate.assert_called()
                    mock_print.assert_called_with(text)
