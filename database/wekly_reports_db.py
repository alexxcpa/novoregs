import sqlite3
import requests
import datetime as dt


DATABASE_PATH = '../database/novoreg.db'


def create_new_table():
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(""" CREATE TABLE crm_main (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crm_partner_id integer DEFAULT 0,
        partner_id integer DEFAULT 0,
        target text DEFAULT True,
        created_at date,
        name text DEFAULT None,
        ref_partner integer DEFAULT 0,
        email text DEFAULT None,
        phone integer DEFAULT 0,
        vk text DEFAULT None,
        skype text DEFAULT None,
        telegram text DEFAULT None,
        send_hello_error text DEFAULT None,
        send_hello text DEFAULT None,
        hello_answer text DEFAULT None,
        form text DEFAULT None,
        connect_offers text DEFAULT None,
        segment_onboarding text DEFAULT None,
        segment_payment text DEFAULT None,
        balance integer DEFAULT 0,
        first_payment integer DEFAULT 0,
        second_payment integer DEFAULT 0,
        third_payment integer DEFAULT 0,
        fourth_payment integer DEFAULT 0,
        fifth_payment integer DEFAULT 0,
        last_payment integer DEFAULT 0,
        first_payment_roi integer DEFAULT 0,
        common_roi integer DEFAULT 0,
        first_payment_date date DEFAULT 0,
        last_payment_date date DEFAULT 0,
        deal_cycle integer DEFAULT 0,
        from_last_payment_days integer DEFAULT 0,
        status test DEFAULT None,
        froder text DEFAULT None,
        exp_years text DEFAULT None,
        solo_or_team text DEFAULT None,
        verticals text DEFAULT None,
        thematics text DEFAULT None,
        sources_exp text DEFAULT None,
        sources_lm text DEFAULT None,
        sources_type text DEFAULT None,
        about_us text DEFAULT None,
        crm_stage text DEFAULT None,
        google_sheets text DEFAULT None) 
        """)
    db.commit()
    db.close()

def add_new_partner_crm_main(partner: dict):
    google_sheets = 'True'

    if partner['target'] == "Нет":
        target = 'False'
    else:
        target = 'True'

    if partner['name'] == '':
        name = None
    else:
        name = partner['name']

    if partner['send_hello_error'] == '':
        send_hello_error = None
    else:
        send_hello_error = partner['send_hello_error']

    if partner['phone'] == '':
        phone = None
    else:
        phone = partner['phone']

    if partner['vk'] == '':
        vk = None
    else:
        vk = partner['vk']

    if partner['skype'] == '':
        skype = None
    else:
        skype = partner['skype']

    if partner['send_hello'] == 'Нет':
        send_hello = 'False'
    else:
        send_hello = 'True'

    if partner['hello_answer'] == 'Нет':
        hello_answer = 'None'
    else:
        hello_answer = 'True'

    if partner['form'] == 'Нет':
        form = 'None'
    else:
        form = 'True'

    if partner['connect_offers'] == 'Нет':
        connect_offers = 'None'
    else:
        connect_offers = 'True'


    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"""INSERT INTO crm_main (partner_id, target, created_at, name, ref_partner, email, phone, vk, skype, telegram, 
        send_hello_error, send_hello, hello_answer, form, connect_offers, segment_onboarding, segment_payment, balance, first_payment, 
        second_payment, third_payment, fourth_payment, fifth_payment, last_payment, first_payment_roi, common_roi, first_payment_date,
        last_payment_date, deal_cycle, from_last_payment_days, status, froder, exp_years, solo_or_team, verticals, thematics, 
        sources_exp, sources_lm, sources_type, about_us, crm_stage, google_sheets)
                                    VALUES ('{partner['partner_id']}', '{target}', '{partner['created_at']}', '{name}', '{partner['ref_partner']}', 
                                    '{partner['email']}', '{phone}',  '{vk}', '{skype}', '{partner['telegram']}', '{send_hello_error}', 
                                    '{send_hello}', '{hello_answer}', '{form}', '{connect_offers}', 
                                    '{partner['segment_onboarding']}', '{partner['segment_payment']}', '{partner['balance']}', '{partner['first_payment']}',
                                    '{partner['second_payment']}', '{partner['third_payment']}', '{partner['fourth_payment']}', '{partner['fifth_payment']}',
                                    '{partner['last_payment']}', '{partner['first_payment_roi']}', '{partner['common_roi']}', '{partner['first_payment_date']}', 
                                    '{partner['last_payment_date']}', '{partner['deal_cycle']}', '{partner['from_last_payment_days']}', '{partner['status']}', 
                                    '{partner['froder']}', '{partner['exp_years']}', '{partner['solo_or_team']}',
                                    '{partner['verticals']}', '{partner['thematics']}', '{partner['sources_exp']}', '{partner['sources_lm']}', '{partner['sources_type']}',
                                    '{partner['about_us']}', '{partner['crm_stage']}', '{google_sheets}') """)
    db.commit()
    db.close()
    return True

