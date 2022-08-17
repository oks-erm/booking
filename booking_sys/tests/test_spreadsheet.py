"""
Tests for spreadsheet module.
"""
from unittest import mock
from booking_sys.spreadsheet import get_data


@mock.patch("booking_sys.spreadsheet.get_worksheet",
            return_value=[['NAME', 'PASSWORD', 'CONTACT'],
                          ['Bob', '123', '003543243422'],
                          ['Kelly', '456', '+44 6734657788']])
def test_get_data(*args):
    """
    Tests if spreadsheet response is converted to dictionary.
    """
    assert get_data("sheet") == [{'CONTACT': '003543243422',
                                  'NAME': 'Bob', 'PASSWORD': '123'},
                                 {'CONTACT': '+44 6734657788',
                                  'NAME': 'Kelly', 'PASSWORD': '456'}]
