"""

"""
import pytest
import os
from unittest import mock
import booking_sys.stats as stats 


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
    assert stats.calculate_age(a) == expected


# @mock.patch("booking_sys.stats.get_worksheet",
#             return_value=[['NAME', 'PHONE', 'EMAIL', 'BIRTHDATE'],
#                           ['Bob', '003543243422', "q@w.er", "10-10-1976"],
#                           ['Kelly', '+44 6734657788', "t@y.ui", "10-11-1987"]])
# def test_data_for_stats(*args): 
#     assert os.path.exists("stats.csv") is True
