from database import db
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

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"
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

def get_partners_txt_file():
    with open('../novoreg_table/update_partners.txt', 'r') as file:
        partners_form_check_list = []
        for i in file:
            partners_form_check_list.append(i.strip('\n'))
        return partners_form_check_list

def sheets_get_partners():
    service = update_google_creds()
    values = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range='обновление статусов!A2:AO',
        majorDimension='ROWS'
    ).execute()
    res = tuple(partner[0] for partner in values['values'])
    return res


def affise_get_update_data(partners_info_list):
    partners_list = []
    for _ in range(5):
        try:
            for partner in partners_info_list:
                print(f"Пробуем получить баланс веба {partner['partner_id']}")
                partner_url = f"https://api-lead-magnet.affise.com/3.0/admin/partner/{partner['partner_id']}"
                headers = {'API-Key': AFFISE_API_KEY}
                r = requests.get(partner_url, headers=headers)
                res = r.json()
                created_at, created_time = str(res['partner']['created_at']).split(" ")
                c_year, c_month, c_day = str(created_at).split("-")
                created_at = dt.date(int(c_year), int(c_month), int(c_day))
                partner["created_at"] = str(created_at)
                partner["balance"] = res['partner']['balance']['RUB']['balance']
                partner["status"] = res['partner']['status']
                print(f"Успешно получили балланс веба {partner['partner_id']}")
                print(f"Пробуем получить биллинги для веба {partner['partner_id']}")
                today = str(dt.date.today())
                payments_url = f"https://api-lead-magnet.affise.com/3.1/payments?date_from={partner['created_at']}&date_to={today}&aid[]={partner['partner_id']}"
                r = requests.get(payments_url, headers=headers)
                payments_res = r.json()
                print(f"Успешно получили биллинги для веба {partner['partner_id']}")
                payments_list = []
                if len(payments_res['payments']) > 0:
                    for payment in payments_res['payments']:
                        payment_date, payment_time = str(payment['posted_date']).split(" ")
                        p_year, p_month, p_day = str(payment_date).split("-")
                        payment_date = dt.date(int(p_year), int(p_month), int(p_day))
                        payment_info = {"payment_id": payment['id'], "payment_date": str(payment_date), "payment_rev": round(float(payment['revenue']))}
                        payments_list.append(payment_info)
                    payments_list.reverse()
                    first_payment_date = payments_list[0]['payment_date']
                    last_payment_date = payments_list[-1]['payment_date']
                else:
                    first_payment_date = "None"
                    last_payment_date = "None"

                partner['payments'] = {'payments_count': len(payments_list), "first_payment_date": first_payment_date,
                                       'last_payment_date': last_payment_date, 'payments_list': payments_list}



                partners_list.append(partner)
            return partners_list

        except Exception as err:
            log.msg.error("Получили ошибку", err, traceback.print_exc())
            log.msg.info("Спим минуту и повторяем попытку")
            time.sleep(60)
            continue



def sheets_add_update_partners(partners_list: list):
    service = update_google_creds()
    log.msg.info(f"Пробуем добавить обновленных вебов в гугл таблицу")
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "обновление статусов!A2:AO",
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


def update_segmentation(updated_partners_list):
    x_segment_sources_lm = ["ВК", "ТГ", "Яндекс", "SEO", "ASO", "Youtube", "Google", "Ютуб", "Telegram"]
    a_segment_sources_lm = ["Email", "ВК", "ТГ", "Яндекс"]
    b_segment_sources_lm = ["Email", "ВК", "ТГ", "Яндекс", "Авито"]
    c_segment_black_list_offers = ["Тизерная/баннерная реклама", "FB", "Instagram", "Pinterest", "Доски объявлений (Авито, Юла и т.д.)", "Tik-Tok"]
    for partner in updated_partners_list:

        if "Новичок (только знакомлюсь)" in partner['exp_years'] or "Меньше года" in partner['exp_years']:
            db.set_segmentation(partner['partner_id'], "D")
            continue
        if "1 год" in partner['exp_years'] and "Сам" in partner['solo_or_team']:
            db.set_segmentation(partner['partner_id'], "C")
            continue
        if "1 год" in partner['exp_years'] or "2 года" in partner['exp_years']:
            if "Инфобизнес" in partner['verticals']:
                for source in str(partner['sources_lm']).split(","):
                    if source in c_segment_black_list_offers:
                        db.set_segmentation(partner['partner_id'], "B")
                        continue
                else:
                    db.set_segmentation(partner['partner_id'], "A")
                    continue
            for source in str(partner['sources_lm']).split(","):
                if source in x_segment_sources_lm:
                    db.set_segmentation(partner['partner_id'], "X")
                    continue
                elif "1 год" in partner['exp_years'] or "2 года" in partner['exp_years']:
                    db.set_segmentation(partner['partner_id'], "B")
                    continue
                else:
                    db.set_segmentation(partner['partner_id'], "A")
                    continue

