"""
Tests for booking module.
"""
from unittest.mock import patch, call
from datetime import date, timedelta
import re
from booking_sys.booking import (dd_mm_yyyy, active, confirmed, cust_bookings,
                                 bookings_menu, view_bookings_menu,
                                 print_bookings, new_date, new_time,
                                 num_of_people, new_booking, to_confirm,
                                 edit_bookings, confirm, update_date,
                                 reschedule, find_bookings, has_duplicates,
                                 pick_booking, cancel, increment_bookings)


# test data
config = {"side_effect": (lambda x: re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
          '\\3-\\2-\\1', x))}
today = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
               '\\3-\\2-\\1', str(date.today()))
tomorrow = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                  '\\3-\\2-\\1', str((date.today() + timedelta(days=1))))
future = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                '\\3-\\2-\\1', (str(date.today() + timedelta(days=10))))
test_data = [{'DATE': tomorrow, 'TIME': '20:00',
              'NAME': 'Name1', 'PEOPLE': '1', 'CREATED': "Bob",
              'CONF': 'yes', 'CANC': ''},
             {'DATE': today, 'TIME': '20:00',
              'NAME': 'Name2', 'PEOPLE': '2', 'CREATED': "Bob",
              'CONF': '', 'CANC': ''},
             {'DATE': future, 'TIME': '20:00',
              'NAME': 'Name3', 'PEOPLE': '3', 'CREATED': "Bob",
              'CONF': '', 'CANC': 'yes'}]
customers = [{'NAME': 'Name1', 'PHONE': '00 11111111111',
              'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
              'NUM OF BOOKINGS': '14', 'CANCELLED': '8'},
             {'NAME': 'Name2', 'PHONE': '00 2222222222',
              'EMAIL': 'test@ma.il', 'BD': '24-06-2000',
              'NUM OF BOOKINGS': '1', 'CANCELLED': '0'}]
customer_bookings = [{'DATE': tomorrow, 'TIME': '20:00',
                      'NAME': 'Name10', 'PEOPLE': '1', 'CREATED': "Bob",
                      'CONF': 'yes', 'CANC': ''},
                     {'DATE': today, 'TIME': '20:00',
                      'NAME': 'Name10', 'PEOPLE': '2', 'CREATED': "Bob",
                      'CONF': '', 'CANC': ''}]


def test_dd_mm_yyyy():
    """
    Test dd_mm_yyyy with different formats and types of data.
    """
    assert dd_mm_yyyy("2022-08-20") == "20-08-2022"
    assert dd_mm_yyyy("2022/08/20") == "2022/08/20"
    assert dd_mm_yyyy(["2022/08/20"]) is None
    assert dd_mm_yyyy({"a": "b"}) is None
    assert dd_mm_yyyy(42) is None
    assert dd_mm_yyyy(None) is None
    assert dd_mm_yyyy(True) is None


def test_active():
    """
    Test active with different formats and types of data.
    """
    test = [{'DATE': '10-10-2022', 'TIME': '20:00',
             'NAME': 'Name', 'PEOPLE': '1', 'CREATED': "Bob",
             'CONF': '', 'CANC': ''},
            {'DATE': '10-05-2022', 'TIME': '20:00',
             'NAME': 'Name', 'PEOPLE': '2', 'CREATED': "Bob",
             'CONF': '', 'CANC': ''},
            {'DATE': '12-09-2022', 'TIME': '20:00',
             'NAME': 'Name', 'PEOPLE': '2', 'CREATED': "Bob",
             'CONF': '', 'CANC': 'yes'}]
    assert active(test) == [test[0]]
    assert active({"a": "b"}) is None
    assert active(42) is None
    assert active("string") is None
    assert active(None) is None
    assert active(True) is None


def test_confirmed():
    """
    Test confirmed with different formats and types of data.
    """
    test_data_conf = {'DATE': '10-10-2022', 'TIME': '20:00',
                      'NAME': 'Name', 'PEOPLE': '1', 'CREATED': "Bob",
                      'CONF': 'yes', 'CANC': ''}
    test_data_not_conf = {'DATE': '10-10-2022', 'TIME': '20:00',
                          'NAME': 'Name', 'PEOPLE': '1', 'CREATED': "Bob",
                          'CONF': '', 'CANC': ''}
    assert confirmed(test_data_conf) == "\\/"
    assert confirmed(test_data_not_conf) == "--"
    assert active(["a"]) is None
    assert active(42) is None
    assert active("string") is None
    assert active(None) is None
    assert active(True) is None


