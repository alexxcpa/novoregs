import sqlite3

DATABASE_PATH = '../database/novoreg.db'

def get_partners_id():
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    db_res = cur.execute("SELECT partner_id FROM crm_main").fetchall()
    res = tuple(i[0] for i in db_res)
    db.commit()
    db.close()

    return res

def add_new_partner(partner: dict):
    created_at = partner['created_at']
    partner_id = partner['partner_id']
    target = "True"
    if partner['ref_partner'] is None:
        ref_partner = 0
    else:
        ref_partner = partner['ref_partner']
    if 'phone' in partner:
        phone = partner['phone']
    else:
        phone = 'None'
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"""INSERT INTO crm_main (partner_id, target, created_at, ref_partner, email, phone, telegram, 
        balance, exp_years, solo_or_team, verticals, thematics, sources_lm, 
        about_us, status)
                                    VALUES ('{partner_id}', '{target}', '{created_at}', '{ref_partner}', 
                                    '{partner['email']}', '{phone}', '{partner['telegram']}',  
                                    '{partner['balance']}', '{partner['exp_years']}', '{partner['solo_or_team']}',
                                    '{partner['verticals']}', '{partner['thematics']}', '{partner['sources_lm']}',
                                    '{partner['about_us']}', '{partner['status']}') """)
    db.commit()
    db.close()
    return True


def get_partners_by_id(partners_sheets_tuple: tuple):
    partners_info_list = []
    for partner_id in partners_sheets_tuple:
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        db_res = cur.execute(f""" SELECT * FROM crm_main WHERE partner_id = '{partner_id}' """).fetchall()
        db.commit()
        db.close()
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
            partner_info['connect_offers'] = i[16]
            partner_info['segment_onboarding'] = i[17]
            partner_info['segment_payment'] = i[18]
            partner_info['balance'] = i[19]
            partner_info['first_payment'] = i[20]
            partner_info['second_payment'] = i[21]
            partner_info['third_payment'] = i[22]
            partner_info['fourth_payment'] = i[23]
            partner_info['fifth_payment'] = i[24]
            partner_info['last_payment'] = i[25]
            partner_info['first_payment_roi'] = i[26]
            partner_info['common_roi'] = i[27]
            partner_info['first_payment_date'] = i[28]
            partner_info['last_payment_date'] = i[29]
            partner_info['deal_cycle'] = i[30]
            partner_info['from_last_payment_days'] = i[31]
            partner_info['status'] = i[32]
            partner_info['froder'] = i[33]
            partner_info['exp_years'] = i[34]
            partner_info['solo_or_team'] = i[35]
            partner_info['verticals'] = i[36]
            partner_info['thematics'] = i[37]
            partner_info['sources_exp'] = i[38]
            partner_info['sources_lm'] = i[39]
            partner_info['sources_type'] = i[40]
            partner_info['about_us'] = i[41]
            partner_info['crm_stage'] = i[42]
            partners_info_list.append(partner_info)
    return partners_info_list


def add_crm_partner_id(crm_partner_id, partner_id):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"UPDATE crm_main SET crm_partner_id = '{crm_partner_id}' WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True


def get_partners_for_hello():  # берем партнеров из базы, кому нужно отправить привет
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    db_res = cur.execute(
        """ SELECT partner_id, telegram, sources_lm FROM crm_main WHERE send_hello = 'None' and target = 'True' """).fetchall()  # and status = 'good_chat'
    db.commit()
    db.close()
    partners_info_list = []
    for i in db_res:
        partner_info = {}
        partner_info['id'] = i[0]
        tg_link1 = 'https://t.me/'
        if tg_link1 in str(i[1]).lower():
            tg = str(i[1]).split('https://t.me/')
            partner_info['telegram'] = tg[1]
        else:
            partner_info['telegram'] = i[1]
        partner_info['sources_lm'] = i[2]
        partners_info_list.append(partner_info)
        continue
    return partners_info_list


def add_good_hello_status(partner_id: int):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"UPDATE crm_main SET send_hello = 'True' WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True


def add_bad_hello_status(text_status: str, partner_id: int):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"UPDATE crm_main SET send_hello_error = '{text_status}', send_hello = 'False'"
                f"WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True


"""-------------update_partners_status----------------------"""


def update_partner(partner_id: int, column: str, value):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"UPDATE crm_main SET {column} = '{value}' WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True


