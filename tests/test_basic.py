from pandasheets import gSheet
import pandas as pd


def test_load():
    g = gSheet(
        sheet_id="https://docs.google.com/spreadsheets/d/1NUyOxbJF4cEUGfT0SEUzDk4Tcg11qCCI9IgU9LDFDD8/edit#gid=542492911",
        suffix="af412",
    )

    assert g.load_from_range("Sheet1").shape == (6, 2)
    assert g.page_names == ["Sheet1", "Sheet2", "Sheet3"]

    g.create_new_page("hey")
    assert g.page_names == ["Sheet1", "Sheet2", "Sheet3", "hey"]

    g.rename_page("hey", "yeh")
    assert g.page_names == ["Sheet1", "Sheet2", "Sheet3", "yeh"]

    g.delete_page("yeh")
    assert g.page_names == ["Sheet1", "Sheet2", "Sheet3"]

    df = pd.DataFrame([{"x": 100, "y": 200}, {"x": 300, "y": 400}])

    g.write_to_page(df, "hey")
    assert g.load_from_range("hey").shape == (2, 2)
