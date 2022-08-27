"""
Tests for stats module.
"""
import os
from unittest.mock import patch
import pytest
from booking_sys.stats import data_for_stats, calculate_age
from run import cleanup


@pytest.mark.parametrize("a, expected",
                         [("10-12-1967", '54'),
                          ("10-08-2022", '0'),
                          ("10-12-2023", ("This date is from the future. "
                                          "Can\'t calculate age.")),
                          ("10/12/2023", ("Make sure you use "
                                          "dd-mm-yyyy format")),
                          (102022, "Argument should be str"),
                          ([], "Argument should be str"),
                          ({}, "Argument should be str"),
                          (True, "Argument should be str"),
                          (None, "Argument should be str"),
                          ("10-18-2023", ("Make sure you use "
                                          "dd-mm-yyyy format"))])
def test_calculate_age(a, expected):
    """
    Tests calculate_age() on different values and data types.
    """
    assert calculate_age(a) == expected


@patch("booking_sys.stats.get_worksheet")
def test_data_for_stats(*args):
    """
    Tests if a file with required data is created.
    """
    (mock_worksheet, ) = args
    test_data = [['NAME', 'PHONE', 'EMAIL', 'BIRTHDATE'],
                 ['Bob', '003543243422', "q@w.er", "10-10-1976"],
                 ['Kelly', '+44 6734657788', "t@y.ui", "10-11-1987"]]
    mock_worksheet.return_value = test_data
    data_for_stats()
    if os.path.exists("stats.csv"):
        with open("stats.csv", 'r') as file:
            content = file.readlines()
            assert 'NAME,PHONE,EMAIL,BIRTHDATE\n' in content
    assert os.path.exists("stats.csv") is True
    cleanup()