@patch("booking_sys.booking.active")
@patch("booking_sys.booking.get_data")
def test_cust_bookings(*args):
    """
    Test cust_bookings with different formats and types of data.
    """
    (mock_data, mock_active) = args
    data = [{'DATE': '10-10-2022', 'TIME': '20:00',
             'NAME': 'Name1', 'PEOPLE': '1', 'CREATED': "Bob",
             'CONF': '', 'CANC': ''},
            {'DATE': '10-05-2022', 'TIME': '20:00',
             'NAME': 'Name2', 'PEOPLE': '2', 'CREATED': "Bob",
             'CONF': '', 'CANC': ''},
            {'DATE': '12-09-2022', 'TIME': '20:00',
             'NAME': 'Name1', 'PEOPLE': '2', 'CREATED': "Bob",
             'CONF': '', 'CANC': 'yes'}]
    mock_active.return_value = data
    name = "Name1"

    assert cust_bookings(name) == [data[0], data[2]]
    mock_active.assert_called()
    mock_data.assert_called()
    assert cust_bookings({"a": 1}) == []
    assert cust_bookings(42) == []
    assert cust_bookings("string") == []
    assert cust_bookings(None) == []
    assert cust_bookings(True) == []


def test_bookings_menu_invalid_input():
    """
    Test bookings_menu if user input is invalid.
    """
    with patch("builtins.input", return_value="0") as mock_input:
        user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
        user_input = mock_input.return_value
        assert bookings_menu.__wrapped__(user_input, user) is False


@patch("booking_sys.booking.view_bookings_menu")
@patch("builtins.input")
def test_bookings_menu_input_1(*args):
    """
    Test bookings_menu if user input is "1".
    """
    (mock_input, mock_view) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    mock_input.return_value = "1"

    user_input = mock_input.return_value
    result = mock_view.return_value = True
    assert bookings_menu.__wrapped__(user_input, user) == result


@patch("booking_sys.booking.new_booking")
@patch("booking_sys.booking.find_customer")
@patch("builtins.input")
def test_bookings_menu_input_2(*args):
    """
    Test bookings_menu if user input is "2".
    """
    (mock_input, mock_find, mock_new) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    user_input = mock_input.return_value = "2"

    result = mock_find.return_value = "x"
    assert bookings_menu.__wrapped__(user_input, user) == result
    mock_find.assert_called()

    result = mock_find.return_value = "q"
    assert bookings_menu.__wrapped__(user_input, user) == result
    mock_find.assert_called()

    result = mock_find.return_value = None
    assert bookings_menu.__wrapped__(user_input, user) == result
    mock_find.assert_called()

    result = mock_new.return_value = None
    assert bookings_menu.__wrapped__(user_input, user) == result


@patch("booking_sys.booking.edit_bookings")
@patch("builtins.input")
def test_bookings_menu_input_3(*args):
    """
    Test bookings_menu if user input is "3".
    """
    (mock_input, mock_edit) = args
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    user_input = mock_input.return_value = "3"

    result = mock_edit.return_value = None
    assert bookings_menu.__wrapped__(user_input, user) == result


@patch("booking_sys.booking.active")
@patch("booking_sys.booking.dd_mm_yyyy")
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_view_bookings_menu_invalid_input(*args):
    """
    Test view_bookings_menu if user input is invalid.
    """
    (mock_input, mock_get_data, mock_dd_mm_yyyy, mock_active) = args
    user_input = mock_input.return_value = "0"
    mock_active.return_value = []
    mock_dd_mm_yyyy.return_value = ""

    assert view_bookings_menu.__wrapped__(user_input) is False
    mock_get_data.assert_called()
    mock_active.assert_called()
    mock_dd_mm_yyyy.assert_called()


@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.active")
@patch("booking_sys.booking.dd_mm_yyyy", **config)
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_view_bookings_menu_input_1(*args):
    """
    Test view_bookings_menu if user input is "1".
    """
    (mock_input, mock_get_data, mock_ddmmyyyy, mock_active, mock_print) = args
    mock_active.return_value = test_data

    user_input = mock_input.return_value = "1"
    assert view_bookings_menu.__wrapped__(user_input) is True
    mock_get_data.assert_called()
    mock_active.assert_called()
    mock_ddmmyyyy.assert_called()
    mock_print.assert_called_with(test_data, today, "today")


@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.active")
@patch("booking_sys.booking.dd_mm_yyyy", **config)
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_view_bookings_menu_input_2(*args):
    """
    Test view_bookings_menu if user input is "2".
    """
    (mock_input, mock_get_data, mock_ddmmyyyy, mock_active, mock_print) = args
    mock_active.return_value = test_data

    user_input = mock_input.return_value = "2"
    assert view_bookings_menu.__wrapped__(user_input) is True
    mock_get_data.assert_called()
    mock_active.assert_called()
    mock_ddmmyyyy.assert_called()
    mock_print.assert_called_with(test_data, tomorrow, "tomorrow")