def add_new_partner(partner: dict):

    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"""INSERT INTO crm_main (partner_id, target, created_at, name, ref_partner, email, phone, vk, skype, telegram, 
        send_hello_error, send_hello, hello_answer, form, connect_offers, exp_years, solo_or_team, verticals, thematics, 
        sources_exp, sources_lm, sources_type, about_us, google_sheets)
                                    VALUES ('{partner['partner_id']}', '{partner['target']}', '{partner['created_at']}', '{partner['name']}', 
                                    '{partner['ref_partner']}', '{partner['email']}', '{partner['phone']}', '{partner['vk']}',  
                                    '{partner['skype']}', '{partner['telegram']}',  '{partner['send_hello_error']}', '{partner['send_hello']}', 
                                    '{partner['hello_answer']}', '{partner['form']}',  '{partner['connect_offers']}', '{partner['exp_years']}', '{partner['solo_or_team']}',
                                    '{partner['verticals']}', '{partner['thematics']}','{partner['sources_exp']}','{partner['sources_lm']}',
                                    '{partner['sources_type']}', '{partner['about_us']}', '{partner['google_sheets']}') """)
    db.commit()
    db.close()
    return True

def create_table_hello_bot():
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(""" CREATE TABLE tg_hello_bot_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATE,
    chat_id integer not null, 
    username text not null,
    first_name text not null,
    last_name text not null
    )
    """)
    db.commit()
    db.close()

def transfer_partners_crm_main(partner: dict):
    crm_partner_id = partner['crm_partner_id']
    partner_id = partner['partner_id']
    target = partner['target']
    created_at = partner['created_at']
    name = partner['name']
    ref_partner = partner['ref_partner']
    email = partner['email']
    phone = partner['phone']
    vk = partner['vk']
    skype = partner['skype']
    telegram = partner['telegram']
    send_hello_error = partner['send_hello_error']
    send_hello = partner['send_hello']
    hello_answer = partner['hello_answer']
    form = partner['form']
    connect_offers = partner['connect_offers']
    segment_onboarding = partner['segment_onboarding']
    segment_payment = partner['segment_payment']
    balance = partner['balance']
    first_payment = partner['first_payment_amount']
    second_payment = partner['second_payment_amount']
    third_payment = partner['third_payment_amount']
    last_payment = partner['last_payment_amount']
    first_payment_roi = partner['first_payment_roi']
    common_roi = partner['common_roi']
    froder = partner['froder']
    status = partner['status']
    exp_years = partner['exp_years']
    solo_or_team = partner['solo_or_team']
    verticals = partner['verticals']
    thematics = partner['thematics']
    sources_exp = partner['sources_exp']
    sources_lm = partner['sources_lm']
    sources_type = partner['sources_type']
    about_us = partner['about_us']
    google_sheets = partner['google_sheets']

    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"""INSERT INTO crm_main (crm_partner_id, partner_id, target, created_at, name, ref_partner, email, phone, vk,
    skype, telegram, send_hello_error, send_hello, hello_answer, form, connect_offers, segment_onboarding, segment_payment,
        balance, first_payment, second_payment, third_payment, last_payment, first_payment_roi, common_roi, status, froder, 
        exp_years, solo_or_team, verticals, thematics, sources_exp, sources_lm, sources_type, about_us, google_sheets)
                                    VALUES ('{crm_partner_id}', '{partner_id}', '{target}', '{created_at}', '{name}', 
                                    '{ref_partner}','{email}', '{phone}', '{vk}', '{skype}', '{telegram}', '{send_hello_error}', 
                                    '{send_hello}', '{hello_answer}', '{form}', '{connect_offers}','{segment_onboarding}',
                                    '{segment_payment}', '{balance}', '{first_payment}', '{second_payment}', '{third_payment}', 
                                    '{last_payment}', '{first_payment_roi}', '{common_roi}', '{status}', '{froder}', '{exp_years}', '{solo_or_team}',
                                    '{verticals}', '{thematics}', '{sources_exp}', '{sources_lm}', '{sources_type}', '{about_us}',  
                                    '{google_sheets}')""")

    db.commit()
    db.close()
    return True

