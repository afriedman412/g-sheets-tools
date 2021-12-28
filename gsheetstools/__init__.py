import pandas as pd
from googleapiclient.discovery import build
from .helpers import *


# MAJOR CODE
class gSheet:
    def __init__(self, sheet_id=None, name=None, suffix=None):
        print('loading sheet object...')
        self.suffix = suffix
        self.sheet_object = self.loadSheetObject()
    
        if name is not None:
            print('starting with new sheet...')
            self.createNewSpreadsheet(str(name))

        elif sheet_id is not None:
            print('loading sheet...')
            self.sheet_id = sheet_id
            self.action = self.sheet_object.get(spreadsheetId=self.sheet_id)

        else:
            print('starting with new sheet...')
            self.createNewSpreadsheet('Untitled Sheet')

    def __repr__(self):
        return self.sheet_id

    def loadSheetObject(self):
        """
        Creates a "sheet" object. 
        Doesn't actually load a sheet, just creates the connection with Google Sheets.
        Also manages credentials.

        Auth flow interpolated from here:
        https://developers.google.com/sheets/api/quickstart/python
        """
        creds_loaded = gAuth(self.suffix)
        service = build('sheets', 'v4', credentials=creds_loaded)
        self.sheet_object = service.spreadsheets()

        return self.sheet_object

    def createNewSpreadsheet(self, title):
        """
        Create a new spreadsheet file with provided title.
        Sets self.sheet_id to new sheet id.
        """
        spreadsheet = {
            'properties': {
                'title': title
                }
            }
        spreadsheet = self.sheet_object.create(
            body=spreadsheet,
            fields='spreadsheetId'
            ).execute()

        sheet_id = spreadsheet.get('spreadsheetId')

        print('Spreadsheet ID: {0}'.format(sheet_id))

        self.sheet_id = sheet_id
        self.action = self.sheet_object.get(spreadsheetId=self.sheet_id)

    def loadDataFromSheet(self, data_range, return_df=True, assume_headers=True):
        """
        Pulls the provided data range from the sheet_id using provided sheet_object.

        Data returned as list of lists.
        """
        try:
            result = self.sheet_object.values().get(spreadsheetId=self.sheet_id, range=data_range).execute()

            values = result.get('values', [])

            if return_df:
                if assume_headers:
                    return pd.DataFrame(values[1:], columns=values[0])
                else:
                    return pd.DataFrame(values)
            else:
                return values
                
        except HttpError as e:
            print(httpErrorParser(e))
            return None 

    def createNewSheet(self, sheet_name):
        """
        Creates a new blank sheet named 'sheet_name' in the sheet 'sheet_id'.
        """

        request_body = {
            'requests': [
                    {
                    'addSheet': 
                        {'properties': {'title': sheet_name}
                        }
                    }
                ]
            }

        try:
            response = self.sheet_object.batchUpdate(
                spreadsheetId=self.sheet_id,
                body=request_body
                ).execute()

            return response

        # escape code for duplicate name error
        except HttpError as e:
            print(httpErrorParser(e))
            return None


    def loadSheetInfo(self):
        """
        Helper function to get latest info on sheets before updating.
        """

        self.sheet_info = {
            s['properties']['title']:{
                k:v for k,v in s['properties'].items() if k is not 'title'
                } for s in self.action.execute().get('sheets')
            }

        return self.sheet_info


    def renameSheet(self, sheet_name, new_name):
        """
        Renames 'sheet_name' in the sheet 'self.sheet_id' as 'new_name.
        """
        self.loadSheetInfo()

        if sheet_name not in self.sheet_info.keys():
            print('sheet name not found')
            return

        request_body = {
            'requests': [
                    {
                    'updateSheetProperties': 
                        {'properties': {
                            'title': new_name,
                            'sheetId': self.sheet_info[sheet_name]['sheetId']
                            },
                            'fields': 'title'
                        }
                    }
                ]
            }

        try:
            response = self.sheet_object.batchUpdate(
                spreadsheetId=self.sheet_id,
                body=request_body
                ).execute()

            return response

        # escape code for duplicate name error
        except HttpError as e:
            print(httpErrorParser(e))
            return None

    def deleteSheet(self, sheet_name):
        """
        Deletes 'sheet_name' from 'self.sheet_id'.
        """
        self.loadSheetInfo()

        if sheet_name not in self.sheet_info.keys():
            print('sheet name not found')
            return

        request_body = {
            'requests': [
                    {
                    'deleteSheet': 
                        {'sheetId': self.sheet_info[sheet_name]['sheetId']}
                    }
                ]
            }

        try:
            response = self.sheet_object.batchUpdate(
                spreadsheetId=self.sheet_id,
                body=request_body
                ).execute()

            return response

        # escape code for duplicate name error
        except HttpError as e:
            print(httpErrorParser(e))
            return None

    def writeDataToSheet(self, new_data, data_range, write_setting='update'):

        value_input_option = 'RAW'
        insert_data_option = 'INSERT_ROWS'

        new_data = new_data.fillna('')
        data_out_for_upload = [new_data.columns.tolist()] + new_data.values.tolist()

        value_range_body = {
            "range": data_range,
            "values": data_out_for_upload
            }

        # if the sheet name doesn't exist, make it
        sheet_name = data_range.split('!')[0]
        self.loadSheetInfo()
        if sheet_name not in self.sheet_info.keys():
            self.createNewSheet(sheet_name)

        if write_setting == 'update':
            request = self.sheet_object.values().update(
                spreadsheetId=self.sheet_id, 
                range=data_range, valueInputOption=value_input_option,
                body=value_range_body
                )

        elif write_setting == 'append':
            request = self.sheet_object.values().append(
                spreadsheetId=self.sheet_id, 
                range=data_range, valueInputOption=value_input_option,
                body=value_range_body
                )

        else:
            print('bad write setting')
            return

        response = request.execute()

        return response

    def formatSheet(self, sheet_name='Sheet1', request_body=format_request):
        self.loadSheetInfo()
        id_ = self.sheet_info[sheet_name]['sheetId']

        request_body[0]['repeatCell']['range']['sheetId'] = id_
        request_body[1]['repeatCell']['range']['sheetId'] = id_
        request_body[2]['updateSheetProperties']['properties']['sheetId'] = id_

        self.sheet_object.batchUpdate(spreadsheetId=self.sheet_id, body=request_body).execute()