@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.active")
@patch("booking_sys.booking.dd_mm_yyyy", **config)
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_view_bookings_menu_input_3(*args):
    """
    Test view_bookings_menu if user input is "3".
    """
    (mock_input, mock_get_data, mock_ddmmyyyy, mock_active, mock_print) = args
    mock_active.return_value = test_data

    user_input = mock_input.return_value = "3"
    week = [today]
    for i in range(1, 7):
        week.append(dd_mm_yyyy(str(date.today() + timedelta(days=i))))
    assert view_bookings_menu.__wrapped__(user_input) is True
    mock_get_data.assert_called()
    mock_active.assert_called()
    mock_ddmmyyyy.assert_called()
    mock_print.assert_called_with(test_data, week, 'the upcoming week')


@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.active")
@patch("booking_sys.booking.dd_mm_yyyy", **config)
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_view_bookings_menu_input_4(*args):
    """
    Test view_bookings_menu if user input is "4".
    """
    (mock_input, mock_get_data, mock_ddmmyyyy, mock_active, mock_print) = args
    mock_active.return_value = test_data

    user_input = mock_input.return_value = "4"
    assert view_bookings_menu.__wrapped__(user_input) is True
    mock_get_data.assert_called()
    mock_active.assert_called()
    mock_ddmmyyyy.assert_called()
    mock_print.assert_called_with(test_data, [tomorrow, today, future],
                                  "all time")


@patch("booking_sys.booking.get_customer")
@patch("builtins.print")
def test_print_bookings(*args):
    """
    Test print_bookings if booking is confirmed.
    """
    (mock_print, mock_customer) = args
    test_data_conf = [{'DATE': today, 'TIME': '20:00', 'NAME': 'Name2',
                       'PEOPLE': '2', 'CREATED': "Bob", 'CONF': 'yes',
                       'CANC': ''}]
    mock_customer.return_value = {'NAME': 'Name2', 'PHONE': '00 11111111111',
                                  'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
                                  'NUM OF BOOKINGS': '14', 'CANCELLED': '8'}

    print_bookings.__wrapped__(test_data, tomorrow, "tomorrow")
    print_bookings.__wrapped__(test_data_conf, today, "today")
    exp_calls = [call("\tYou have 1 booking(s) for tomorrow:\n"),
                 call(f"\t{tomorrow[:5]} - 20:00 - Name1 (1 ppl) "
                      "added by Bob \\/"),
                 call("\tYou have 1 booking(s) for today:\n"),
                 call(f"\t{today[:5]} - 20:00 - Name2 (2 ppl) "
                      "added by Bob \\/")]
    mock_print.assert_has_calls(exp_calls)


@patch("booking_sys.booking.get_customer")
@patch("builtins.print")
def test_print_bookings_not_conf(*args):
    """
    Test print_bookings if booking is not confirmed.
    """
    (mock_print, mock_customer) = args
    mock_customer.return_value = {'NAME': 'Name2', 'PHONE': '00 11111111111',
                                  'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
                                  'NUM OF BOOKINGS': '14', 'CANCELLED': '8'}

    print_bookings.__wrapped__(test_data, today, "today")
    exp_call = [call("\tYou have 1 booking(s) for today:\n"),
                call(f"\t{today[:5]} - 20:00 - Name2 (2 ppl) added by Bob --"),
                call("\t!!! confirm this booking: 00 11111111111\n")]
    mock_print.assert_has_calls(exp_call)


@patch("booking_sys.booking.has_duplicates")
@patch("booking_sys.booking.valid.date_input")
@patch("builtins.input")
def test_new_date_invalid_input(*args):
    """
    Test new_date if user input is invalid.
    """
    (mock_input, mock_date, mock_dup) = args
    cust = {'NAME': 'Test Name'}
    mock_date.return_value = False
    mock_dup.return_value = False

    assert new_date.__wrapped__(mock_input, cust) is False
    mock_date.assert_called()
    mock_dup.assert_called()


