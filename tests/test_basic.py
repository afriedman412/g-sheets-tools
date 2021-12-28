from gsheetstools import *
import pandas as pd

def test_load():
    g_service = gSheet(sheet_id="1WDqZsdZuFp-CzIjQqTaWCqyEWSHEz0YrfhkOzoBQlM0", 
        suffix="cd_service")
    
    g_user = gSheet(sheet_id="1b_mclyAuvfj2lk1hpOruSUJNS2ozIru3t4aefqyVfJs",
        suffix="af412")

    df_service = g_service.loadDataFromSheet('macro_tags')
    df_user = g_user.loadDataFromSheet("Sheet1")

    assert df_service.shape == (253, 6)
    assert df_user.shape == (2, 3)