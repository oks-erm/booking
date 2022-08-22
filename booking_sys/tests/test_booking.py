from unittest.mock import patch, call
from datetime import date, timedelta
import re
from booking_sys.booking import (dd_mm_yyyy, active, confirmed, cust_bookings,
                                 bookings_menu, view_bookings_menu,
                                 print_bookings, new_date)


def test_dd_mm_yyyy():
    assert dd_mm_yyyy("2022-08-20") == "20-08-2022"
    assert dd_mm_yyyy("2022/08/20") == "2022/08/20"
    assert dd_mm_yyyy(["2022/08/20"]) is None
    assert dd_mm_yyyy({"a": "b"}) is None
    assert dd_mm_yyyy(42) is None
    assert dd_mm_yyyy(None) is None
    assert dd_mm_yyyy(True) is None


def test_active():
    test_data = [{'DATE': '10-10-2022', 'TIME': '20:00',
                  'NAME': 'Name', 'PEOPLE': '1', 'CREATED': "Bob",
                  'CONF': '', 'CANC': ''},
                 {'DATE': '10-05-2022', 'TIME': '20:00',
                  'NAME': 'Name', 'PEOPLE': '2', 'CREATED': "Bob",
                  'CONF': '', 'CANC': ''},
                 {'DATE': '12-09-2022', 'TIME': '20:00',
                  'NAME': 'Name', 'PEOPLE': '2', 'CREATED': "Bob",
                  'CONF': '', 'CANC': 'yes'}]
    assert active(test_data) == [test_data[0]]
    assert active({"a": "b"}) is None
    assert active(42) is None
    assert active("string") is None
    assert active(None) is None
    assert active(True) is None


def test_confirmed():
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


def test_cust_bookings():
    test_data = [{'DATE': '10-10-2022', 'TIME': '20:00',
                  'NAME': 'Name1', 'PEOPLE': '1', 'CREATED': "Bob",
                  'CONF': '', 'CANC': ''},
                 {'DATE': '10-05-2022', 'TIME': '20:00',
                  'NAME': 'Name2', 'PEOPLE': '2', 'CREATED': "Bob",
                  'CONF': '', 'CANC': ''},
                 {'DATE': '12-09-2022', 'TIME': '20:00',
                  'NAME': 'Name1', 'PEOPLE': '2', 'CREATED': "Bob",
                  'CONF': '', 'CANC': 'yes'}]
    with patch("booking_sys.booking.get_data") as mock_data:
        with patch("booking_sys.booking.active") as mock_active:
            mock_active.return_value = test_data
            name = "Name1"

            assert cust_bookings(name) == [test_data[0], test_data[2]]
            mock_active.assert_called()
            mock_data.assert_called()
            assert cust_bookings({"a": 1}) == []
            assert cust_bookings(42) == []
            assert cust_bookings("string") == []
            assert cust_bookings(None) == []
            assert cust_bookings(True) == []


def test_bookings_menu_invalid_input():
    with patch("builtins.input", return_value="0") as mock_input:
        user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
        user_input = mock_input.return_value
        assert bookings_menu.__wrapped__(user_input, user) is False


def test_bookings_menu_input_1():
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    with patch("builtins.input", return_value="1") as mock_input:
        with patch("booking_sys.booking.view_bookings_menu") as mock_view:
            user_input = mock_input.return_value
            result = mock_view.return_value = True
            assert bookings_menu.__wrapped__(user_input, user) == result


def test_bookings_menu_input_2():
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    with patch("builtins.input", return_value="2") as mock_input:
        with patch("booking_sys.booking.find_customer") as mock_find:
            with patch("booking_sys.booking.new_booking") as mock_new:
                user_input = mock_input.return_value
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


def test_bookings_menu_input_3():
    user = {'NAME': 'Name1', 'PASSWORD': '111', 'CONTACT': ''}
    with patch("builtins.input", return_value="3") as mock_input:
        with patch("booking_sys.booking.edit_bookings") as mock_edit:
            user_input = mock_input.return_value
            result = mock_edit.return_value = None
            assert bookings_menu.__wrapped__(user_input, user) == result


def test_view_bookings_menu_invalid_input():
    with patch("builtins.input") as mock_input:
        with patch("booking_sys.booking.get_data") as mock_get_data:
            with patch("booking_sys.booking.dd_mm_yyyy") as mock_dd_mm_yyyy:
                with patch("booking_sys.booking.active") as mock_active:
                    user_input = mock_input.return_value = "0"
                    mock_active.return_value = []
                    mock_dd_mm_yyyy.return_value = ""

                    assert view_bookings_menu.__wrapped__(user_input) is False
                    mock_get_data.assert_called()
                    mock_active.assert_called()
                    mock_dd_mm_yyyy.assert_called()


