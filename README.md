# README #
Functions for easy importing/exporting from google sheets, especially for pandas.

```python
from google_sheets_tools import *
import pandas as pd

%load_ext autoreload
```

### Your Sheets Code

Input your data


```python
sheet_id = '1Be9CucUdoZ0AKIORHr208F3Jq1cnHhRwZHegXhQNV9A'
sheet_name = 'Everlane BP'
sheet_range = 'C1:C300'
data_range = '!'.join([sheet_name, sheet_range])
```

Make a sheet object.


```python
sheet_object = loadSheetObject()
```

Load your data from the sheet.


```python
data_in = loadDataFromSheet(sheet_id, data_range, sheet_object)
```

Prep output.


```python
data_out = data_in

new_sheet_id = '11d-tyk8cesRUfc-53EZPqRvOC4Jth9smdELKEcNNu-E'
new_sheet_name = 'new sheet'
new_sheet_range = 'A:Z'
new_data_range = '!'.join([new_sheet_name, new_sheet_range])

data_out_for_upload = [data_out.columns.tolist()] + data_out.values.tolist()
```

Create new sheet if needed.


```python
createNewSheet(new_sheet_name, new_sheet_id, sheet_object)
```




    {'spreadsheetId': '11d-tyk8cesRUfc-53EZPqRvOC4Jth9smdELKEcNNu-E',
     'replies': [{'addSheet': {'properties': {'sheetId': 1127381843,
         'title': 'new sheet',
         'index': 5,
         'sheetType': 'GRID',
         'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}}]}



Update or append new data.


```python
# write_setting = 'append' if you don't want to overwrite old data
writeDataToSheet(data_out_for_upload, new_data_range, new_sheet_id, sheet_object)
```




    {'spreadsheetId': '11d-tyk8cesRUfc-53EZPqRvOC4Jth9smdELKEcNNu-E',
     'updatedRange': "'new sheet'!A1:A300",
     'updatedRows': 292,
     'updatedColumns': 1,
     'updatedCells': 292}