def main():
    log.msg.info('Пробуем получить список вебов из гугл-таблицы')
    partners_sheets_tuple = sheets_get_partners()
    log.msg.info('Успешно получили список вебов из гугл-таблицы')
    partners_for_sheets_list = []
    partners_list_from_db = db.get_partners_by_id(partners_sheets_tuple)
    log.msg.info('Пробуем получить инфо по вебам от аффайз')
    updated_partners_list = affise_get_update_data(partners_list_from_db)
    db.update_partner_status(updated_partners_list)
    update_segmentation(updated_partners_list)
    for partner in updated_partners_list:
        partners_for_sheets_list.append(db.get_update_partner_for_sheets(partner['partner_id']))
    sheets_add_update_partners(partners_for_sheets_list)
    partners_for_crm = db.get_partners_by_id(partners_sheets_tuple)
    for partner in partners_for_crm:
        if partner['crm_partner_id'] == 0:
            crm.crm_deal_add(partner, crm.stage_new)
            continue
        if "banned" in partner['status']:
           crm.crm_deal_update(partner, crm.stage_froder)
           continue
        elif partner['fifth_payment'] > 0 and partner['fifth_payment'] != partner['last_payment']:
            crm.crm_deal_update(partner, crm.stage_active_partner)
            continue
        elif partner['fifth_payment'] > 0 and partner['fifth_payment'] == partner['last_payment']:
            crm.crm_deal_update(partner, crm.stage_fifth_payment)
            continue
        elif partner['fourth_payment'] > 0 and partner['fifth_payment'] == 0:
            crm.crm_deal_update(partner, crm.stage_fourth_payment)
            continue
        elif partner['third_payment'] > 0 and partner['fourth_payment'] == 0:
            crm.crm_deal_update(partner, crm.stage_third_payment)
            continue
        elif partner['second_payment'] > 0 and partner['third_payment'] == 0:
            crm.crm_deal_update(partner, crm.stage_second_payment)
            continue
        elif partner['first_payment'] > 0 and partner['second_payment'] == 0:
            crm.crm_deal_update(partner, crm.stage_first_payment)
            continue
        elif partner['balance'] >= 4000 and partner['balance'] < 5000:
            crm.crm_deal_update(partner, crm.stage_ballance_4000)
            continue
        elif partner['balance'] >= 3000 and partner['balance'] < 4000:
            crm.crm_deal_update(partner, crm.stage_ballance_3000)
            continue
        elif partner['balance'] >= 2000 and partner['balance'] < 3000:
            crm.crm_deal_update(partner, crm.stage_ballance_2000)
            continue
        elif partner['balance'] >= 1000 and partner['balance'] < 2000:
            crm.crm_deal_update(partner, crm.stage_ballance_1000)
            continue
        elif partner['balance'] > 0 and partner['balance'] < 1000:
            crm.crm_deal_update(partner, crm.stage_first_traffic)
            continue
        elif "True" in partner['connect_offers']:
            crm.crm_deal_update(partner, crm.stage_connect_offers)
            continue
        elif "True" in partner['hello_answer']:
            crm.crm_deal_update(partner, crm.stage_hello_answer)
            continue
        else:
            crm.crm_deal_update(partner, crm.stage_new)
            continue



if __name__ == '__main__':
    try:
        main()
    except Exception:
        log.msg.error(f"Поймали исключение ", str(traceback.print_exc()))




