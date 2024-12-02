import requests
from database import db
import time
import os
from logs import logger as log

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"
# SAMPLE_SPREADSHEET_ID = "1X5Op6GMDDrSUbpw-LhTwQsdt3xLDyKV4CUyCPkXWpP4"


def update_google_creds():
    creds = None
    if os.path.exists("../sheets/token.json"):
        creds = Credentials.from_authorized_user_file("../sheets/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../sheets/creds.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("../sheets/token.json", "w") as token:
            token.write(creds.to_json())
    service = build("sheets", "v4", credentials=creds)
    return service

# def sheets_get_partners():
#     service = update_google_creds()
#     values = service.spreadsheets().values().get(
#         spreadsheetId=SAMPLE_SPREADSHEET_ID,
#         range='CRM (авто)!A2:AO',
#         majorDimension='ROWS'
#     ).execute()
#     res = tuple(partner[0] for partner in values['values'])
#     return res

def sheets_get_form_partners():
    service = update_google_creds()
    values = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range='crm даня!A2:L',
        majorDimension='ROWS'
    ).execute()
    form_partners_info_list = []
    for partner in values['values']:
        form_partner_info = {'segment': partner[0], 'name': partner[1], 'partner_id': partner[2],
                             'experience': partner[3], 'verticals': partner[4], 'sources_exp': partner[5],
                             'sources_lm': partner[6], 'thematics': partner[7], 'exp_years': partner[8],
                             'sources_type': partner[9], 'solo_or_team': partner[10], 'about_us': partner[11]}
        form_partners_info_list.append(form_partner_info)

    return form_partners_info_list


def add_update_partners(partners_list: list):
    service = update_google_creds()
    log.msg.info(f"Пробуем добавить обновленных вебов в гугл таблицу")
    service.spreadsheets().values().batchClear(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        body={"ranges": "CRM (авто) тест!A2:AO"}
    ).execute()
    log.msg.info(f"Успешно очистили таблицу")
    time.sleep(1)
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "CRM (авто) тест!A2:AO",
                 "majorDimension": "COLUMNS",
                 "values": [
                     [partner['partner_id'] for partner in partners_list],
                     [partner['target'] for partner in partners_list],
                     [partner['created_at'] for partner in partners_list],
                     [partner['name'] for partner in partners_list],
                     [partner['ref_partner'] for partner in partners_list],
                     [partner['email'] for partner in partners_list],
                     [partner['phone'] for partner in partners_list],
                     [partner['vk'] for partner in partners_list],
                     [partner['skype'] for partner in partners_list],
                     [partner['telegram'] for partner in partners_list],
                     [partner['send_hello_error'] for partner in partners_list],
                     [partner['send_hello'] for partner in partners_list],
                     [partner['hello_answer'] for partner in partners_list],
                     [partner['form'] for partner in partners_list],
                     [partner['connect_offers'] for partner in partners_list],
                     [partner['segment_onboarding'] for partner in partners_list],
                     [partner['segment_payment'] for partner in partners_list],
                     [partner['balance'] for partner in partners_list],
                     [partner['first_payment'] for partner in partners_list],
                     [partner['second_payment'] for partner in partners_list],
                     [partner['third_payment'] for partner in partners_list],
                     [partner['fourth_payment'] for partner in partners_list],
                     [partner['fifth_payment'] for partner in partners_list],
                     [partner['last_payment'] for partner in partners_list],
                     [partner['first_payment_roi'] for partner in partners_list],
                     [partner['common_roi'] for partner in partners_list],
                     [partner['first_payment_date'] for partner in partners_list],
                     [partner['last_payment_date'] for partner in partners_list],
                     [partner['deal_cycle'] for partner in partners_list],
                     [partner['from_last_payment_days'] for partner in partners_list],
                     [partner['status'] for partner in partners_list],
                     [partner['froder'] for partner in partners_list],
                     [partner['exp_years'] for partner in partners_list],
                     [partner['solo_or_team'] for partner in partners_list],
                     [partner['verticals'] for partner in partners_list],
                     [partner['thematics'] for partner in partners_list],
                     [partner['sources_exp'] for partner in partners_list],
                     [partner['sources_lm'] for partner in partners_list],
                     [partner['sources_type'] for partner in partners_list],
                     [partner['about_us'] for partner in partners_list],
                     [partner['crm_stage'] for partner in partners_list],
                 ]
                 },
            ]
        }
    ).execute()

    log.msg.info(f"Успешно вставили обновленных вебов в гугл таблицу")