def get_all_partners_crm():
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    db_res = cur.execute(f"SELECT * FROM crm").fetchall()
    partners_info_list = []
    for i in db_res:
        partner_info = {}
        partner_info['crm_partner_id'] = i[1]
        partner_info['partner_id'] = i[2]
        partner_info['target'] = i[3]
        partner_info['created_at'] = i[4]
        partner_info['name'] = i[5]
        partner_info['ref_partner'] = i[6]
        partner_info['email'] = i[7]
        partner_info['phone'] = i[8]
        partner_info['vk'] = i[9]
        partner_info['skype'] = i[10]
        partner_info['telegram'] = i[11]
        partner_info['send_hello_error'] = i[12]
        partner_info['send_hello'] = i[13]
        partner_info['hello_answer'] = i[14]
        partner_info['form'] = i[15]
        partner_info['second_hello'] = i[16]
        partner_info['third_hello'] = i[17]
        partner_info['connect_offers'] = i[18]
        partner_info['first_traffic'] = i[19]
        partner_info['segment_onboarding'] = i[20]
        partner_info['segment_payment'] = i[21]
        partner_info['balance'] = i[22]
        partner_info['first_payment'] = i[23]
        partner_info['experience'] = i[24]
        partner_info['exp_years'] = i[25]
        partner_info['solo_or_team'] = i[26]
        partner_info['verticals'] = i[27]
        partner_info['thematics'] = i[28]
        partner_info['sources_exp'] = i[29]
        partner_info['sources_lm'] = i[30]
        partner_info['sources_type'] = i[31]
        partner_info['about_us'] = i[32]
        partner_info['crm_stage'] = i[33]
        partner_info['first_payment_amount'] = i[34]
        partner_info['second_payment_amount'] = i[35]
        partner_info['third_payment_amount'] = i[36]
        partner_info['last_payment_amount'] = i[37]
        partner_info['first_payment_roi'] = i[38]
        partner_info['second_payment_roi'] = i[39]
        partner_info['common_roi'] = i[40]
        partner_info['froder'] = i[41]
        partner_info['status'] = i[42]
        partner_info['google_sheets'] = i[43]
        partners_info_list.append(partner_info)
    db.commit()
    db.close()
    return partners_info_list

