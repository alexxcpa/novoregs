from database import db, hello_bot_db as tg_db
import requests
import datetime as dt
import traceback
import time
from logs import logger as log
from crm import crm
import random
import affise.lib as affise
from sheets import sheets
from weekly_reports import weekly_reports

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"
# SAMPLE_SPREADSHEET_ID = "1X5Op6GMDDrSUbpw-LhTwQsdt3xLDyKV4CUyCPkXWpP4"

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'


def random_time_sleep():
    time_secs = [1, 2, 3, 4, 5]
    random_time = random.choice(time_secs)
    if random_time == 1:
        text = 'cекунду'
    elif random_time == 2 or random_time == 3 or random_time == 4:
        text = 'cекунды'
    else:
        text = 'cекунд'
    log.msg.info(f'Спим {random_time} {text}')
    time.sleep(random_time)


def affise_get_update_data(partners_info_list):
    black_list = [
        619,
        856,
        1067,
        1495,
        2425,
        2546,
        3286,
        3441,
        3456,
        4730,
        5290,
        5308,
        6481]
    for partner in partners_info_list:
        for attempt in range(5):
            try:
                if partner['partner_id'] in black_list:
                    log.msg.info(f" Попытка {attempt}.  Партнер  {partner['partner_id']} находится в блек листе, пропускаем")
                    break
                log.msg.info(f"Попытка {attempt}. Пробуем получить анкету и баланс веба {partner['partner_id']}")
                update_partner_url = f"https://api-lead-magnet.affise.com/3.0/admin/partner/{partner['partner_id']}"
                headers = {'API-Key': AFFISE_API_KEY}
                update_partner_info = requests.get(update_partner_url, headers=headers)
                update_partner_info_res = update_partner_info.json()
                log.msg.info(f"Попытка {attempt}. Успешно получили анкету и баланс веба {partner['partner_id']}")
                created_at, created_time = str(update_partner_info_res['partner']['created_at']).split(" ")
                partner_info = {'partner_id': update_partner_info_res['partner']['id'],
                                'status': update_partner_info_res['partner']['status'], 'balance': update_partner_info_res['partner']['balance']['RUB']['balance'],
                                'ref_partner': update_partner_info_res['partner']['ref']}

                form_fields_list = []
                partner_info['phone'] = 'None'
                partner_info['exp_years'] = 'None'
                partner_info['solo_or_team'] = 'None'
                partner_info['verticals'] = "None"
                partner_info['sources_lm'] = "None"
                partner_info['thematics'] = "None"
                partner_info['about_us'] = 'None'
                for fields in update_partner_info_res['partner']['customFields']:
                    if type(fields['label']) is dict:
                        form_fields_list.append(
                            {'field_id': fields['id'], 'label': ", ".join(list(fields['label'].values()))})
                    else:
                        form_fields_list.append({'field_id': fields['id'], 'label': fields['label']})
                for field in form_fields_list:
                    if field['field_id'] == 5:
                        partner_info['phone'] = field['label']
                    if field['field_id'] == 1:
                        if "https://t.me/" in field['label']:
                            partner_info['telegram'] = field['label']
                        elif "https://t.me/" not in field['label']:
                            try:
                                partner_info['telegram'] = int(field['label'])
                            except ValueError:
                                tg_value = "https://t.me/" + str(field['label']).strip('@')
                                partner_info['telegram'] = tg_value
                    elif field['field_id'] == 16:
                        partner_info['exp_years'] = field['label']
                    elif field['field_id'] == 18:
                        partner_info['solo_or_team'] = field['label']
                    elif field['field_id'] == 20:  # multiple types
                        partner_info['verticals'] = field['label']
                    elif field['field_id'] == 22:  # multiple types
                        partner_info['sources_lm'] = field['label']
                    elif field['field_id'] == 23:  # multiple types
                        partner_info['thematics'] = field['label']
                    elif field['field_id'] == 25:
                        partner_info['about_us'] = field['label']

                db.update_partner(partner['partner_id'], 'balance', partner_info['balance'])
                db.update_partner(partner['partner_id'], 'status', partner_info['status'])
                db.update_partner(partner['partner_id'], 'exp_years', partner_info['exp_years'])
                db.update_partner(partner['partner_id'], 'solo_or_team', partner_info['solo_or_team'])
                db.update_partner(partner['partner_id'], 'verticals', partner_info['verticals'])
                db.update_partner(partner['partner_id'], 'sources_lm', partner_info['sources_lm'])
                db.update_partner(partner['partner_id'], 'thematics', partner_info['thematics'])
                db.update_partner(partner['partner_id'], 'about_us', partner_info['about_us'])

                if tg_db.validation_by_partner_id(partner['partner_id']):
                    db.update_partner(partner['partner_id'], 'send_hello', 'True')

                log.msg.info(f"Попытка {attempt}. Пробуем получить биллинги для веба {partner['partner_id']}")
                today = str(dt.date.today())
                payments_url = f"https://api-lead-magnet.affise.com/3.1/payments?date_from={partner['created_at']}&date_to={today}&aid[]={partner['partner_id']}"
                payments_r = requests.get(payments_url, headers=headers)
                payments_res = payments_r.json()
                log.msg.info(f"Попытка {attempt}. Успешно получили биллинги для веба {partner['partner_id']}")


                if len(payments_res['payments']) > 0:
                    payments_list = []
                    for payment in payments_res['payments']:
                        payment_date, payment_time = str(payment['posted_date']).split(" ")
                        p_year, p_month, p_day = str(payment_date).split("-")
                        payment_date = dt.date(int(p_year), int(p_month), int(p_day))
                        payment_info = {"payment_id": payment['id'], "payment_date": str(payment_date), "payment_rev": round(float(payment['revenue']))}
                        payments_list.append(payment_info)
                    payments_list.reverse()
                    db.update_partner_payments(partner['partner_id'], payments_list)
                    first_payment_date = payments_list[0]['payment_date']
                    last_payment_date = payments_list[-1]['payment_date']
                    db.update_partner(partner['partner_id'], "first_payment_date", first_payment_date)
                    db.update_partner(partner['partner_id'], "last_payment_date", last_payment_date)

                    """ ----------- расчет цикла сделки, количество дней со дня последней выплаты--------------------- """

                    deal_cycle = dt.datetime.strptime(first_payment_date, '%Y-%m-%d') - dt.datetime.strptime(str(created_at), '%Y-%m-%d')
                    from_last_payment_days = dt.datetime.today() - dt.datetime.strptime(last_payment_date, '%Y-%m-%d')
                    db.update_partner(partner['partner_id'], "deal_cycle", deal_cycle.days)
                    db.update_partner(partner['partner_id'], "from_last_payment_days", from_last_payment_days.days)

                    """ ----------- расчет рои для первой выплаты--------------------- """

                    log.msg.info(f"Попытка {attempt}. Пробуем получить ОРБ для веба {partner['partner_id']} для первой выплаты")
                    first_payment_charge_url = f"https://api-lead-magnet.affise.com/3.0/stats/getbypartner?filter[date_from]={partner['created_at']}&filter[date_to]={first_payment_date}&filter[partner]={partner['partner_id']}"
                    first_payment_charge_r = requests.get(first_payment_charge_url, headers=headers)
                    log.msg.info(f"Попытка {attempt}. Успешно получили ОРБ для веба {partner['partner_id']} для первой выплаты")
                    first_payment_charge_url_res = first_payment_charge_r.json()
                    first_payment_charge = first_payment_charge_url_res['stats'][0]['actions']['confirmed']['charge']


                    log.msg.info(f"Попытка {attempt}. Пробуем получить продажи для веба {partner['partner_id']} для первой выплаты")
                    first_payment_sales_url = f"https://api-lead-magnet.affise.com/3.0/stats/conversions?date_from={partner['created_at']}&date_to={first_payment_date}&partner[]={partner['partner_id']}&goal=5"
                    first_payment_sales_r = requests.get(first_payment_sales_url, headers=headers)
                    log.msg.info(f"Попытка {attempt}. Успешно получили продажи для веба {partner['partner_id']} для первой выплаты")
                    first_payment_sales_url_res = first_payment_sales_r.json()

                    if len(first_payment_sales_url_res['conversions']) > 0:
                        sales_list = []
                        sales_affprices_list = []
                        for goal in first_payment_sales_url_res['conversions']:
                            sale = {'offer_id': goal['offer_id'],
                                    'affprice': goal['sum']}
                            sales_affprices_list.append(int(goal['sum']))
                            sales_list.append(sale)
                        sales_sum = sum(sales_affprices_list)
                        first_payment_roi = int(round(sales_sum/first_payment_charge * 100))
                        db.update_partner(partner['partner_id'], "first_payment_roi", first_payment_roi)

                    """ ----------- расчет общего рои --------------------- """

                    common_roi = affise.get_common_roi(attempt, partner['created_at'], partner['partner_id'])

                    db.update_partner(partner['partner_id'], "common_roi", common_roi)
                break


            except Exception as ex:
                log.msg.error(f"Попытка {attempt}. Поймали исключение {traceback.format_exc()}")
                log.msg.info("Спим и повторяем попытку")
                time.sleep(1)
                continue