@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.get_data")
@patch("booking_sys.booking.active")
@patch("booking_sys.booking.has_duplicates")
@patch("booking_sys.booking.valid.date_input")
@patch("builtins.input")
def test_new_date_valid_input(*args):
    """
    Test new_date if user input is valid.
    """
    (mock_input, mock_date, mock_dup, mock_active,
     mock_get_data, mock_print) = args
    cust = {'NAME': 'Test Name'}
    user_input = mock_input.return_value = "10-10-2022"
    valid = mock_date.return_value = "10-10-2022"
    mock_dup.return_value = False
    bookings = mock_active.return_value = []

    assert new_date.__wrapped__(user_input, cust) == valid
    mock_date.assert_called()
    mock_dup.assert_called()
    mock_active.assert_called()
    mock_get_data.assert_called()
    mock_print.assert_called_with(bookings, valid, valid)

    mock_dup.return_value = True
    assert new_date.__wrapped__(user_input, cust) is None


@patch("booking_sys.booking.valid.time_input")
@patch("builtins.input")
def test_new_time_invalid_input(*args):
    """
    Test new_time if user input is invalid.
    """
    (mock_input, mock_time) = args
    mock_time.return_value = False

    assert new_time.__wrapped__(mock_input) is False
    mock_time.assert_called()


@patch("booking_sys.booking.valid.time_input")
@patch("builtins.input")
def test_new_time_valid_input(*args):
    """
    Test new_time if user input is valid.
    """
    (mock_input, mock_time) = args
    user_input = mock_input.return_value = "10:00"
    mock_time.return_value = True

    assert new_time.__wrapped__(user_input) == user_input
    mock_time.assert_called()


def test_num_of_people_invalid_input():
    """
    Test num_of_people if user input is invalid.
    """
    with patch("builtins.input") as mock_input:
        user_input = mock_input.return_value = "test"
        assert num_of_people.__wrapped__(user_input) is False


def test_num_of_people_valid_input():
    """
    Test num_of_people if user input is valid.
    """
    with patch("builtins.input") as mock_input:
        user_input = mock_input.return_value = "2"
        assert num_of_people.__wrapped__(user_input) == int(user_input)


def test_new_booking_date_returns_qx():
    """
    Test new_booking if new_date returns "x" or "q".
    """
    customer = {'NAME': 'Customer', 'PHONE': '00 11111111111',
                'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
                'NUM OF BOOKINGS': '14', 'CANCELLED': '8'}
    user = {'NAME': 'Staff', 'PASSWORD': '111', 'CONTACT': ''}

    with patch("booking_sys.booking.new_date") as mock_date:
        day = mock_date.return_value = "x"
        assert new_booking(user, customer) == day

        day = mock_date.return_value = "q"
        assert new_booking(user, customer) == day


@patch("booking_sys.booking.new_time")
@patch("booking_sys.booking.new_date")
def test_new_booking_time_returns_qx(*args):
    """
    Test new_booking if new_time returns "x" or "q".
    """
    (mock_date, mock_time) = args
    customer = {'NAME': 'Customer', 'PHONE': '00 11111111111',
                'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
                'NUM OF BOOKINGS': '14', 'CANCELLED': '8'}
    user = {'NAME': 'Staff', 'PASSWORD': '111', 'CONTACT': ''}
    mock_date.return_value = "12-12-2022"

    time = mock_time.return_value = "x"
    assert new_booking(user, customer) == time

    time = mock_time.return_value = "q"
    assert new_booking(user, customer) == time


@patch("booking_sys.booking.num_of_people")
@patch("booking_sys.booking.new_time")
@patch("booking_sys.booking.new_date")
def test_new_booking_num_of_people_returns_qx(*args):
    """
    Test new_booking if num_of_people returns "x" or "q".
    """
    (mock_date, mock_time, mock_ppl) = args
    customer = {'NAME': 'Customer', 'PHONE': '00 11111111111',
                'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
                'NUM OF BOOKINGS': '14', 'CANCELLED': '8'}
    user = {'NAME': 'Staff', 'PASSWORD': '111', 'CONTACT': ''}
    mock_date.return_value = "12-12-2022"
    mock_time.return_value = "20:00"

    ppl = mock_ppl.return_value = "x"
    assert new_booking(user, customer) == ppl

    ppl = mock_ppl.return_value = "q"
    assert new_booking(user, customer) == ppl


