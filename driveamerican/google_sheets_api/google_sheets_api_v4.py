from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re
import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(os.path.dirname(BASE_DIR), "driveamerican")
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'driveamerican.settings'
import django

django.setup()
from driveamericanapp.models import Auction, TransportationPrice

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# SAMPLE_SPREADSHEET_ID = '1IG13mYrF1FGEWeFQ0ZaJfFVvYUOFVxiGZylVD8wxEic'
JSON_CONFIG = 'driveamerican-6d11d1ea30b7.json'


class GoogleSheetsAPI:
    def __init__(self, json_config):
        try:
            credentials = service_account.Credentials.from_service_account_file(json_config)
            service = build('sheets', 'v4', credentials=credentials)
            self.sheet = service.spreadsheets()
        except FileNotFoundError:
            raise FileNotFoundError

    def import_data_from_sheets_to_db(self, spreadsheet_id, auction_name):
        result = self.sheet.values().get(spreadsheetId=spreadsheet_id,
                                         range='A2:E',
                                         majorDimension='ROWS').execute()
        values = result.get('values', [])
        for row in values:
            auction = Auction.objects.get(auction=auction_name)
            auction_location = str(row[0][0:-4])
            state = str(row[0][-2:])
            print(str(auction_location) + ' ' + str(state))
            TransportationPrice.objects.create(auction=auction,
                                               auction_location=auction_location,
                                               state=state,
                                               port_savannah=row[1],
                                               port_newark=row[3],
                                               port_houston=row[4],
                                               port_los_angeles=row[2])

    def delete_all_row_in_table_transportation_prices(self):
        TransportationPrice.objects.all().delete()


SPREADSHEET_ID = '1Uz9k2Xbow6lnnSo6qHkZRB-9wUBSAVDKKD_xflL3tkA'
if __name__ == '__main__':
    sheet = GoogleSheetsAPI(JSON_CONFIG)
    # sheet.import_data_from_sheets_to_db(SPREADSHEET_ID, 'Copart')
