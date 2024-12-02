import requests
from params import *
from database import db
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"


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

def crm_deal_update(partner):
    update_deal_url = f"https://lead-magnet.bitrix24.ru/rest/456/x29qpt47k23euvyj/crm.deal.update.json"
    # params[affise_partner_id] = partner["partner_id"]
    # params[crm_created_at] = partner["created_at"]
    # params[crm_partner_name] = partner['name']
    # params[crm_ref_partner] = partner['ref_partner']
    # params[crm_email] = partner['email']
    # params[crm_phone] = partner['phone']
    # params[crm_tg] = partner['telegram']
    # params[crm_vk] = partner['vk']
    # params[crm_skype] = partner['skype']
    # params[crm_segment_onboarding] = partner['segment_onboarding']
    # params[crm_segment_payment] = partner['segment_payment']
    # params[crm_balance] = partner['balance']
    # params[crm_exp_years] = partner['exp_years']
    # params[crm_solo_or_team] = partner['solo_or_team']
    # params[crm_verticals] = partner['verticals']
    # params[crm_thematics] = partner['thematics']
    # params[crm_sources_exp] = partner['sources_exp']
    # params[crm_sources_lm] = partner['sources_lm']
    # params[crm_sources_type] = partner['sources_type']
    # params[crm_about_us] = partner['about_us']
    # # params[crm_stage] = stage
    # params[crm_first_payment_amount] = partner['first_payment']
    # params[crm_second_payment_amount] = partner['second_payment']
    # params[crm_third_payment_amount] = partner['third_payment']
    # params[crm_fourth_payment_amount] = partner['fourth_payment']
    # params[crm_fifth_payment_amount] = partner['fifth_payment']
    # params[crm_last_payment_amount] = partner['last_payment']
    # params[crm_first_payment_roi] = partner['first_payment_roi']
    #
    # params[crm_common_roi] = partner['common_roi']
    params_test[crm_partner_id] = partner['crm_partner_id']

    params_test[crm_affmanager] = '430'
    # params_test[crm_segment_dvv] = partner['dvv_segment']

    print(f"Пробуем обновить партнера {params[crm_partner_id]} в crm битрикс")
    r = requests.get(update_deal_url, params=params_test)
    res = r.json()
    print(res)
    if res['result'] is True:
        print(f"Успешно обновили партнера {params[crm_partner_id]}")
def crm_deal_add(partner: dict, stage: str):
    add_deal_url = f"https://lead-magnet.bitrix24.ru/rest/456/x29qpt47k23euvyj/crm.deal.add.json"
    params[affise_partner_id] = partner["partner_id"]
    params[crm_created_at] = partner["created_at"]
    params[crm_partner_name] = partner['name']
    params[crm_ref_partner] = partner['ref_partner']
    params[crm_email] = partner['email']
    params[crm_phone] = partner['phone']
    params[crm_tg] = partner['telegram']
    params[crm_vk] = partner['vk']
    params[crm_skype] = partner['skype']
    params[crm_segment_onboarding] = partner['segment_onboarding']
    params[crm_segment_payment] = partner['segment_payment']
    params[crm_balance] = partner['balance']
    params[crm_exp_years] = partner['exp_years']
    params[crm_solo_or_team] = partner['solo_or_team']
    params[crm_verticals] = partner['verticals']
    params[crm_thematics] = partner['thematics']
    params[crm_sources_exp] = partner['sources_exp']
    params[crm_sources_lm] = partner['sources_lm']
    params[crm_sources_type] = partner['sources_type']
    params[crm_about_us] = partner['about_us']
    params[crm_stage] = stage
    params[crm_first_payment_amount] = partner['first_payment']
    params[crm_second_payment_amount] = partner['second_payment']
    params[crm_third_payment_amount] = partner['third_payment']
    params[crm_fourth_payment_amount] = partner['fourth_payment']
    params[crm_fifth_payment_amount] = partner['fifth_payment']
    params[crm_last_payment_amount] = partner['last_payment']

    params[crm_first_payment_roi] = partner['first_payment_roi']
    params[crm_common_roi] = partner['common_roi']


    print(f"Пробуем добавить партнера {partner['partner_id']} в crm битрикс")
    r = requests.get(add_deal_url, params=params)
    res = r.json()
    print(res)
    crm_partner_id = res['result']
    if isinstance(crm_partner_id, int):
        print(f"Успешно добавили партнера {partner['partner_id']} в crm битрикс")
        partner_id = partner['partner_id']
        db.add_crm_partner_id(crm_partner_id, partner_id)
    else:
        print(f"Не смогли добавить партнера {partner['partner_id']} в crm. {res['result']}")

def crm_deal_delete(crm_id):
    delete_deal = f"https://lead-magnet.bitrix24.ru/rest/456/x29qpt47k23euvyj/crm.deal.delete.json?ID={crm_id}"
    print(f"Пробуем удалить партнера {crm_id} из crm битрикс")
    r = requests.get(delete_deal)
    res = r.json()
    if res['result'] is True:
        print(f"Успешно удалили партнера {crm_id}")