@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.increment_bookings")
@patch("booking_sys.booking.update_worksheet")
@patch("booking_sys.booking.num_of_people", return_value="2")
@patch("booking_sys.booking.new_time", return_value="20:00")
@patch("booking_sys.booking.new_date", return_value="12-12-2022")
def test_new_booking_completed(*args):
    """
    Test new_booking if completed.
    """
    (mock_date, mock_time, mock_ppl, mock_upd,
     mock_increment, mock_print) = args
    customer = {'NAME': 'Customer', 'PHONE': '00 11111111111',
                'EMAIL': 'mail@te.st', 'BD': '14-03-1967',
                'NUM OF BOOKINGS': '14', 'CANCELLED': '8'}
    user = {'NAME': 'Staff', 'PASSWORD': '111', 'CONTACT': ''}
    expected_call = [{'DATE': '12-12-2022', 'TIME': '20:00',
                      'NAME': 'Customer', 'PEOPLE': '2',
                      'CREATED': 'Staff', 'CONF': '-', 'CANC': ''}]

    assert new_booking(user, customer) is None
    mock_date.assert_called()
    mock_time.assert_called()
    mock_ppl.assert_called()
    mock_upd.assert_called()
    mock_increment.assert_called_with(customer)
    mock_print.assert_called_with(expected_call, '12-12-2022', '12-12-2022')


def test_to_confirm():
    """
    Test to_confirm.
    """
    test_data_not_conf = [{'DATE': today, 'TIME': '20:00',
                           'NAME': 'Name1', 'PEOPLE': '1', 'CREATED': "Bob",
                           'CONF': 'yes', 'CANC': ''},
                          {'DATE': today, 'TIME': '20:00',
                           'NAME': 'Name2', 'PEOPLE': '2', 'CREATED': "Bob",
                           'CONF': '', 'CANC': ''}]
    test_data_conf = [{'DATE': today, 'TIME': '20:00',
                      'NAME': 'Name2', 'PEOPLE': '2', 'CREATED': "Bob",
                       'CONF': 'yes', 'CANC': ''}]

    assert to_confirm(test_data_not_conf) == [test_data[1]]
    assert to_confirm(test_data_conf) is None


def test_edit_bookings_invalid_input():
    """
    Test edit_bookings if user input is invalid.
    """
    with patch("builtins.input") as mock_input:
        user_input = mock_input.return_value = "0"
        assert edit_bookings.__wrapped__(user_input) is False


@patch('booking_sys.booking.confirm')
@patch('booking_sys.booking.to_confirm')
@patch('booking_sys.booking.active')
@patch('booking_sys.booking.get_data')
def test_edit_bookings_input_1(*args):
    """
    Test edit_bookings if user input is "1".
    """
    mock_data, mock_active, mock_to_confirm, mock_confirm = (args)
    with patch("builtins.input") as mock_input:
        user_input = mock_input.return_value = "1"
        result = mock_confirm.return_value = [{}]
        assert edit_bookings.__wrapped__(user_input) == result
        mock_data.assert_called()
        mock_active.assert_called()
        mock_to_confirm.assert_called()


@patch('booking_sys.booking.reschedule')
@patch('booking_sys.booking.find_bookings')
@patch("builtins.input")
def test_edit_bookings_input_2(*args):
    """
    Test edit_bookings if user input is "2".
    """
    mock_input, mock_find, mock_reschedule = (args)

    user_input = mock_input.return_value = "2"
    mock_find.return_value = "x"
    assert edit_bookings.__wrapped__(user_input) is None
    mock_find.assert_called()

    mock_find.return_value = 0
    assert edit_bookings.__wrapped__(user_input) is None
    mock_find.assert_called()

    mock_find.return_value = None
    assert edit_bookings.__wrapped__(user_input) is None
    mock_find.assert_called()

    resut = mock_find.return_value = "q"
    assert edit_bookings.__wrapped__(user_input) == resut
    mock_find.assert_called()

    mock_find.return_value = {}
    result = mock_reschedule.return_value = None
    assert edit_bookings.__wrapped__(user_input) == result
    mock_find.assert_called()
    mock_reschedule.assert_called()


@patch('booking_sys.booking.cancel')
@patch('booking_sys.booking.find_bookings')
@patch("builtins.input")
def test_edit_bookings_input_3(*args):
    """
    Test edit_bookings if user input is "3".
    """
    mock_input, mock_find, mock_cancel = (args)

    user_input = mock_input.return_value = "3"
    mock_find.return_value = "x"
    assert edit_bookings.__wrapped__(user_input) is None
    mock_find.assert_called()

    mock_find.return_value = 0
    assert edit_bookings.__wrapped__(user_input) is None
    mock_find.assert_called()

    mock_find.return_value = None
    assert edit_bookings.__wrapped__(user_input) is None
    mock_find.assert_called()

    resut = mock_find.return_value = "q"
    assert edit_bookings.__wrapped__(user_input) == resut
    mock_find.assert_called()

    mock_find.return_value = {}
    result = mock_cancel.return_value = True
    assert edit_bookings.__wrapped__(user_input) == result
    mock_find.assert_called()
    mock_cancel.assert_called()