def get_partners_for_crm_2024():
    date = dt.datetime(2024, 1, 1)
    date_and = dt.datetime(2024, 1, 31)
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    db_res = cur.execute(
        f"""SELECT partner_id, target, created_at, name, ref_partner, email, phone, vk, skype, telegram, send_hello_error,
        send_hello, hello_answer, form, second_hello, third_hello, connect_offers, first_traffic,
        segment_onboarding, segment_payment, balance, first_payment, experience, exp_years, solo_or_team,
        verticals, thematics, sources_exp, sources_lm, sources_type, about_us, crm_stage, first_payment_amount,
        second_payment_amount, third_payment_amount, last_payment_amount, first_payment_roi, second_payment_roi,
        common_roi, froder, status, crm_partner_id FROM crm WHERE crm_partner_id != 0""").fetchall()
    partners_info_list = []
    for i in db_res:
        partner_info = {}
        partner_info['partner_id'] = i[0]
        partner_info['target'] = i[1]
        partner_info['created_at'] = i[2]
        partner_info['name'] = i[3]
        partner_info['ref_partner'] = i[4]
        partner_info['email'] = i[5]
        partner_info['phone'] = i[6]
        partner_info['vk'] = i[7]
        partner_info['skype'] = i[8]
        partner_info['telegram'] = i[9]
        partner_info['send_hello_error'] = i[10]
        partner_info['send_hello'] = i[11]
        partner_info['hello_answer'] = i[12]
        partner_info['form'] = i[13]
        partner_info['second_hello'] = i[14]
        partner_info['third_hello'] = i[15]
        partner_info['connect_offers'] = i[16]
        partner_info['first_traffic'] = i[17]
        partner_info['segment_onboarding'] = i[18]
        partner_info['segment_payment'] = i[19]
        partner_info['balance'] = i[20]
        partner_info['first_payment'] = i[21]
        partner_info['experience'] = i[22]
        partner_info['exp_years'] = i[23]
        partner_info['solo_or_team'] = i[24]
        partner_info['verticals'] = i[25]
        partner_info['thematics'] = i[26]
        partner_info['sources_exp'] = i[27]
        partner_info['sources_lm'] = i[28]
        partner_info['sources_type'] = i[29]
        partner_info['about_us'] = i[30]
        partner_info['crm_stage'] = i[31]
        partner_info['first_payment_amount'] = i[32]
        partner_info['second_payment_amount'] = i[33]
        partner_info['third_payment_amount'] = i[34]
        partner_info['last_payment_amount'] = i[35]
        partner_info['first_payment_roi'] = i[36]
        partner_info['second_payment_roi'] = i[37]
        partner_info['common_roi'] = i[38]
        partner_info['froder'] = i[39]
        partner_info['status'] = i[40]
        partner_info['crm_partner_id'] = i[41]
        created_at = dt.datetime.strptime(i[2], '%Y-%m-%d')
        if created_at >= date:
            partners_info_list.append(partner_info)
    db.commit()
    db.close()
    return partners_info_list