@patch("booking_sys.booking.get_data")
def test_view_bookings_menu_valid_input(get_data):
    today = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                   '\\3-\\2-\\1', str(date.today()))
    tomorrow = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                      '\\3-\\2-\\1', str((date.today() + timedelta(days=1))))
    future = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                    '\\3-\\2-\\1', (str(date.today() + timedelta(days=10))))
    test_data = [{'DATE': tomorrow, 'TIME': '20:00',
                  'NAME': 'Name1', 'PEOPLE': '1', 'CREATED': "Bob",
                  'CONF': '', 'CANC': ''},
                 {'DATE': today, 'TIME': '20:00',
                  'NAME': 'Name2', 'PEOPLE': '2', 'CREATED': "Bob",
                  'CONF': '', 'CANC': ''},
                 {'DATE': future, 'TIME': '20:00',
                  'NAME': 'Name3', 'PEOPLE': '3', 'CREATED': "Bob",
                  'CONF': '', 'CANC': 'yes'}]
    config = {"side_effect": (lambda x: re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
              '\\3-\\2-\\1', x))}

    with patch("booking_sys.booking.dd_mm_yyyy", **config) as mock_ddmmyyyy:
        with patch("builtins.input") as mock_input:
            with patch("booking_sys.booking.print_bookings") as mock_print:
                with patch("booking_sys.booking.active") as mock_active:
                    mock_active.return_value = test_data

                    user_input = mock_input.return_value = "1"
                    assert view_bookings_menu.__wrapped__(user_input) is True
                    mock_active.assert_called()
                    mock_ddmmyyyy.assert_called()
                    mock_print.assert_called_with(test_data, today, "today")

                    user_input = mock_input.return_value = "2"
                    assert view_bookings_menu.__wrapped__(user_input) is True
                    mock_print.assert_called_with(test_data, tomorrow,
                                                  "tomorrow")

                    user_input = mock_input.return_value = "3"
                    week = [today]
                    for i in range(1, 7):
                        week.append(dd_mm_yyyy(str(date.today()
                                    + timedelta(days=i))))
                    assert view_bookings_menu.__wrapped__(user_input) is True
                    mock_print.assert_called_with(test_data, week,
                                                  'the upcoming week')

                    user_input = mock_input.return_value = "4"
                    assert view_bookings_menu.__wrapped__(user_input) is True
                    mock_print.assert_called_with(test_data,
                                                  [tomorrow, today, future],
                                                  "all time")


def test_print_bookings():
    today = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                   '\\3-\\2-\\1', str(date.today()))
    tomorrow = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                      '\\3-\\2-\\1', str((date.today() + timedelta(days=1))))
    future = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})',
                    '\\3-\\2-\\1', (str(date.today() + timedelta(days=10))))
    test_data = [{'DATE': tomorrow, 'TIME': '20:00',
                  'NAME': 'Name1', 'PEOPLE': '1', 'CREATED': "Bob",
                  'CONF': '', 'CANC': ''},
                 {'DATE': today, 'TIME': '20:00',
                  'NAME': 'Name2', 'PEOPLE': '2', 'CREATED': "Bob",
                  'CONF': 'yes', 'CANC': ''},
                 {'DATE': future, 'TIME': '20:00',
                  'NAME': 'Name3', 'PEOPLE': '3', 'CREATED': "Bob",
                  'CONF': '', 'CANC': 'yes'}]

    with patch("builtins.print") as mock_print:
        print_bookings.__wrapped__(test_data, today, "today")
        exp_calls = [call('\tYou have 1 booking(s) for today:\n'),
                     call('\t22-08 - 20:00 - Name2 (2 ppl) added by Bob \\/')]
        mock_print.assert_has_calls(exp_calls)


@patch("booking_sys.booking.get_data")
def test_new_date_valid_input(get_data):
    cust = {'NAME': 'Test Name'}

    with patch("builtins.input") as mock_input:
        with patch("booking_sys.booking.valid.date_input") as mock_date:
            with patch("booking_sys.booking.has_duplicates") as mock_dup:
                with patch("booking_sys.booking.print_bookings") as mock_print:
                    with patch("booking_sys.booking.active") as mock_active:
                        user_input = mock_input.return_value = "10-10-2022"
                        valid = mock_date.return_value = "10-10-2022"
                        mock_dup.return_value = False
                        bookings = mock_active.return_value = []
                        assert new_date.__wrapped__(user_input, cust) == valid
                        mock_date.assert_called()
                        mock_dup.assert_called()
                        mock_active.assert_called()
                        mock_print.assert_called_with(bookings, valid, valid)

                        mock_dup.return_value = True
                        assert new_date.__wrapped__(user_input, cust) is None


@patch("booking_sys.booking.active")
@patch("booking_sys.booking.get_data")
def test_new_date_invalid_input(get_data, active):
    cust = {'NAME': 'Test Name'}

    with patch("builtins.input") as mock_input:
        with patch("booking_sys.booking.valid.date_input") as mock_date:
            with patch("booking_sys.booking.has_duplicates") as mock_dup:
                user_input = mock_input.return_value = "10-10-22"
                mock_date.return_value = False
                mock_dup.return_value = False

                assert new_date.__wrapped__(user_input, cust) is False
                mock_date.assert_called()
                mock_dup.assert_called()





# def new_date(*args):
#     user_input, customer = (args)
#     valid_date = valid.date_input(user_input)
#     duplicates = has_duplicates(valid_date, customer["NAME"])
#     if valid_date and duplicates is False:
#         bookings = active(get_data("bookings"))
#         print_bookings(bookings, valid_date, valid_date)
#         return valid_date
#     if duplicates:
#         return None
#     return False