def quickSheet(data, spreadsheet_name, page_names='Sheet1'):
    """
    Creates a new spreadsheet called "spreadsheet_name" and writes "data" to it.

    By default, writes "data" to "Sheet1", or to "sheet_names" if provided

    Other input options:

        1) dict of "sheet_name:data_file" pairs
            - creates "sheet_name" and writes "data_file" to it

        2) list of data_files, no sheet_names
            - writes every "data_file" in list to sequential "Sheet1", "Sheet2" etc pages

        3) list of data_files, sheet_names
            - writes every "data_file in list to every name in "sheet_names", adding "Sheet5" etc. if it runs out of names
    """

    if page_names is None:
        page_names = 'Sheet1'

    if type(page_names) is not list:
        page_names = [page_names]

    if type(data) is dict:
        data_dict = data

    if type(data) is pd.DataFrame:
        data = [data]

    if type(data) is list:
        data_dict = {}
        for n in range(len(data)):
            try:
                data_dict[page_names[n]] = data[n]
            except KeyError:
                data_dict['Sheet{}'.format(n+1)] = data[n]

    g = gSheet(spreadsheet_name)

    for d in data_dict:
        g.createNewSheet(d)
        g.writeDataToSheet(data_dict[d].fillna(''), '{}!A:Z'.format(d))

    return g.sheet_id
    

def quickLoad(sheet_id, data_range="Sheet1!A:Z"):
    g = gSheet(sheet_id)
    df = g.loadDataFromSheet(data_range)
    return df


def quickWrite(data, sheet_id, data_range="Sheet1!A:Z"):
    g = gSheet(sheet_id)
    g.loadSheetInfo()
    
    sheet_name = data_range.split('!')[0]
    if sheet_name not in g.sheet_info.keys():
        g.createNewSheet(sheet_name)

    df = g.writeDataToSheet(data.fillna(''), data_range)
    return