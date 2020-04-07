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
SAMPLE_SPREADSHEET_ID = '1EX5zEpBjmcHGzMVYcIw7_j6KXr9NrJyG'


def connect_sheets():
    credentials = service_account.Credentials.from_service_account_file('driveamerican-6d11d1ea30b7.json')
    # scoped_credentials = credentials.with_scopes(SCOPES)

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    return sheet


def import_data_from_sheets_to_db():
    result = connect_sheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                           range='A1:E',
                                           majorDimension='ROWS').execute()
    values = result.get('values', [])

    for row in values:
        print('%s' % (row))
        if row[1] == 'IAAI' or row[1] == 'Copart':
            auction = Auction.objects.get(auction=row[1])
            # print(re.sub(r'[^A-Za-z\s]', '', row[0]))
            # print(re.split(r'[,(\-!?:]+', row[0]))
            print(re.sub(r'[^A-Za-z\s]', '', re.split(r'[,(!?:]+', row[0])[0]))
            print('savannah =  ' + str(str_to_int(re.sub('\D', '', row[4]))))

            # TransportationPrice.objects.create(auction=auction,
            #                                    auction_location=re.sub(r'[^A-Za-z\s]', '',
            #                                                            re.split(r'[,(!?:]+', row[0])[0]),
            #                                    city=row[2], state=row[3], zip=row[4],
            #                                    port_savannah=str_to_int(re.sub('\D', '', row[5])),
            #                                    port_newark=str_to_int(re.sub('\D', '', row[6])),
            #                                    port_houston=str_to_int(re.sub('\D', '', row[7])),
            #                                    port_los_angeles=str_to_int(re.sub('\D', '', row[8])),
            #                                    port_indianapolis=str_to_int(re.sub('\D', '', row[9])))


def str_to_int(value):
    res = 0
    if value == '':
        res = 0
    else:
        res = value
    return res


if __name__ == '__main__':
    import_data_from_sheets_to_db()
