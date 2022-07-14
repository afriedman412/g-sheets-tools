import pytest
from unittest.mock import patch


@pytest.fixture
def mock_build():
    # Mock the 'build' function from googleapiclient.discovery
    with patch("pandasheets.build") as mock_build:
        yield mock_build


test_sheet_id = "1NUyOxbJF4cEUGfT0SEUzDk4Tcg11qCCI9IgU9LDFDD8"
test_url = f"https://docs.google.com/spreadsheets/d/{test_sheet_id}/"
# test_sheet_id = "https://docs.google.com/spreadsheets/d/1NUyOxbJF4cEUGfT0SEUzDk4Tcg11qCCI9IgU9LDFDD8/edit#gid=542492911"
