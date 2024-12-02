import db_manualy as db
import requests
import datetime as dt
import traceback
import os
import time
import logger as log
import crm_manualy as crm
from sheets import sheets


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"
# SAMPLE_SPREADSHEET_ID = "1X5Op6GMDDrSUbpw-LhTwQsdt3xLDyKV4CUyCPkXWpP4"

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'

def sheets_get_partners():
    service = sheets.update_google_creds()
    values = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range='обновление статусов!A2:AO',
        majorDimension='ROWS'
    ).execute()
    sheets_partners_info_list = []
    for partner in values['values']:
        print(partner)
        sheets_partner_info = {
           'partner_id': partner[0],
           'target': partner[1],
           'created_at': partner[2],
           'name': partner[3],
           'ref_partner': partner[4],
           'email': partner[5],
           'phone': partner[6],
           'vk': partner[7],
           'skype': partner[8],
           'telegram': partner[9],
           'send_hello_error': partner[10],
           'send_hello': partner[11],
           'hello_answer': partner[12],
           'form': partner[13],
           'connect_offers': partner[14],
           'segment_onboarding': partner[15],
           'segment_payment' : partner[16],
           'balance' : partner[17],
           'first_payment': partner[18],
           'second_payment': partner[19],
           'third_payment': partner[20],
           'fourth_payment': partner[21],
           'fifth_payment': partner[22],
           'last_payment': partner[23],
           'first_payment_roi': partner[24],
           'common_roi': partner[25],
           'first_payment_date': partner[26],
           'last_payment_date': partner[27],
           'deal_cycle': partner[28],
           'from_last_payment_days' : partner[29],
           'status': partner[30],
           'froder': partner[31],
           'exp_years': partner[32],
           'solo_or_team': partner[33],
           'verticals': partner[34],
           'thematics': partner[35],
           'sources_exp': partner[36],
           'sources_lm': partner[37],
           'sources_type': partner[38],
           'about_us': partner[39],
           'crm_stage': partner[40]}
        sheets_partners_info_list.append(sheets_partner_info)

    return sheets_partners_info_list


def main():
    log.msg.info('Пробуем получить список вебов из гугл-таблицы')
    partners_sheets_list = sheets_get_partners()
    log.msg.info('Успешно получили список вебов из гугл-таблицы')
    partners_for_sheets_list = []
    # partners_list_from_db = db.get_partners_by_id(partners_sheets_tuple)
    log.msg.info('Пробуем получить инфо по вебам от аффайз')
    db.update_partner_status(partners_sheets_list)
    # for partner in updated_partners_list:
    #     partners_for_sheets_list.append(db.get_update_partner_for_sheets(partner['partner_id']))
    # sheets_add_update_partners(partners_for_sheets_list)
    # partners_for_crm = db.get_partners_by_id(partners_sheets_tuple)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        log.msg.error(f"Поймали исключение  {str(traceback.print_exc())}")