def test_confirm():
    """
    Test confirm if the argument is None.
    """
    assert confirm(None) is None


@patch("booking_sys.booking.update_data")
@patch("builtins.input")
@patch("booking_sys.booking.print_bookings")
def test_confirm_input_1(*args):
    """
    Test confirm if the argument is not None, not empty and user input is "1".
    """
    (mock_print, mock_input, mock_upd) = args
    test_data_to_conf = [{'DATE': today, 'TIME': '20:00', 'NAME': 'Name1',
                          'PEOPLE': '1', 'CREATED': "Bob", 'CONF': '',
                          'CANC': ''}]
    mock_input.return_value = "1"

    assert confirm(test_data_to_conf) is None
    mock_print.assert_has_calls([call([test_data_to_conf[0]], today, 'today')])
    assert test_data_to_conf[0]["CONF"] == "yes"
    mock_upd.assert_has_calls([call('bookings',
                               test_data_to_conf[0],
                               'CONF', 'yes')])


@patch("builtins.input")
@patch("booking_sys.booking.print_bookings")
def test_confirm_input_2(*args):
    """
    Test confirm if the argument is not None, not empty and user input is "2".
    """
    (mock_print, mock_input) = args
    test_data_to_conf = [{'DATE': today, 'TIME': '20:00', 'NAME': 'Name1',
                          'PEOPLE': '1', 'CREATED': "Bob", 'CONF': '',
                          'CANC': ''}]
    mock_input.return_value = "2"

    assert confirm(test_data_to_conf) is None
    mock_print.assert_has_calls([call([test_data_to_conf[0]], today, 'today')])
    assert test_data_to_conf[0]["CONF"] != "yes"


@patch("booking_sys.booking.cancel")
@patch("builtins.input")
@patch("booking_sys.booking.print_bookings")
def test_confirm_input_3(*args):
    """
    Test confirm if the argument is not None, not empty and user input is "3".
    """
    (mock_print, mock_input, mock_cancel) = args
    test_data_to_conf = [{'DATE': today, 'TIME': '20:00', 'NAME': 'Name1',
                          'PEOPLE': '1', 'CREATED': "Bob", 'CONF': '',
                          'CANC': ''}]
    mock_input.return_value = "3"

    assert confirm(test_data_to_conf) is None
    mock_print.assert_has_calls([call([test_data_to_conf[0]], today, 'today')])
    mock_cancel.assert_called()
    assert test_data_to_conf[0]["CONF"] != "yes"


@patch("builtins.input")
@patch("booking_sys.booking.print_bookings")
def test_confirm_input_qx(*args):
    """
    Test confirm if the argument is not None, not empty
    and user input is "x" or "q".
    """
    (mock_print, mock_input) = args
    test_data_to_conf = [{'DATE': today, 'TIME': '20:00', 'NAME': 'Name1',
                          'PEOPLE': '1', 'CREATED': "Bob", 'CONF': '',
                          'CANC': ''}]

    user_input = mock_input.return_value = "x"
    assert confirm(test_data_to_conf) == user_input
    mock_print.assert_has_calls([call([test_data_to_conf[0]], today, 'today')])

    user_input = mock_input.return_value = "q"
    assert confirm(test_data_to_conf) == user_input
    mock_print.assert_has_calls([call([test_data_to_conf[0]], today, 'today')])


@patch("builtins.print")
@patch("builtins.input")
@patch("booking_sys.booking.print_bookings")
def test_confirm_invalid_input(*args):
    """
    Test confirm if the argument is not None, not empty and user input is "2".
    """
    (mock_print_bookings, mock_input, mock_print) = args
    test_data_to_conf = [{'DATE': today, 'TIME': '20:00', 'NAME': 'Name1',
                          'PEOPLE': '1', 'CREATED': "Bob", 'CONF': '',
                          'CANC': ''}]
    mock_input.return_value = "invalid"

    assert confirm(test_data_to_conf) is None
    mock_print_bookings.assert_has_calls([call([test_data_to_conf[0]],
                                               today, 'today')])
    mock_print.assert_called_with("\t\t\tInvalid input. Please, "
                                  "use options above.")


