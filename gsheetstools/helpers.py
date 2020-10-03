import os
# from pathlib import Path
import json
from shutil import copyfile
import pickle
import numpy as np
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# HELPER FUNCTIONS
def httpErrorParser(e):
    e_dict = json.loads(e.content.decode("utf-8"))
    return e_dict['error']['message']

def gAuth(creds_file=None):
    if creds_file is None:
        creds_file = 'credentials.json'

    if os.name == 'nt':
        base_path = os.environ["APPDATA"] + 'gst/'

    else:
        base_path = os.path.expanduser('~/') + '.config/gst/'
    
    # path = Path(base_path)
    os.makedirs(base_path, exist_ok=True)

    token_path = base_path + 'token.pickle'
    creds_path = base_path + creds_file
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    try:
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES)
        return creds

    except:

        if not os.path.exists(creds_path):
            if [f for f in os.listdir(os.path.expanduser('~/')) if 'apps.googleusercontent.com' in f]:
                try:
                    cred_file = [
                        f for f in os.listdir(os.path.expanduser('~/')) if 'apps.googleusercontent.com' in f][0]
                    copyfile(
                        os.path.expanduser('~/') + cred_file, creds_path
                    )
                except FileNotFoundError:
                    print('credentials not found in home dir')
                    return
                     

        creds = None
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                print('loading token...')
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            print('getting new credentials...')
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES) # replaced 'credentials.json'
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            print('saving new credentials...')
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        return creds

class NpEncoder(json.JSONEncoder):
    """
    if I'm using it, it's from here:
    https://stackoverflow.com/questions/56250514/how-to-tackle-with-error-object-of-type-int32-is-not-json-serializable
    """
    def defaultEncode(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

format_request =  {
    "requests": [
        {
            "repeatCell": {
                "range": {
                    "sheetId": ''
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment" : "CENTER"

                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": '',
                    "startRowIndex": 0,
                    "endRowIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "fontSize": 10,
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat)"
            }
        },
        
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": '',
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                },
                "fields": "gridProperties.frozenRowCount"
            }
        }
    ]
}