import pathlib

import pandas
import pandas as pd

from apiclient import discovery
from flask import current_app
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIAL_FILE = str(pathlib.PurePath(current_app.instance_path) / 'jeddie-wedding-8eac7493485d.json')
SPREADSHEET_ID = '19s13h3ll4MiayT41vaInAH2iNTwlGc8oYpLIdAs5nc8'
SHEET_NAME = 'Mailing List_Test'


class RsvpList:

    def __init__(self):
        self._connect()
        self._database = self._get_all_data()

    def _connect(self):
        credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_FILE, scopes=SCOPES)
        try:
            service = discovery.build('sheets', 'v4', credentials=credentials)
            self.sheet = service.spreadsheets()
        except HttpError:
            pass

    def _get_all_data(self) -> pandas.DataFrame:
        results = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{SHEET_NAME}!A:K',
                                          majorDimension='ROWS').execute()
        db = pd.DataFrame(results.get('values'))
        db.columns = db.iloc[0]
        return db[1:]  # Return data without header

    def _set_range(self):
        body = {
            'values': self._database.values.tolist()
        }
        self.sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f'{SHEET_NAME}!A2:K', valueInputOption='RAW',
                                   body=body).execute()

    def select(self, column: str, value: str) -> str:
        """Select invitee details by looking up a value in a column."""

        return self._database[self._database[column] == value].to_csv()

    def update(self, column: str, value: str, where_column: str, where_value: str) -> str:
        """Update a datapoint in a column at the selected index."""

        self._database.loc[self._database[where_column] == where_value, column] = value
        self._set_range()
        return self._database[self._database[where_column] == where_value].to_csv()
