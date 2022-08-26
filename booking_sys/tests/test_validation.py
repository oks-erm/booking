"""
Tests for validation module.
"""
from datetime import date
import pytest
from booking_sys.validation import (to_date, convert_date, date_input,
                                    birthdate, time_input, email, phone_num)


@pytest.mark.parametrize("a, expected",
                         [("10-10-2022", date(2022, 10, 10)),
                          ("1-10-2022", date(2022, 10, 1)),
                          ("01-10-2022", date(2022, 10, 1)),
                          ("10/10/2022", False),
                          ("10.10.2022", False),
                          ("30-02-2022", False),
                          ("10-20-2022", False),
                          ("10-10-22", False)])
def test_to_date_date_formats(a, expected):
    """
    Test date formats.
    """
    assert to_date(a) == expected


@pytest.mark.parametrize("a, expected",
                         [("string", False),
                          (0, False),
                          (["10-10-2022"], False),
                          (("10-10-2022",), False),
                          ({"date": "10-10-2022"}, False),
                          (None, False),
                          (True, False),
                          (False, False)])
def test_to_date_data_formats(a, expected):
    """
    Test data formats.
    """
    assert to_date(a) == expected


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


@pytest.mark.parametrize("a, expected",
                         [(42, False),
                          (0, False),
                          (["10/10/2022"], False),
                          (("10/10/2022",), False),
                          ({"date": "10/10/2022"}, False),
                          (None, False),
                          (True, False),
                          (False, False)])
def test_convert_date_data_formats(a, expected):
    """
    Test different data formats.
    """
    assert convert_date(a) == expected


@pytest.mark.parametrize("a, expected",
                         [("10/10/2023", "10-10-2023"),
                          ("10.10.2023", "10-10-2023"),
                          ("10-10-2023", "10-10-2023"),
                          ("10,10,2023", "10-10-2023"),
                          ("10.10.2021", False),
                          ("1.10.2022", False)])
def test_date_input(a, expected):
    """
    Test different date formats.
    """
    assert date_input(a) == expected


@pytest.mark.parametrize("a, expected",
                         [(42, False),
                          (0, False),
                          (["10/10/2022"], False),
                          (("10/10/2022",), False),
                          ({"date": "10/10/2022"}, False),
                          (None, False),
                          (True, False),
                          (False, False)])
def test_date_input_data_formats(a, expected):
    """
    Test different data formats.
    """
    assert date_input(a) == expected


@pytest.mark.parametrize("a, expected",
                         [("10/10/2000", "10-10-2000"),
                          ("10.10.2000", "10-10-2000"),
                          ("10-10-2000", "10-10-2000"),
                          ("10,10,2000", "10-10-2000"),
                          ("10.10.2023", False),
                          ("1.10.2022", False)])
def test_birthdate(a, expected):
    """
    Test different date formats.
    """
    assert birthdate(a) == expected


@pytest.mark.parametrize("a, expected",
                         [(42, False),
                          (0, False),
                          (["10/10/2022"], False),
                          (("10/10/2022",), False),
                          ({"date": "10/10/2022"}, False),
                          (None, False),
                          (True, False),
                          (False, False)])
def test_birthdate_data_formats(a, expected):
    """
    Test different data formats.
    """
    assert birthdate(a) == expected


@pytest.mark.parametrize("a, expected",
                         [("18:00", True),
                          ("25:00", False),
                          ("1:00", False),
                          ("111:00", False)])
def test_time_inpit(a, expected):
    """
    Test different time formats.
    """
    assert time_input(a) == expected


@pytest.mark.parametrize("a, expected",
                         [(42, False),
                          (0, False),
                          (["18:00"], False),
                          (("18:00",), False),
                          ({"time": "18:00"}, False),
                          (None, False),
                          (True, False),
                          (False, False)])
def test_time_input_data_formats(a, expected):
    """
    Test different data formats.
    """
    assert time_input(a) == expected


@pytest.mark.parametrize("a, expected",
                         [("email@a.bc", True),
                          ("string", False),
                          ("@string", False),
                          ("string@", False),
                          ("str@ing", False),
                          ("str@ing.", False),
                          ("stri.ng", False),
                          (".str@i.ng", False),
                          ("@str@i.ng", False),
                          ("@str@in.g", False)])
def test_email(a, expected):
    """
    Test different email formats.
    """
    assert email(a) == expected


@pytest.mark.parametrize("a, expected",
                         [(42, False),
                          (0, False),
                          (["email@a.bc"], False),
                          (("email@a.bc",), False),
                          ({"email": "email@a.bc"}, False),
                          (None, False),
                          (True, False),
                          (False, False)])
def test_email_data_formats(a, expected):
    """
    Test different data formats.
    """
    assert email(a) == expected


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
pairs_valid = []
for item in valid:
    pairs_valid.append((item, True))

invalid = ["1234567", "022 345678", "+023 456789", "423 45 67 890",
           "+002345 678901", "+6123456+78901", "+(712)34567 89012",
           "+81234567888901238786", "-912345678901", "-1 23 45 67.1",
           "22.345.678", "323-4567-89", "+42 345", "+612,3 45 6,789 01",
           "00 234567", "stringstring", "00(235)67-90.1", ""]
pairs_invalid = []
for item in invalid:
    pairs_invalid.append((item, False))


@pytest.mark.parametrize("a, expected",
                         pairs_valid)
def test_phone_num_valid(a, expected):
    """
    Test valid phone formats.
    """
    assert phone_num(a) == expected


@pytest.mark.parametrize("a, expected",
                         pairs_invalid)
def test_phone_num_invalid(a, expected):
    """
    Test invalid phone formats.
    """
    assert phone_num(a) == expected


@pytest.mark.parametrize("a, expected",
                         [(42, False),
                          ([], False),
                          ((), False),
                          ({}, False),
                          (None, False),
                          (True, False),
                          (False, False)])
def test_phone_num_data_formats(a, expected):
    """
    Test different data formats.
    """
    assert phone_num(a) == expected