@patch("booking_sys.booking.has_duplicates")
@patch("booking_sys.booking.valid.date_input")
@patch("builtins.input")
def test_update_date(*args):
    """
    Test update_date with all possible scenarios.
    """
    (mock_input, mock_valid_date, mock_dups) = args
    old_date = test_data[0]["DATE"]

    user_input = mock_input.return_value = ""
    assert update_date.__wrapped__(user_input, test_data[0]) == old_date

    user_input = mock_input.return_value = "12-12-2023"
    mock_valid_date.return_value = user_input
    mock_dups.return_value = False
    assert update_date.__wrapped__(user_input, test_data[0]) == user_input
    mock_valid_date.assert_called()
    mock_dups.assert_called()

    user_input = mock_input.return_value = "12-12-2023"
    mock_valid_date.return_value = False
    mock_dups.return_value = False
    assert update_date.__wrapped__(user_input, test_data[0]) is False
    mock_valid_date.assert_called()
    mock_dups.assert_called()

    user_input = mock_input.return_value = "12-12-2023"
    mock_valid_date.return_value = user_input
    mock_dups.return_value = True
    assert update_date.__wrapped__(user_input, test_data[0]) is False
    mock_valid_date.assert_called()
    mock_dups.assert_called()

    user_input = mock_input.return_value = "12-12-2023"
    mock_valid_date.return_value = False
    mock_dups.return_value = True
    assert update_date.__wrapped__(user_input, test_data[0]) is False
    mock_valid_date.assert_called()
    mock_dups.assert_called()


@patch("booking_sys.booking.update_date")
def test_reschedule_date_xq(*args):
    """
    Test reschedule if update_date returns "x" or "q".
    """
    (mock_date,) = args

    user_input = mock_date.return_value = "x"
    assert reschedule(test_data[0]) == user_input

    user_input = mock_date.return_value = "q"
    assert reschedule(test_data[0]) == user_input


@patch("booking_sys.booking.new_time")
@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.active")
@patch("booking_sys.booking.get_data")
@patch("booking_sys.booking.update_date")
def test_reschedule_time_qx(*args):
    """
    Test reschedule if new_time returns "x" or "q".
    """
    (mock_date, mock_data, mock_active, mock_print, mock_time) = args
    user_date = mock_date.return_value = "12-12-2023"
    bookings = mock_active.return_value = test_data

    time = mock_time.return_value = "x"
    assert reschedule(test_data[0]) == time
    mock_date.assert_called()
    mock_data.assert_called()
    mock_active.assert_called()
    mock_print.assert_called_with(bookings, user_date, user_date)
    mock_time.assert_called()

    time = mock_time.return_value = "q"
    assert reschedule(test_data[0]) == time
    mock_date.assert_called()
    mock_data.assert_called()
    mock_active.assert_called()
    mock_print.assert_called_with(bookings, user_date, user_date)
    mock_time.assert_called()


@patch("booking_sys.booking.update_data")
@patch("booking_sys.booking.new_time")
@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.active")
@patch("booking_sys.booking.get_data")
@patch("booking_sys.booking.update_date")
def test_reschedule_completed(*args):
    """
    Test reschedule if completed.
    """
    (mock_date, mock_data, mock_active, mock_print, mock_time, mock_upd) = args
    user_date = mock_date.return_value = "12-12-2023"
    bookings = mock_active.return_value = test_data
    time = mock_time.return_value = "10:00"

    assert reschedule(test_data[0]) is None
    mock_date.assert_called()
    mock_data.assert_called()
    mock_active.assert_called()
    mock_print.assert_called_with(bookings, user_date, user_date)
    mock_time.assert_called()
    mock_upd.assert_has_calls([call("bookings", test_data[0],
                                    "DATE", user_date),
                               call("bookings", test_data[0], "TIME", time)])


@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_find_bookings_invalid_name(*args):
    """
    Test find_bookings if entered name is not in customers data.
    """
    (mock_input, mock_data) = args
    mock_data.return_value = customers
    user_input = mock_input.return_value = "Name3"

    assert find_bookings.__wrapped__(user_input) is False


@patch("builtins.print")
@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.cust_bookings")
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_find_bookings_no_bookings(*args):
    """
    Test find_bookings if there are no bookings for a valid name.
    """
    (mock_input, mock_data, mock_bookings, mock_print_b, mock_print) = args
    mock_data.return_value = customers
    user_input = mock_input.return_value = "Name2"
    bookings = mock_bookings.return_value = []

    assert find_bookings.__wrapped__(user_input) == 0
    mock_data.assert_called()
    mock_bookings.assert_called()
    mock_print_b.assert_called_with(bookings, [], "all time")
    mock_print.assert_called_with("\t\tThere are no active bookings "
                                  "for this customer.")


