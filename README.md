# Google Sheets Tools

`G Sheets Tools` is a wrapper for the Google Sheets API that streamlines the process of moving data in and out of Sheets, especially for Pandas users. (I built this because I got tired of exporting and uploading .csv files.)

# Before you install...
This package allows you to interface with your Google Sheets docs, but you still need to make a dummy Google App that runs the Sheets API to use it. It's easy! Here's how.

1. Go to the [Google Developers Console](https://console.developers.google.com/cloud-resource-manager). Create a new app.
2. Go to the [Google API Library](https://console.developers.google.com/apis/library) and find the Google Sheets API.
3. Click "Enable"
4. Go to the [Credentials](https://console.developers.google.com/apis/credentials) page, either through the provided link or the in the console sidebar.
5.  Follow the prompt to open the OAuth Consent Screen and name your app. _(This is the only thing you need to do on this page!)_
6. Click "+ Create Credentials" at the top of the screen and select "OAuth client ID".
7. Select "Desktop app" from the "Application type" menu and put whatever you like in "Name".
8. You should now see your OAuth Client ID on the Credentials page.
9. Click the arrow on the right side of the menu to download your credentials.
10. Save them in your home directory!

# Installation
To install with pip, run

`pip install g_sheets_tools`

You can also clone this repository and run `python setup.py install`.

# Basic Usage
**Make a gSheet object:**  
Duplicate names are OK, Sheets automatically assigns unique ID's.

```
# pass a sheet id (the alphanumerical code from the sheet url) to load an existing spreadsheet
g = gSheet(sheet_id='1pMvgod2nteAIIRJbplMqkllLaXpK15_046Zz_82b4zg')

# pass a name to create a new spreadsheet
g = gSheet(name='new spreadsheet')

# pass nothing to create a new spreadsheet called 'Untitled"
g = gSheet()
```


**Download data with a gSheet object:**  
Data ranges are formatted "Sheet Name!first cell:last cell". 

```
# pass a data range
data = g.loadDataFromSheet('cities!A:Z')
```

**Upload data with a gSheet object:**  
This overwrites data by default. Pass `write_setting='append'` to preserve existing data.

```
# pass a dataframe and a destination
new_cities_df = pd.read_csv('new_cities.csv)
g.writeDataToSheet(new_cities_df, 'cities!A:Z')
```

**Other Functions**

```
# create a new sheet within the spreadsheet
g.createNewSheet('new sheet name')

# rename an existing sheet
g.renameSheet('current sheet name', 'new sheet name')

# delete a sheet
g.deleteSheet('sheet to delete')
```

# Standalone Functions
There are standalone functions that allow you to quickly load and write data to a sheet without creating a `gSheet` object

```
# create a new spreadsheet and write data to it
# this is flexible -- try passing it a dictionary of sheet name/data pairs!
quickSheet(data, new_spreadsheet_name, new_sheet_name)

# load data from a sheet
data = quickLoad(sheet_id, data_range)

# write data to a sheet
quickWrite(data, sheet_id, data_range)
```

