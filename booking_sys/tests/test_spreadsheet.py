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
get_values_config = {"return_value": [[]]}
config_exception = {"side_effect": [exceptions.GSpreadException,
                                    exceptions.GSpreadException,
                                    [[]]]}
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
    (*_, mock_worksheet, mock_values) = args
    assert get_worksheet("name") == [[]]
    mock_worksheet.assert_called()
    mock_values.assert_called()


@patch("builtins.print")
@patch('booking_sys.spreadsheet.sys.exit')
@patch("builtins.input")
@patch(GET_VALUES_PATH, **config_exception)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_get_worksheet_exception(*args):
    """
    Test get_worksheet handling exceptions.
    """
    (*_, mock_input, exit_mock, mock_print) = args
    exc_msg = "press 1 - Try again\npress x - Exit\n"

    mock_input.return_value = "x"
    get_worksheet("name")
    mock_input.assert_called_with(exc_msg)
    exit_mock.assert_called()

    mock_input.return_value = "1"
    get_worksheet("name")
    mock_input.assert_called_with(exc_msg)
    mock_print.assert_has_calls([call('Trying...')], any_order=False)


@patch('builtins.print')
@patch(APPEND_ROW_PATH)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_worksheet(*args):
    """
    Test update_worksheet successful scenario.
    """
    (*_, mock_worksheet, mock_append, print_mock) = args

    update_worksheet([[]], "name")
    mock_worksheet.assert_called()
    mock_append.assert_called()
    print_mock.assert_called_with("\n\t\tSaved successfully!")


@patch("builtins.print")
@patch("builtins.input")
@patch(APPEND_ROW_PATH, **config_exception)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_worksheet_exception(*args):
    """
    Test update_worksheet handling exceptions.
    """
    (*_, mock_input, mock_print) = args
    exc_msg = "press 1 - Try again\npress x - Continue without saving\n"

    mock_input.return_value = "x"
    update_worksheet([[]], "name")
    mock_input.assert_called_with(exc_msg)
    mock_print.assert_called_with("Your data was not saved.")

    mock_input.return_value = "1"
    update_worksheet([[]], "name")
    mock_input.assert_called_with(exc_msg)
    mock_print.assert_has_calls([call('Trying...')], any_order=False)


@patch("booking_sys.spreadsheet.get_worksheet")
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_get_data(*args):
    """
    Tests if spreadsheet response is converted to dictionary.
    """
    (*_, mock_get_ws) = args
    mock_get_ws.return_value = [['NAME', 'PASSWORD', 'CONTACT'],
                                ['Bob', '123', '003543243422'],
                                ['Kelly', '456', '+44 6734657788']]

    assert get_data("sheet") == [{'CONTACT': '003543243422',
                                  'NAME': 'Bob', 'PASSWORD': '123'},
                                 {'CONTACT': '+44 6734657788',
                                  'NAME': 'Kelly', 'PASSWORD': '456'}]


@patch('builtins.print')
@patch(UPD_CELL_PATH)
@patch(FIND_PATH, return_value=Cell(row=2, col=1, value="Bob"))
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_data(*args):
    """
    Test update_data successful scenario.
    """
    (*_, mock_worksheet, mock_find, mock_upd, mock_print) = args
    worksheet = "name"
    test_obj = {'CONTACT': '003543243422', 'NAME': 'Bob', 'PASSWORD': '123'}
    attr = "PASSWORD"
    new_value = "321"
    msg = (f"\t\t{worksheet.capitalize()}({attr}) "
           "info was successfully updated!")

    update_data(worksheet, test_obj, attr, new_value)
    assert test_obj[attr] == new_value
    assert update_data("name", test_obj, attr, new_value) == test_obj
    mock_find.assert_called()
    mock_worksheet.assert_called()
    mock_print.assert_called_with(msg)
    mock_upd.assert_called()


config_exception = {"side_effect": [exceptions.GSpreadException,
                                    exceptions.GSpreadException,
                                    Cell(2, 1, value="Bob"),
                                    Cell(2, 1, value="Bob")]}


@patch("builtins.print")
@patch("builtins.input")
@patch(FIND_PATH, **config_exception)
@patch(UPD_CELL_PATH)
@patch(WORKSHEET_PATH, **worksheet_config)
@patch("gspread.client", autospec=True)
@patch("gspread.authorize", autospec=True)
def test_update_data_exception(*args):
    """
    Test update_data handling exceptions.
    """
    (*_, mock_input, mock_print) = args
    worksheet = "name"
    test_obj = {'CONTACT': '003543243422', 'NAME': 'Bob', 'PASSWORD': '123'}
    attr = "PASSWORD"
    new_value = "321"
    exc_print = "\nDatabase is not available, I couldn't save your data"
    exc_msg = "press 1 - Try again\npress x - Continue without saving\n"

    mock_input.return_value = "x"
    update_data(worksheet, test_obj, attr, new_value)
    mock_input.assert_called_with(exc_msg)
    mock_print.assert_called_with("Your data was not saved.")

    mock_input.return_value = "1"
    update_data(worksheet, test_obj, attr, new_value)
    mock_input.assert_called_with(exc_msg)
    mock_print.assert_has_calls([call(exc_print), call('Trying...')],
                                any_order=False)