@patch("booking_sys.booking.pick_booking")
@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.cust_bookings")
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_find_bookings_pick_returns_x(*args):
    """
    Test find_bookings if pick_booking returns "x".
    """
    (mock_input, mock_data, mock_bookings, mock_print_b, mock_pick) = args
    mock_data.return_value = customers
    user_input = mock_input.return_value = "Name2"
    bookings = mock_bookings.return_value = customer_bookings
    mock_pick.return_value = "x"
    dates = [bookings[0]["DATE"], bookings[1]["DATE"]]

    assert find_bookings.__wrapped__(user_input) is True
    mock_data.assert_called()
    mock_bookings.assert_called()
    mock_print_b.assert_called_with(bookings, dates, "all time")
    mock_pick.assert_called()


@patch("booking_sys.booking.pick_booking")
@patch("booking_sys.booking.print_bookings")
@patch("booking_sys.booking.cust_bookings")
@patch("booking_sys.booking.get_data")
@patch("builtins.input")
def test_find_bookings_completed(*args):
    """
    Test find_bookings if completed.
    """
    (mock_input, mock_data, mock_bookings, mock_print_b, mock_pick) = args
    mock_data.return_value = customers
    user_input = mock_input.return_value = "Name2"
    bookings = mock_bookings.return_value = customer_bookings
    result = mock_pick.return_value = test_data[1]
    dates = [bookings[0]["DATE"], bookings[1]["DATE"]]

    assert find_bookings.__wrapped__(user_input) == result
    mock_data.assert_called()
    mock_bookings.assert_called()
    mock_print_b.assert_called_with(bookings, dates, "all time")
    mock_pick.assert_called()


@patch("builtins.print")
@patch("booking_sys.booking.valid.date_input")
@patch("builtins.input")
def test_pick_bookings_date_returns_false(*args):
    """
    Test pick_bookings id date_input returns False.
    """
    (mock_input, mock_date, mock_print) = args
    user_input = mock_input.return_value = "Name2"
    mock_date.return_value = False

    assert pick_booking.__wrapped__(user_input, customer_bookings) is None
    mock_date.assert_called()
    mock_print.assert_called_with(f"\t\tInvalid input: '{user_input}'. "
                                  "Please, enter a valid date.")


@patch("booking_sys.booking.search")
@patch("booking_sys.booking.valid.date_input")
@patch("builtins.input")
def test_pick_bookings_search_returns_none(*args):
    """
    Test pick_bookings if search returns None.
    """
    (mock_input, mock_date, mock_search) = args
    user_input = mock_input.return_value = "Name2"
    mock_date.return_value = tomorrow
    mock_search.return_value = None

    assert pick_booking.__wrapped__(user_input, customer_bookings) is False
    mock_date.assert_called()
    mock_search.assert_called()


@patch("booking_sys.booking.search")
@patch("booking_sys.booking.valid.date_input")
@patch("builtins.input")
def test_pick_bookings(*args):
    """
    Test pick_bookings if search is successful.
    """
    (mock_input, mock_date, mock_search) = args
    user_input = mock_input.return_value = "Name2"
    mock_date.return_value = tomorrow
    search = mock_search.return_value = {}

    assert pick_booking.__wrapped__(user_input, customer_bookings) == search
    mock_date.assert_called()
    mock_search.assert_called()


@patch("booking_sys.booking.get_customer")
@patch("booking_sys.booking.update_data")
def test_cancel(*args):
    """
    Test cancel().
    """
    (mock_upd, mock_get_customer) = args
    mock_get_customer.return_value = customers[0]
    exp_calls = [call('bookings', test_data[0], 'CANC', 'yes'),
                 call('customers', customers[0], 'CANCELLED', '9')]

    assert cancel(test_data[0]) is None
    mock_upd.assert_has_calls(exp_calls)


@patch("booking_sys.booking.print_bookings")
@patch("builtins.print")
@patch("booking_sys.booking.cust_bookings")
def test_has_duplicates(*args):
    """
    Test has_duplicates().
    """
    (mock_cust_bookings, mock_print, mock_print_bookings) = args
    mock_cust_bookings.return_value = customer_bookings
    msg = f"\n\t\t!!!Booking for {tomorrow} already exists!!!"

    assert has_duplicates(tomorrow, "Name1") is True
    mock_print.assert_called_with(msg)
    mock_print_bookings.assert_called_with(customer_bookings,
                                           tomorrow, tomorrow)

    assert has_duplicates("12-12-2023", "Name1") is False


@patch("booking_sys.booking.update_data")
def test_increment_bookings(*args):
    """
    Test increment_bookings().
    """
    (mock_upd, ) = args
    new_number = str(int(customers[0]["NUM OF BOOKINGS"]) + 1)

    increment_bookings(customers[0])
    mock_upd.assert_called_with("customers", customers[0],
                                "NUM OF BOOKINGS", new_number)
