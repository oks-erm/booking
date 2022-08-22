"""
Tests for validation module.
"""
from datetime import date
import pytest
from booking_sys.validation import (to_date, convert_date, date_input,
                                    birthdate, time_input, email, phone_num)


def test_to_date_date_formats():
    """
    Test date formats.
    """
    assert to_date("10-10-2022") == date(2022, 10, 10)
    assert to_date("1-10-2022") == date(2022, 10, 1)
    assert to_date("01-10-2022") == date(2022, 10, 1)
    formats = ["10/10/2022", "10.10.2022", "30-02-2022",
               "10-20-2022", "10-10-22"]
    for item in formats:
        assert to_date(item) is False


def test_to_date_data_formats():
    """
    Test data formats.
    """
    fail = ["string", 0, ["10-10-2022"], ("10-10-2022",),
            {"date": "10-10-2022"}, None, True, False]
    for item in fail:
        assert to_date(item) is False


@pytest.mark.parametrize("a, expected",
                         [("10/10/2022", "10-10-2022"),
                          ("10.10.2022", "10-10-2022"),
                          ("10,10,2022", "10-10-2022"),
                          ("10\10\2022", "10\10\2022"),
                          ("string", "string")])
def test_convert_date(a, expected):
    """
    Test different date formats and input
    with nothing to substitute.
    """
    assert convert_date(a) == expected


def test_convert_date_data_formats():
    """
    Test different data formats.
    """
    fail = [42, 0, ["10/10/2022"], ("10/10/2022",),
            {"date": "10/10/2022"}, None, True, False]
    for item in fail:
        assert convert_date(item) is False


def test_date_input():
    """
    Test different date formats.
    """
    assert date_input("10/10/2023") == "10-10-2023"
    assert date_input("10.10.2023") == "10-10-2023"
    assert date_input("10-10-2023") == "10-10-2023"
    assert date_input("10,10,2023") == "10-10-2023"
    assert date_input("10.10.2021") is False
    assert date_input("1.10.2022") is False


def test_date_input_data_formats():
    """
    Test different data formats.
    """
    fail = [42, 0, ["10/10/2022"], ("10/10/2023",),
            {"date": "10/10/2022"}, None, True, False]
    for item in fail:
        assert date_input(item) is False


def test_birthdate():
    """
    Test different date formats.
    """
    assert birthdate("10/10/2000") == "10-10-2000"
    assert birthdate("10.10.2000") == "10-10-2000"
    assert birthdate("10-10-2000") == "10-10-2000"
    assert birthdate("10,10,2000") == "10-10-2000"
    assert birthdate("10.10.2023") is False
    assert birthdate("1.10.2021") is False


def test_birthdate_data_formats():
    """
    Test different data formats.
    """
    fail = [42, 0, ["10/10/2000"], ("10/10/2000",),
            {"date": "10/10/2000"}, None, True, False]
    for item in fail:
        assert birthdate(item) is False


def test_time_inpit():
    """
    Test different time formats.
    """
    assert time_input("18:00") is True
    assert time_input("25:00") is False
    assert time_input("1:00") is False
    assert time_input("111:00") is False


def test_time_input_data_formats():
    """
    Test different data formats.
    """
    fail = [42, 0, ["18:00"], ("18:00",), {"time": "18:00"},
            None, True, False]
    for item in fail:
        assert time_input(item) is False


def test_email():
    """
    Test different email formats.
    """
    assert email("email@a.bc") is True
    emails = ["string", "@string", "string@",
              "str@ing", "str@ing.", "stri.ng",
              ".str@i.ng", "@str@i.ng", "@str@in.g"]
    for item in emails:
        assert email(item) is False


def test_email_data_formats():
    """
    Test different data formats.
    """
    fail = [42, 0, ["email@a.bc"], ("email@a.bc",),
            {"email": "email@a.bc"}, None, True, False]
    for item in fail:
        assert email(item) is False


def test_phone_num():
    """
    Test different phone formats.
    """
    valid = ["+1 234567", "+22 345678", "+323 456789",
             "+42345 67890", "+52345 678901", "+6123456 78901",
             "+71234567 89012", "+812345678 90123", "+91234567890.1",
             "+1 23 45 67", "+22 345 678", "+323 4567 89",
             "+42 345 678 90", "+523 45 67 89 01", "+612 3 45 6 789 01",
             "+71-234-567-8", "+812-345-678.123", "+9(235)67-90.1",
             "003 456 78", "0023 456789", "002 34 56 78 9",
             "002345 67890", "002345 678901", "00123456 78901",
             "001234567 89012", "0012345678 90123", "001234567890.1",
             "0023 45 67", "002 345 678", "0023 4567 89",
             "002 345 678 90", "0023 45 67 89 01", "0012 3 45 6 789 01",
             "001-234-567-8", "0012-345-678.123", "+523.4567.89 01"]
    for phone in valid:
        assert phone_num(phone) is True

    invalid = ["1234567", "022 345678", "+023 456789",
               "423 45 67 890", "+002345 678901", "+6123456+78901",
               "+(712)34567 89012", "+81234567888901238786", "-912345678901",
               "-1 23 45 67.1", "22.345.678", "323-4567-89",
               "+42 345", "+612,3 45 6,789 01",
               "00 234567", "stringstring", "00(235)67-90.1", ""]
    for phone in invalid:
        assert phone_num(phone) is False


def test_phone_num_data_formats():
    """
    Test different data formats.
    """
    data = [None, True, False, 42, [], {}, ()]
    for item in data:
        assert phone_num(item) is False