def sheets_get_partners():
    service = update_google_creds()
    values = service.spreadsheets().values().get(
        spreadsheetId='1wKT-pj7744y4FmwcVuCiYRa5xsiSSt8_YmjJU8ExwLI',
        range='Лист1!A1:B',
        majorDimension='ROWS'
    ).execute()
    # res = tuple(partner[0] for partner in values['values'])
    parters_crm_info_list = []

    for value in values['values']:
        partner_info = {'partner_id': value[0],
                        'crm_partner_id': value[1]}
        parters_crm_info_list.append(partner_info)


    return parters_crm_info_list









# if __name__ == '__main__':
#     txt_file_partners = get_txt_file_partners()
#     partners_for_crm = db.get_partners_by_id(txt_file_partners)
#     for i in partners_for_crm:
#         print(i)
#     for partner in partners_for_crm:
#         if "banned" in partner['status']:
#             crm_deal_update(partner, stage_froder)
#             continue
#         elif partner['fifth_payment'] > 0 and partner['fifth_payment'] != partner['last_payment']:
#             crm_deal_update(partner, stage_active_partner)
#             continue
#         elif partner['fifth_payment'] > 0 and partner['fifth_payment'] == partner['last_payment']:
#             crm_deal_update(partner, stage_fifth_payment)
#             continue
#         elif partner['fourth_payment'] > 0 and partner['fifth_payment'] == 0:
#             crm_deal_update(partner, stage_fourth_payment)
#             continue
#         elif partner['third_payment'] > 0 and partner['fourth_payment'] == 0:
#             crm_deal_update(partner, stage_third_payment)
#             continue
#         elif partner['second_payment'] > 0 and partner['third_payment'] == 0:
#             crm_deal_update(partner, stage_second_payment)
#             continue
#         elif partner['first_payment'] > 0 and partner['second_payment'] == 0:
#             crm_deal_update(partner, stage_first_payment)
#             continue
#         elif partner['balance'] >= 4000 and partner['balance'] < 5000:
#             crm_deal_update(partner, stage_ballance_4000)
#             continue
#         elif partner['balance'] >= 3000 and partner['balance'] < 4000:
#             crm_deal_update(partner, stage_ballance_3000)
#             continue
#         elif partner['balance'] >= 2000 and partner['balance'] < 3000:
#             crm_deal_update(partner, stage_ballance_2000)
#             continue
#         elif partner['balance'] >= 1000 and partner['balance'] < 2000:
#             crm_deal_update(partner, stage_ballance_1000)
#             continue
#         elif partner['balance'] > 0 and partner['balance'] < 1000:
#             crm_deal_update(partner, stage_first_traffic)
#             continue
#         elif "True" in partner['connect_offers']:
#             crm_deal_update(partner, stage_connect_offers)
#             continue
#         elif "True" in partner['hello_answer']:
#             crm_deal_update(partner, stage_hello_answer)
#             continue
#         else:
#             crm_deal_update(partner, stage_new)
#             continue

# if __name__ == '__main__':
#     txt_file_partners = get_txt_file_partners()
#     partners_for_crm = db.get_partners_by_id(txt_file_partners)
#     for i in partners_for_crm:
#         print(i)
#     for partner in partners_for_crm:
#         if "banned" in partner['status']:
#             crm_deal_add(partner, stage_froder)
#             continue
#         elif partner['fifth_payment'] > 0 and partner['fifth_payment'] != partner['last_payment']:
#             crm_deal_add(partner, stage_active_partner)
#             continue
#         elif partner['fifth_payment'] > 0 and partner['fifth_payment'] == partner['last_payment']:
#             crm_deal_add(partner, stage_fifth_payment)
#             continue
#         elif partner['fourth_payment'] > 0 and partner['fifth_payment'] == 0:
#             crm_deal_add(partner, stage_fourth_payment)
#             continue
#         elif partner['third_payment'] > 0 and partner['fourth_payment'] == 0:
#             crm_deal_add(partner, stage_third_payment)
#             continue
#         elif partner['second_payment'] > 0 and partner['third_payment'] == 0:
#             crm_deal_add(partner, stage_second_payment)
#             continue
#         elif partner['first_payment'] > 0 and partner['second_payment'] == 0:
#             crm_deal_add(partner, stage_first_payment)
#             continue
#         elif partner['balance'] >= 4000 and partner['balance'] < 5000:
#             crm_deal_add(partner, stage_ballance_4000)
#             continue
#         elif partner['balance'] >= 3000 and partner['balance'] < 4000:
#             crm_deal_add(partner, stage_ballance_3000)
#             continue
#         elif partner['balance'] >= 2000 and partner['balance'] < 3000:
#             crm_deal_add(partner, stage_ballance_2000)
#             continue
#         elif partner['balance'] >= 1000 and partner['balance'] < 2000:
#             crm_deal_add(partner, stage_ballance_1000)
#             continue
#         elif partner['balance'] > 0 and partner['balance'] < 1000:
#             crm_deal_add(partner, stage_first_traffic)
#             continue
#         elif "True" in partner['connect_offers']:
#             crm_deal_add(partner, stage_connect_offers)
#             continue
#         elif "True" in partner['hello_answer']:
#             crm_deal_add(partner, stage_hello_answer)
#             continue
#         else:
#             crm_deal_add(partner, stage_new)
#             continue