def update_partner_payments(partner_id, payments_list):
    first_payment = 0
    second_payment = 0
    third_payment = 0
    fourth_payment = 0
    fifth_payment = 0
    last_payment = 0
    if len(payments_list) >= 5:
        first_payment = payments_list[0]['payment_rev']
        second_payment = payments_list[1]['payment_rev']
        third_payment = payments_list[2]['payment_rev']
        fourth_payment = payments_list[3]['payment_rev']
        fifth_payment = payments_list[4]['payment_rev']
        last_payment = payments_list[-1]['payment_rev']
    elif len(payments_list) == 4:
        first_payment = payments_list[0]['payment_rev']
        second_payment = payments_list[1]['payment_rev']
        third_payment = payments_list[2]['payment_rev']
        fourth_payment = payments_list[3]['payment_rev']
        last_payment = payments_list[-1]['payment_rev']

    elif len(payments_list) == 3:
        first_payment = payments_list[0]['payment_rev']
        second_payment = payments_list[1]['payment_rev']
        third_payment = payments_list[2]['payment_rev']
        last_payment = payments_list[-1]['payment_rev']

    elif len(payments_list) == 2:
        first_payment = payments_list[0]['payment_rev']
        second_payment = payments_list[1]['payment_rev']
        last_payment = payments_list[-1]['payment_rev']

    elif len(payments_list) == 1:
        first_payment = payments_list[0]['payment_rev']
        last_payment = payments_list[-1]['payment_rev']

    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f""" UPDATE crm_main SET first_payment = "{first_payment}",  second_payment = "{second_payment}", 
                third_payment = "{third_payment}", fourth_payment = "{fourth_payment}", fifth_payment = "{fifth_payment}", last_payment = "{last_payment}"
                WHERE partner_id = "{partner_id}" 
                """)
    db.commit()
    db.close()
    print(f'Успешно обновили выплаты в базе для партнера {partner_id}')
    return True

def set_payment_segment(partner_id, segment):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f""" UPDATE crm_main SET segment_payment = '{segment}' WHERE partner_id = '{partner_id}' """)
    db.commit()
    db.close()

def set_onboarding_segment(partner_id, segment):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f""" UPDATE crm_main SET segment_onboarding = '{segment}' WHERE partner_id = '{partner_id}' """)
    db.commit()
    db.close()

def get_partners_for_update():
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    db_res = cur.execute(f"SELECT partner_id FROM crm_main WHERE crm_partner_id != 0").fetchall()
    res = tuple(i[0] for i in db_res)
    db.commit()
    db.close()
    return res

def get_update_partner_for_sheets(partner_id: int):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    db_res = cur.execute(f""" SELECT * FROM crm_main WHERE partner_id = '{partner_id}' """).fetchone()
    db.commit()
    db.close()
    if db_res is not None:
        target = "Да"
        name = db_res[5]
        vk = db_res[9]
        skype = db_res[10]
        if db_res[3] != "True":
            target = "Нет"
        if db_res[5] == "None":
            name = ""
        if db_res[8] == "None":
            phone = ""
        else:
            phone = str(db_res[8]).strip("+")
        if db_res[9] == "None":
            vk = ""
        if db_res[10] == "None":
            skype = ""
        if db_res[12] == "None":
            send_hello_error = ""
        else:
            send_hello_error = db_res[12]
        if db_res[13] == "True":
            send_hello = "Да"
        else:
            send_hello = "Нет"
        if db_res[14] == "True":
            hello_answer = "Да"
        else:
            hello_answer = "Нет"
        if db_res[15] == "True":
            form = "Да"
        else:
            form = "Нет"
        if db_res[16] == "True":
            connect_offers = "Да"
        else:
            connect_offers = "Нет"

        partner_info = {"partner_id": db_res[2], "target": target, "created_at": db_res[4], "name": name,
                        "ref_partner": db_res[6], "email": db_res[7], "phone": phone, "vk": vk, "skype": skype,
                        "telegram": db_res[11], "send_hello_error":  send_hello_error, "send_hello": send_hello,
                        "hello_answer": hello_answer, "form": form, "connect_offers": connect_offers,
                        "segment_onboarding": db_res[17], "segment_payment": db_res[18], "balance": db_res[19],
                        "first_payment": db_res[20], "second_payment": db_res[21], "third_payment": db_res[22],
                        "fourth_payment": db_res[23], "fifth_payment": db_res[24], "last_payment": db_res[25],
                        "first_payment_roi": db_res[26], "common_roi": db_res[27], "first_payment_date": db_res[28],
                        "last_payment_date": db_res[29], "deal_cycle": db_res[30], "from_last_payment_days": db_res[31],
                        "status": db_res[32], "froder": db_res[33], "exp_years": db_res[34], "solo_or_team": db_res[35],
                        "verticals": db_res[36], "thematics": db_res[37], "sources_exp": db_res[38], "sources_lm": db_res[39],
                        "sources_type": db_res[40], "about_us": db_res[41], "crm_stage": db_res[42]}
        return partner_info
    else:
        return None


def set_novoreg_status(partner_id: int, column: str, status: str):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"UPDATE crm_main SET {column} = '{status}' WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True

def get_novoreg_status(partner_id: int, column: str):
    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    res = cur.execute(f"""SELECT {column} from crm_main WHERE partner_id = '{partner_id}'""").fetchone()
    res = res[0]
    db.commit()
    db.close()
    return res
