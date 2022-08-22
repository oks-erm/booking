"""
Tests for spreadsheet module.
"""
from unittest.mock import patch, call
from gspread import Worksheet, exceptions, Cell
from booking_sys.spreadsheet import (SHEET, get_worksheet, get_data,
                                     update_worksheet, update_data)


GET_VALUES_PATH = ('booking_sys.spreadsheet.gspread'
                   '.worksheet.Worksheet.get_values')
APPEND_ROW_PATH = ('booking_sys.spreadsheet.gspread'
                   '.worksheet.Worksheet.append_row')
WORKSHEET_PATH = 'booking_sys.spreadsheet.SHEET.worksheet'
FIND_PATH = 'booking_sys.spreadsheet.gspread.worksheet.Worksheet.find'
UPD_CELL_PATH = ('booking_sys.spreadsheet.gspread'
                 '.worksheet.Worksheet.update_cell')
get_values_config = {"return_value": [[]], "autospec": True}
config_exception = {"side_effect": [exceptions.GSpreadException,
                                    exceptions.GSpreadException,
                                    [[]]],
                    "autospec": True}
worksheet_config = {"return_value": Worksheet(SHEET,
                    properties={"sheetId": "12345", "title": "name"})}


@patch(GET_VALUES_PATH, **get_values_config)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_get_worksheet(*args):
    """
    Test get_worksheet: if it returns correct data.
    """
    assert get_worksheet("name") == [[]]


@patch(GET_VALUES_PATH, **config_exception)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_get_worksheet_exception(*args):
    """
    Test get_worksheet handling exceptions.
    """
    exc_msg = "press 1 - Try again\npress x - Exit\n"
    with patch("builtins.input", return_value="x", autospec=True) as mock_inp:
        with patch('booking_sys.spreadsheet.sys.exit') as exit_mock:
            get_worksheet("name")
            mock_inp.assert_called_with(exc_msg)
            exit_mock.assert_called()

    with patch("builtins.input", return_value="1", autospec=True) as mock_inp:
        with patch('builtins.print') as print_mock:
            get_worksheet("name")
            mock_inp.assert_called_with(exc_msg)
            print_mock.assert_has_calls([call('Trying...')], any_order=False)


@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_worksheet(*args):
    """
    Test update_worksheet successful scenario.
    """
    with patch(APPEND_ROW_PATH, autospec=True) as mock_append:
        with patch('builtins.print') as print_mock:
            update_worksheet([[]], "name")
            mock_append.assert_called()
            print_mock.assert_called_with("\n\t\tSaved successfully!\n")


@patch(APPEND_ROW_PATH, **config_exception)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_worksheet_exception(*args):
    """
    Test update_worksheet handling exceptions.
    """
    exc_msg = "press 1 - Try again\npress x - Continue without saving\n"
    with patch("builtins.input", return_value="x", autospec=True) as mock_inp:
        with patch('builtins.print') as print_mock:
            update_worksheet([[]], "name")
            mock_inp.assert_called_with(exc_msg)
            print_mock.assert_called_with("Your data was not saved.")

    with patch("builtins.input", return_value="1", autospec=True) as mock_inp:
        with patch('builtins.print') as print_mock:
            update_worksheet([[]], "name")
            mock_inp.assert_called_with(exc_msg)
            print_mock.assert_has_calls([call('Trying...')], any_order=False)


@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_get_data(*args):
    """
    Tests if spreadsheet response is converted to dictionary.
    """
    with patch("booking_sys.spreadsheet.get_worksheet",
               return_value=[['NAME', 'PASSWORD', 'CONTACT'],
                             ['Bob', '123', '003543243422'],
                             ['Kelly', '456', '+44 6734657788']]):
        assert get_data("sheet") == [{'CONTACT': '003543243422',
                                      'NAME': 'Bob', 'PASSWORD': '123'},
                                     {'CONTACT': '+44 6734657788',
                                      'NAME': 'Kelly', 'PASSWORD': '456'}]


@patch(FIND_PATH, return_value=Cell(row=2, col=1, value="Bob"), autospec=True)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_data(*args):
    """
    Test update_data successful scenario.
    """
    worksheet = "name"
    test_obj = {'CONTACT': '003543243422', 'NAME': 'Bob', 'PASSWORD': '123'}
    attr = "PASSWORD"
    new_value = "321"
    msg = f"\t\t{worksheet.capitalize()} info was successfully updated!"
    with patch(UPD_CELL_PATH, autospec=True) as mock_upd:
        with patch('builtins.print') as print_mock:
            update_data(worksheet, test_obj, attr, new_value)
            assert test_obj[attr] == new_value
            assert update_data("name", test_obj, attr, new_value) == test_obj
            print_mock.assert_called_with(msg)
            mock_upd.assert_called()


config_exception = {"side_effect": [exceptions.GSpreadException,
                                    exceptions.GSpreadException,
                                    Cell(2, 1, value="Bob"),
                                    Cell(2, 1, value="Bob")],
                    "autospec": True}


@patch(FIND_PATH, **config_exception)
@patch(UPD_CELL_PATH, autospec=True)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_data_exception(*args):
    """
    Test update_data handling exceptions.
    """
    worksheet = "name"
    test_obj = {'CONTACT': '003543243422', 'NAME': 'Bob', 'PASSWORD': '123'}
    attr = "PASSWORD"
    new_value = "321"
    exc_print = "\nDatabase is not available, I couldn't save your data"
    exc_msg = "press 1 - Try again\npress x - Continue without saving\n"
    with patch("builtins.input", return_value="x", autospec=True) as mock_inp:
        with patch('builtins.print') as print_mock:
            update_data(worksheet, test_obj, attr, new_value)
            mock_inp.assert_called_with(exc_msg)
            print_mock.assert_called_with("Your data was not saved.")

    with patch("builtins.input", return_value="1", autospec=True) as mock_inp:
        with patch('builtins.print') as print_mock:

            update_data(worksheet, test_obj, attr, new_value)
            mock_inp.assert_called_with(exc_msg)
            print_mock.assert_has_calls([call(exc_print), call('Trying...')],
                                        any_order=False)