def update_segmentation_test(updated_partners_list):
    for partner in updated_partners_list:
        if partner['last_payment_date'] == 'None' or partner['last_payment_date'] == 0:
            set_onboarding_segmentation(partner)
        else:
            set_payment_segmentation(partner)

def set_onboarding_segmentation(partner):
    x_segment_sources_lm = ["вк", "тг", "яндекс.директ", "seo", "aso", "youtube", "google", "ютуб", "telegram", "вконтакте",
                            "рся", "я.директ"]
    a_segment_sources_lm = ["email", "email-рассылки", "telegram", "вк", "тг", "яндекс", "вконтакте", "рся",
                            "тг(свои каналы)", "тг(закуп постов)",
                            'вк (свой паблики)', 'вк(закуп постов)', "яндекс.директ", "я.директ"]

    b_segment_exp_years_list = ['2 года', '3 года', '4 года', '5 лет и более']
    c_segment_exp_years_list = ['1 год']
    if partner['segment_payment'] != 'None':
        db.set_payment_segment(partner['partner_id'], 'None')
    if str("в команде") in str(partner['solo_or_team']).lower():
        if str("инфобизнес") in str(partner['verticals']).lower():
            for source in str(partner['sources_lm']).lower().split(","):
                if source in a_segment_sources_lm:
                    db.set_onboarding_segment(partner['partner_id'], "A")
                else:
                    db.set_onboarding_segment(partner['partner_id'], "B")
        else:
            for source in str(partner['sources_lm']).lower().split(","):
                if source in x_segment_sources_lm:
                    db.set_onboarding_segment(partner['partner_id'], "X")
                else:
                    db.set_onboarding_segment(partner['partner_id'], "A")
    elif str("инфобизнес") in str(partner['verticals']).lower().split(","):
        for source in str(partner['sources_lm']).lower().split(","):
            if source in a_segment_sources_lm:
                db.set_onboarding_segment(partner['partner_id'], "A")
            else:
                db.set_onboarding_segment(partner['partner_id'], "B")

    elif len(partner['verticals'].lower().split(",")) > 2:
        for source in str(partner['sources_lm']).lower().split(","):
            if source in a_segment_sources_lm:
                db.set_onboarding_segment(partner['partner_id'], "A")
            else:
                db.set_onboarding_segment(partner['partner_id'], "B")
    elif partner['exp_years'] in b_segment_exp_years_list:
        db.set_onboarding_segment(partner['partner_id'], "B")
    elif partner['exp_years'] in c_segment_exp_years_list:
        db.set_onboarding_segment(partner['partner_id'], "C")
    else:
        db.set_onboarding_segment(partner['partner_id'], "D")



