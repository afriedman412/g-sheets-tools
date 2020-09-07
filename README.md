# Google Sheets Tools

`Google Sheets Tools` is a wrapper for the Google Sheets API that streamlines the process of moving data in and out of Sheets, especially for Pandas users. (I built this because I got tired of exporting and uploading .csv files.)

# Before you install...
To run `GST`, you need your own App under your own Google account. This is easy!

1. Go to the [Google Developers Console](https://console.developers.google.com/cloud-resource-manager). Create a new app.
2. Go to the [Google API Library](https://console.developers.google.com/apis/library) and find the Google Sheets API.
3. Click "Enable"
4. Go to the [Credentials](https://console.developers.google.com/apis/credentials) page, either through the provided link or the in the console sidebar.
5.  If Google requires you to set up the OAuth Consent Screen, select "external" and then name your app whatever you would like. (This is the only thing you need to do on the OAuth Consent Screen menu!)
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
**Make a GST object:**  
Duplicate names are OK, Sheets automatically assigns unique ID's.

```
# pass a sheet id (the alphanumerical code from the sheet url) to load an existing spreadsheet
g = gSheet(sheet_id='1pMvgod2nteAIIRJbplMqkllLaXpK15_046Zz_82b4zg')

# pass a name to create a new spreadsheet
g = gSheet(name='new spreadsheet')

# pass nothing to create a new spreadsheet called 'Untitled"
g = gSheet()
```


**Download data with a GST object:**  
Data ranges are formatted "Sheet Name!first cell:last cell". 

```
# pass a data range
data = g.loadDataFromSheet('cities!A:Z')
```

**Upload data with a GST object:**  
This overwrites data by default. pass `write_setting='append'` to preserve existing data.

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
**quickSheet**  
Create a new spreadsheet from one or many data sources.
```

```




# Example

