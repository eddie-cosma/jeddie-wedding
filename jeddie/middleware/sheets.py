import pathlib

from enum import Enum
from itertools import chain

from apiclient import discovery
from flask import current_app
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIAL_FILE = str(pathlib.PurePath(current_app.instance_path) / 'jeddie-wedding-8eac7493485d.json')
SPREADSHEET_ID = '19s13h3ll4MiayT41vaInAH2iNTwlGc8oYpLIdAs5nc8'
SHEET_NAME = 'Mailing List'


class RsvpList:
    class RangeName(Enum):
        recipients = ('A:A', 'Recipient(s)')
        num_recipients = ('G:G', 'Num Recipients')
        plus_one = ('H:H', 'Plus One')
        invitation_code = ('I:I', 'Invitation Code')
        rsvp = ('J:J', 'RSVP')
        plus_one_name = ('K:K', 'Plus One Name')

    def __init__(self):
        self._connect()
        self._database = dict()
        self._get_all_data()

    def _connect(self):
        credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_FILE, scopes=SCOPES)
        try:
            service = discovery.build('sheets', 'v4', credentials=credentials)
            self.sheet = service.spreadsheets()
        except HttpError:
            pass

    def _get_all_data(self):
        ranges = []
        for sheet_range in self.RangeName:
            (range_cells, _) = sheet_range.value
            ranges.append(f'{SHEET_NAME}!{range_cells}')

        results = self.sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID, ranges=ranges).execute()
        for result in results.get('valueRanges'):
            dataset_values = list(chain.from_iterable(result.get('values')))  # Convert 2d list to 1d
            dataset_name = dataset_values.pop(0)
            self._database[dataset_name] = dataset_values

    def _set_range(self, range_name: RangeName):
        (range_cells, range_title) = range_name.value

        range_cells = f'{SHEET_NAME}!{range_cells}'
        values = [[range_title]]
        values += [[i] for i in self._database.get(range_title)]
        body = {
            'values': values
        }
        self.sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_cells, valueInputOption='RAW',
                                   body=body).execute()

    def select(self, column: RangeName, value: str) -> dict:
        """Select invitee details by looking up a value in a column.

        :param column: Column being searched
        :param value: Value to look for
        :return: Dict of all values from the row selected, including index of that row in the internal database
        """

        value_list = self._database.get(column.value[1])
        try:
            index = value_list.index(value)
        except ValueError:
            return {'Error': f'Value \'{value}\' not found in column \'{column.value[1]}\''}

        invitee = dict()
        for sheet_range in self.RangeName:
            (_, range_name) = sheet_range.value
            print(range_name)
            invitee[range_name] = self._database.get(range_name)[index]
        invitee['index'] = index
        return invitee

    def update(self, column: RangeName, index: int, value: str):
        """Update a datapoint in a column at the selected index.

        :param column: Column in which update will occur
        :param index: Int index at which to update, based on the internal database index (excludes title row in sheet)
        :param value: New value
        :return:
        """
        self._database[column.value[1]][index] = value
        self._set_range(column)