def set_payment_segmentation(partner):
    set_onboarding_segmentation(partner)
    if str("В команде").lower() in str(partner['solo_or_team']).lower():
        if int(partner['first_payment_roi']) >= 150:
            if int(partner['deal_cycle']) <= 30:
                db.set_payment_segment(partner['partner_id'], "X")
            else:
                db.set_payment_segment(partner['partner_id'], "A")
        elif 100 <= int(partner['first_payment_roi']) <= 150:
            if int(partner['deal_cycle']) <= 21:
                db.set_payment_segment(partner['partner_id'], "A")
            else:
                db.set_payment_segment(partner['partner_id'], "B")
        elif 0 <= int(partner['first_payment_roi']) <= 100:
            if int(partner['deal_cycle']) <= 30:
                db.set_payment_segment(partner['partner_id'], "B")
            else:
                db.set_payment_segment(partner['partner_id'], "C")

    elif int(partner['first_payment_roi']) >= 150:
        if int(partner['deal_cycle']) <= 21:
            db.set_payment_segment(partner['partner_id'], "A")
        else:
            db.set_payment_segment(partner['partner_id'], "B")
    elif 100 <= int(partner['first_payment_roi']) <= 150:
        if partner['deal_cycle'] <= 30:
            db.set_payment_segment(partner['partner_id'], "B")
        else:
            db.set_payment_segment(partner['partner_id'], "C")
    elif 0 <= int(partner['first_payment_roi']) <= 100:
        if int(partner['deal_cycle']) <= 60:
            db.set_payment_segment(partner['partner_id'], "C")
        else:
            db.set_payment_segment(partner['partner_id'], "D")

