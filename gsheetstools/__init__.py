import pandas as pd
from googleapiclient.discovery import build
from typing import Union
from .helpers import *

# MAJOR CODE
class gSheet:
    def __init__(
        self, 
        sheet_id: str=None, 
        name: str=None, 
        suffix: str=None
        ):
        self.suffix = suffix
        self.load_sheet_object()
    
        if name is not None:
            print('starting with new sheet...')
            self.create_new_spreadsheet(str(name))

        elif sheet_id is not None:
            if "docs.google.com" in sheet_id:
                # handles sheet urls
                sheet_id = sheet_id.split("d/")[1].split("/")[0]
            print('loading sheet...')
            self.sheet_id = sheet_id
            
        else:
            raise ValueError("no name or sheet_id provided!")

        self.load_sheet()

    def __repr__(self):
        return self.sheet_id

    def load_sheet(self):
        self.load_sheet_object()
        self.action = self.sheet_object.get(spreadsheetId=self.sheet_id)
        self.load_page_info()

    def load_sheet_object(self):
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

    def create_new_spreadsheet(self, title):
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

        self.sheet_id = spreadsheet.get('spreadsheetId')

        print(f'Spreadsheet ID: {self.sheet_id}')
        return
        

    def load_from_range(self, data_range, return_df=True, assume_headers=True):
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

    def create_new_page(self, page_name):
        """
        Creates a new blank page named 'page_name' in the loaded sheet.
        """

        request_body = {
            'requests': [
                    {
                    'addSheet': 
                        {'properties': {'title': page_name}
                        }
                    }
                ]
            }

        try:
            response = self.sheet_object.batchUpdate(
                spreadsheetId=self.sheet_id,
                body=request_body
                ).execute()
            self.load_page_info()
            return response

        # escape code for duplicate name error
        except HttpError as e:
            print(httpErrorParser(e))
            return None

    def load_page_info(self):
        """
        Loads info for all pages and page names.
        """
        self.page_info = {
            s['properties']['title']:{
                k:v for k,v in s['properties'].items() if k is not 'title'
                } for s in self.action.execute().get('sheets')
            }

        self.page_names = list(self.page_info.keys())

    def check_page_name(self, page_names: Union[list, str], create: bool=False):
        """
        Checks if a page name exists. If it doesn't either create new page (create=True) or raise an error.
        """
        self.load_page_info()
        if isinstance(page_names, str):
            page_names = [page_names]
        for n in page_names:
            if n not in self.page_names:
                if create:
                    self.create_new_page(n)
                else:
                    raise ValueError(f"page {n} does not exist")
        return


    def rename_page(self, current_name, new_name):
        """
        Renames 'current_name' in the sheet 'self.sheet_id' as 'new_name.
        """
        self.check_page_name(current_name, new_name)
            
        request_body = {
            'requests': [
                    {
                    'updateSheetProperties': 
                        {'properties': {
                            'title': new_name,
                            'sheetId': self.page_info[current_name]['sheetId']
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
            self.load_page_info()
            return response

        # escape code for duplicate name error
        except HttpError as e:
            print(httpErrorParser(e))
            return None

    def delete_page(self, page_name):
        """
        Deletes 'page_name' from 'self.sheet_id'.
        """
        self.check_page_name(page_name)

        request_body = {
            'requests': [
                    {
                    'deleteSheet': 
                        {'sheetId': self.page_info[page_name]['sheetId']}
                    }
                ]
            }

        try:
            response = self.sheet_object.batchUpdate(
                spreadsheetId=self.sheet_id,
                body=request_body
                ).execute()
            self.load_page_info()
            return response

        # escape code for duplicate name error
        except HttpError as e:
            print(httpErrorParser(e))
            return None

    def format_df(self, df):
        """
        Formats dataframe for upload to google sheets. Fills missing entries and converts times to strings.
        """
        df = df.fillna('')
        for c in df.select_dtypes(include=['datetime']).columns:
            df[c] = df[c].astype(str)

        return df

    def write_to_page(self, new_data: pd.DataFrame, data_range, write_setting='update'):

        value_input_option = 'RAW'
        insert_data_option = 'INSERT_ROWS'

        new_data = self.format_df(new_data)
        data_out_for_upload = [new_data.columns.tolist()] + new_data.values.tolist()

        value_range_body = {
            "range": data_range,
            "values": data_out_for_upload
            }

        # if the sheet name doesn't exist, make it
        page_name = data_range.split('!')[0]
        self.check_page_name(page_name, create=True)

        if write_setting not in ['update', 'append']:
            raise ValueError("bad write setting")

        if write_setting == 'update':
            request = self.sheet_object.values().update(
                spreadsheetId=self.sheet_id, 
                range=data_range, valueInputOption=value_input_option,
                body=value_range_body
                )

        if write_setting == 'append':
            request = self.sheet_object.values().append(
                spreadsheetId=self.sheet_id, 
                range=data_range, valueInputOption=value_input_option,
                body=value_range_body
                )

        response = request.execute()

        return response

    def format_sheet(self, page_name='Sheet1', request_body=format_request):
        self.load_page_info()
        id_ = self.page_info[page_name]['sheetId']

        request_body[0]['repeatCell']['range']['sheetId'] = id_
        request_body[1]['repeatCell']['range']['sheetId'] = id_
        request_body[2]['updateSheetProperties']['properties']['sheetId'] = id_

        self.sheet_object.batchUpdate(spreadsheetId=self.sheet_id, body=request_body).execute()

def quick_sheet(data, spreadsheet_name, page_names='Sheet1'):
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
        g.create_new_page(d)
        g.write_data(data_dict[d].fillna(''), '{}!A:Z'.format(d))

    return g.sheet_id
    
def quickLoad(sheet_id, data_range="Sheet1!A:Z"):
    g = gSheet(sheet_id)
    df = g.load_data_from_sheet(data_range)
    return df

def quickWrite(data, sheet_id, data_range="Sheet1!A:Z"):
    g = gSheet(sheet_id)
    g.loadSheetInfo()
    
    sheet_name = data_range.split('!')[0]
    if sheet_name not in g.sheet_info.keys():
        g.create_new_page(sheet_name)

    df = g.write_data(data.fillna(''), data_range)
    return