def get_weekly_reports():
    january_1 = {'month': 'Январь', 'date_from': dt.date(2024, 1, 1), 'date_to': dt.date(2024, 1, 7)}
    january_2 = {'month': 'Январь', 'date_from': dt.date(2024, 1, 8), 'date_to': dt.date(2024, 1, 14)}
    january_3 = {'month': 'Январь', 'date_from': dt.date(2024, 1, 15), 'date_to': dt.date(2024, 1, 21)}
    january_4 = {'month': 'Январь', 'date_from': dt.date(2024, 1, 22), 'date_to': dt.date(2024, 1, 28)}

    february_1 = {'month': 'Февраль', 'date_from': dt.date(2024, 1, 29), 'date_to': dt.date(2024, 2, 4)}
    february_2 = {'month': 'Февраль', 'date_from': dt.date(2024, 2, 5), 'date_to': dt.date(2024, 2, 11)}
    february_3 = {'month': 'Февраль', 'date_from': dt.date(2024, 2, 12), 'date_to': dt.date(2024, 2, 18)}
    february_4 = {'month': 'Февраль', 'date_from': dt.date(2024, 2, 19), 'date_to': dt.date(2024, 2, 25)}

    march_1 = {'month': 'Март', 'date_from': dt.date(2024, 2, 26), 'date_to': dt.date(2024, 3, 3)}
    march_2 = {'month': 'Март', 'date_from': dt.date(2024, 3, 4), 'date_to': dt.date(2024, 3, 10)}
    march_3 = {'month': 'Март', 'date_from': dt.date(2024, 3, 11), 'date_to': dt.date(2024, 3, 17)}
    march_4 = {'month': 'Март', 'date_from': dt.date(2024, 3, 18), 'date_to': dt.date(2024, 3, 24)}
    march_5 = {'month': 'Март', 'date_from': dt.date(2024, 3, 25), 'date_to': dt.date(2024, 3, 31)}

    april_1 = {'month': 'Апрель', 'date_from': dt.date(2024, 4, 1), 'date_to': dt.date(2024, 4, 7)}
    april_2 = {'month': 'Апрель', 'date_from': dt.date(2024, 4, 8), 'date_to': dt.date(2024, 4, 14)}
    april_3 = {'month': 'Апрель', 'date_from': dt.date(2024, 4, 15), 'date_to': dt.date(2024, 4, 21)}
    april_4 = {'month': 'Апрель', 'date_from': dt.date(2024, 4, 22), 'date_to': dt.date(2024, 4, 28)}

    may_1 = {'month': 'Май', 'date_from': dt.date(2024, 4, 29), 'date_to': dt.date(2024, 5, 5)}
    may_2 = {'month': 'Май', 'date_from': dt.date(2024, 5, 6), 'date_to': dt.date(2024, 5, 12)}
    may_3 = {'month': 'Май', 'date_from': dt.date(2024, 5, 13), 'date_to': dt.date(2024, 5, 19)}
    may_4 = {'month': 'Май', 'date_from': dt.date(2024, 5, 20), 'date_to': dt.date(2024, 5, 26)}

    june_1 = {'month': 'Июнь', 'date_from': dt.date(2024, 5, 27), 'date_to': dt.date(2024, 6, 2)}
    june_2 = {'month': 'Июнь', 'date_from': dt.date(2024, 6, 3), 'date_to': dt.date(2024, 6, 9)}
    june_3 = {'month': 'Июнь', 'date_from': dt.date(2024, 6, 10), 'date_to': dt.date(2024, 6, 16)}
    june_4 = {'month': 'Июнь', 'date_from': dt.date(2024, 6, 17), 'date_to': dt.date(2024, 6, 23)}
    june_5 = {'month': 'Июнь', 'date_from': dt.date(2024, 6, 24), 'date_to': dt.date(2024, 6, 30)}

    july_1 = {'month': 'Июль', 'date_from': dt.date(2024, 7, 1), 'date_to': dt.date(2024, 7, 7)}
    july_2 = {'month': 'Июль', 'date_from': dt.date(2024, 7, 8), 'date_to': dt.date(2024, 7, 14)}
    july_3 = {'month': 'Июль', 'date_from': dt.date(2024, 7, 15), 'date_to': dt.date(2024, 7, 21)}
    july_4 = {'month': 'Июль', 'date_from': dt.date(2024, 7, 22), 'date_to': dt.date(2024, 7, 28)}

    august_1 = {'month': 'Август', 'date_from': dt.date(2024, 7, 29), 'date_to': dt.date(2024, 8, 4)}
    august_2 = {'month': 'Август', 'date_from': dt.date(2024, 8, 5), 'date_to': dt.date(2024, 8, 11)}
    august_3 = {'month': 'Август', 'date_from': dt.date(2024, 8, 12), 'date_to': dt.date(2024, 8, 18)}
    august_4 = {'month': 'Август', 'date_from': dt.date(2024, 8, 19), 'date_to': dt.date(2024, 8, 25)}

    september_1 = {'month': 'Сентябрь', 'date_from': dt.date(2024, 8, 26), 'date_to': dt.date(2024, 9, 1)}
    september_2 = {'month': 'Сентябрь', 'date_from': dt.date(2024, 9, 2), 'date_to': dt.date(2024, 9, 8)}
    september_3 = {'month': 'Сентябрь', 'date_from': dt.date(2024, 9, 9), 'date_to': dt.date(2024, 9, 15)}
    september_4 = {'month': 'Сентябрь', 'date_from': dt.date(2024, 9, 16), 'date_to': dt.date(2024, 9, 22)}
    september_5 = {'month': 'Сентябрь', 'date_from': dt.date(2024, 9, 23), 'date_to': dt.date(2024, 9, 29)}

    october_1 = {'month': 'Октябрь', 'date_from': dt.date(2024, 9, 30), 'date_to': dt.date(2024, 10, 6)}
    october_2 = {'month': 'Октябрь', 'date_from': dt.date(2024, 10, 7), 'date_to': dt.date(2024, 10, 13)}
    october_3 = {'month': 'Октябрь', 'date_from': dt.date(2024, 10, 14), 'date_to': dt.date(2024, 10, 20)}
    october_4 = {'month': 'Октябрь', 'date_from': dt.date(2024, 10, 21), 'date_to': dt.date(2024, 10, 27)}

    november_1 = {'month': 'Ноябрь', 'date_from': dt.date(2024, 10, 28), 'date_to': dt.date(2024, 11, 3)}
    november_2 = {'month': 'Ноябрь', 'date_from': dt.date(2024, 11, 4), 'date_to': dt.date(2024, 11, 10)}
    november_3 = {'month': 'Ноябрь', 'date_from': dt.date(2024, 11, 11), 'date_to': dt.date(2024, 11, 17)}
    november_4 = {'month': 'Ноябрь', 'date_from': dt.date(2024, 11, 18), 'date_to': dt.date(2024, 11, 24)}

    december_1 = {'month': 'Декабрь', 'date_from': dt.date(2024, 11, 25), 'date_to': dt.date(2024, 12, 1)}
    december_2 = {'month': 'Декабрь', 'date_from': dt.date(2024, 12, 2), 'date_to': dt.date(2024, 12, 8)}
    december_3 = {'month': 'Декабрь', 'date_from': dt.date(2024, 12, 9), 'date_to': dt.date(2024, 12, 15)}
    december_4 = {'month': 'Декабрь', 'date_from': dt.date(2024, 12, 16), 'date_to': dt.date(2024, 12, 22)}
    december_5 = {'month': 'Декабрь', 'date_from': dt.date(2024, 12, 23), 'date_to': dt.date(2024, 12, 29)}


    weeks_list = [january_1, january_2, january_3, january_4,
                  february_1, february_2, february_3, february_4,
                  march_1, march_2, march_3, march_4, march_5,
                  april_1, april_2, april_3, april_4,
                  may_1, may_2, may_3, may_4,
                  june_1, june_2, june_3, june_4, june_5,
                  july_1, july_2, july_3, july_4,
                  august_1, august_2, august_3, august_4,
                  september_1, september_2, september_3,
                  september_4, september_5, october_1, october_2, october_3, october_4,
                  november_1, november_2, november_3, november_4,
                  december_1, december_2, december_3, december_4, december_5]

    # delta = dt.timedelta(7)
    # print((date_to - date_from).days)

    # for i in range(4):
    #     date_from = date_from + delta
    #     date_to = date_to + delta
    #     print(date_from, date_to)
    weekly_res_list = []
    for week in weeks_list:
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        partners_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' """).fetchall()
        partners = tuple(i[0] for i in partners_res)
        target_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND target = 'True' """).fetchall()
        target = tuple(i[0] for i in target_res)
        send_hello_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND send_hello = 'True' """).fetchall()
        send_hello = tuple(i[0] for i in send_hello_res)
        connect_offers_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND connect_offers = 'True' """).fetchall()
        connect_offers = tuple(i[0] for i in connect_offers_res)
        first_traffic_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND balance > 0 """).fetchall()
        first_traffic = tuple(i[0] for i in first_traffic_res)
        first_payment_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND first_payment > 0 AND status = 'active' """).fetchall()
        first_payment = tuple(i[0] for i in first_payment_res)
        balance_1000_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND balance >= 1000 AND balance < 2000  """).fetchall()
        balance_1000 = tuple(i[0] for i in balance_1000_res)
        balance_2000_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND balance >= 2000 AND balance < 3000  """).fetchall()
        balance_2000 = tuple(i[0] for i in balance_2000_res)
        balance_3000_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND balance >= 3000 AND balance < 4000  """).fetchall()
        balance_3000 = tuple(i[0] for i in balance_3000_res)
        balance_4000_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE created_at >= '{week['date_from']}' AND created_at <= '{week['date_to']}' AND balance >= 4000 AND balance < 5000  """).fetchall()
        balance_4000 = tuple(i[0] for i in balance_4000_res)

        db.commit()
        db.close()

        week_res = {'period': f"{week['month']} \n {str(week['date_from'])}-{str(week['date_to'])}", 'partners': len(partners),
                    'target': len(target), 'send_hello': len(send_hello), 'connect_offers': len(connect_offers),'first_traffic': len(first_traffic), 'first_payment': len(first_payment),
                    'balance_1000': len(balance_1000), 'balance_2000': len(balance_2000), 'balance_3000': len(balance_3000), 'balance_4000': len(balance_4000), }

        weekly_res_list.append(week_res)
    return weekly_res_list


def update_crm_partner_id(partner: dict):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    db_res = cur.execute(f"UPDATE crm_main SET crm_partner_id = '{partner['crm_partner_id']}' WHERE partner_id ='{partner['partner_id']}' ").fetchall()
    db.commit()
    db.close()


