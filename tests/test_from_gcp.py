# test_google_sheets_utils.py

import pytest
from unittest.mock import Mock
from pandasheets import create_sheet, delete_sheet


@pytest.mark.parametrize(
    "test_input, expected_method, expected_args",
    [
        (
            ("your_spreadsheet_id", "Sheet1"),
            "create",
            {
                "body": {"properties": {"title": "Sheet1"}},
                "spreadsheetId": "your_spreadsheet_id",
            },
        ),
        (
            ("your_spreadsheet_id", "your_sheet_id"),
            "batchUpdate",
            {
                "spreadsheetId": "your_spreadsheet_id",
                "body": {"requests": [{"deleteSheet": {"sheetId": "your_sheet_id"}}]},
            },
        ),
    ],
)
def test_google_sheets_utils(mock_build, test_input, expected_method, expected_args):
    # Mock the 'build' function from googleapiclient.discovery
    mock_service = Mock()
    mock_build.return_value = mock_service

    # Unpack the test input
    args = test_input

    # Call the function under test
    if expected_method == "create":
        create_sheet(*args)
    elif expected_method == "batchUpdate":
        delete_sheet(*args)

    # Assert that the necessary methods were called on the mock service
    em = getattr(mock_service.spreadsheets(), expected_method)
    em.assert_called_once_with(**expected_args)
