import db_manualy as db
import requests
import datetime as dt
import traceback
import os
import time
import logger as log
import crm_manualy as crm



from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DVV_CRM_SPREADSHEET_ID = "1MAvtUqZvnvo7H2YTpJ_rKfzhKXrwzsMvZmoUi-42gtk"
# SAMPLE_SPREADSHEET_ID = "1X5Op6GMDDrSUbpw-LhTwQsdt3xLDyKV4CUyCPkXWpP4"

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'
def update_google_creds():
    creds = None
    if os.path.exists("../token.json"):
        creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../creds.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("../token.json", "w") as token:
            token.write(creds.to_json())
    service = build("sheets", "v4", credentials=creds)
    return service

def sheets_get_partners():
    service = update_google_creds()
    values = service.spreadsheets().values().get(
        spreadsheetId=DVV_CRM_SPREADSHEET_ID,
        range='Никита!A2:J',
        majorDimension='ROWS'
    ).execute()

    sheets_partners_info_list = []
    for partner in values['values']:
        sheets_partner_info = {
           'dvv_segment': partner[0],
           'partner_id': partner[1],
           'crm_partner_id': partner[2],
           'name': partner[3],
           'phone': partner[4],
           'email': partner[5],
           'telegram': partner[6],
           'vk': partner[7],
           'thematics': partner[8],
            'sources_lm': partner[9],
           # 'common_roi': partner[10]
        }
        sheets_partners_info_list.append(sheets_partner_info)

    return sheets_partners_info_list


def main():
    log.msg.info('Пробуем получить список вебов из гугл-таблицы')
    partners_sheets_list = sheets_get_partners()
    log.msg.info('Успешно получили список вебов из гугл-таблицы')
    partners_for_sheets_list = []
    log.msg.info('Пробуем получить инфо по вебам от аффайз')
    db.update_dvv_partners_status(partners_sheets_list)

    # for partner in partners_sheets_list:
    #     crm.crm_deal_update(partner)

    # for partner in partners_sheets_list:
    #     print(partner)

    # for partner in updated_partners_list:
    #     partners_for_sheets_list.append(db.get_update_partner_for_sheets(partner['partner_id']))
    # sheets_add_update_partners(partners_for_sheets_list)
    # partners_for_crm = db.get_partners_by_id(partners_sheets_tuple)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        log.msg.error(f"Поймали исключение  {str(traceback.print_exc())}")