def update_crm(partners_for_crm):
    for partner in partners_for_crm:
        for attempt in range(5):
            try:
                if "banned" in partner['status']:
                    crm.crm_deal_update(partner, crm.stage_froder)
                    time.sleep(0.5)
                    break
                if partner['from_last_payment_days'] >= 60:
                    crm.crm_deal_update(partner, crm.stage_sleep_partner)
                    time.sleep(0.5)
                    break
                if partner['last_payment_date'] != 0:
                    if partner['fifth_payment'] > 0 and partner['fifth_payment'] != partner['last_payment']:
                        crm.crm_deal_update(partner, crm.stage_active_partner)
                        time.sleep(0.5)
                        break
                    elif partner['fifth_payment'] > 0 and partner['fifth_payment'] == partner['last_payment']:
                        crm.crm_deal_update(partner, crm.stage_fifth_payment)
                        time.sleep(0.5)
                        break
                    elif partner['fourth_payment'] > 0 and partner['fifth_payment'] == 0:
                        crm.crm_deal_update(partner, crm.stage_fourth_payment)
                        time.sleep(0.5)
                        break
                    elif partner['third_payment'] > 0 and partner['fourth_payment'] == 0:
                        crm.crm_deal_update(partner, crm.stage_third_payment)
                        time.sleep(0.5)
                        break
                    elif partner['second_payment'] > 0 and partner['third_payment'] == 0:
                        crm.crm_deal_update(partner, crm.stage_second_payment)
                        time.sleep(0.5)
                        break
                    elif partner['first_payment'] > 0 and partner['second_payment'] == 0:
                        crm.crm_deal_update(partner, crm.stage_first_payment)
                        time.sleep(0.5)
                        break

                if partner['balance'] >= 4000 and partner['balance'] < 5000:
                    crm.crm_deal_update(partner, crm.stage_ballance_4000)
                    time.sleep(0.5)
                    break
                elif partner['balance'] >= 3000 and partner['balance'] < 4000:
                    crm.crm_deal_update(partner, crm.stage_ballance_3000)
                    time.sleep(0.5)
                    break
                elif partner['balance'] >= 2000 and partner['balance'] < 3000:
                    crm.crm_deal_update(partner, crm.stage_ballance_2000)
                    time.sleep(0.5)
                    break
                elif partner['balance'] >= 1000 and partner['balance'] < 2000:
                    crm.crm_deal_update(partner, crm.stage_ballance_1000)
                    time.sleep(0.5)
                    break
                elif partner['balance'] > 0 and partner['balance'] < 1000:
                    crm.crm_deal_update(partner, crm.stage_first_traffic)
                    time.sleep(0.5)
                    break
                elif "True" in partner['connect_offers']:
                    crm.crm_deal_update(partner, crm.stage_connect_offers)
                    time.sleep(0.5)
                    break
                elif "True" in partner['hello_answer']:
                    crm.crm_deal_update(partner, crm.stage_hello_answer)
                    time.sleep(0.5)
                    break
                else:
                    crm.crm_deal_update(partner, crm.stage_new)
                    time.sleep(0.5)
                    break
            except Exception as err:
                log.msg.error(f"Попытка {attempt} Получили ошибку при обновлении crm {err}. Поймали исключение {traceback.format_exc()}")
                log.msg.info('Спим 1 минуту и повторяем попытку')
                time.sleep(1)
                continue

def update_partners_status():
    log.msg.info('Пробуем получить список вебов для обновления')
    partners_for_update = db.get_partners_for_update()
    log.msg.info('Успешно получили список вебов для обновления')
    partners_list_from_db = db.get_partners_by_id(partners_for_update)
    affise_get_update_data(partners_list_from_db)
    updated_partners_list = db.get_partners_by_id(partners_for_update)
    update_segmentation_test(updated_partners_list)
    partners_for_sheets_list = []
    for partner in updated_partners_list:
        partners_for_sheets_list.append(db.get_update_partner_for_sheets(partner['partner_id']))
    sheets.add_update_partners(partners_for_sheets_list)
    partners_for_crm = db.get_partners_by_id(partners_for_update)
    update_crm(partners_for_crm)


if __name__ == '__main__':
    while True:
        try:
            # update_partners_status()
            weekly_reports.weekly_reports()
            log.msg.info('Спим час и повторяем попытку')
            time.sleep(3600)
        except Exception as ex:
            log.msg.error(f"Поймали исключение {ex}", )
            continue

