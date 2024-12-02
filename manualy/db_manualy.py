import sqlite3
import requests
import datetime as dt


def update_partner_status(updated_partners_list: list):
    for partner in updated_partners_list:
        target = "True"
        if partner['target'] == 'Нет':
            target = 'False'

        hello_answer = 'False'
        if partner['hello_answer'] == 'Да':
            hello_answer = 'True'

        db = sqlite3.connect('../database/novoreg.db')
        cur = db.cursor()
        cur.execute(f""" UPDATE crm_main SET target = '{target}', hello_answer = '{hello_answer}'
                    WHERE partner_id = '{partner['partner_id']}' """)
        db.commit()
        db.close()
        print('Успешно обновили статусы в базе')
    return True

def update_dvv_partners_status(updated_partners_list: list):
    for partner in updated_partners_list:
        name = partner['name']
        if partner['name'] == '':
            name = 'None'

        phone = partner['phone']
        if partner['phone'] == '':
            phone = 'None'

        telegram = partner['telegram']
        if partner['telegram'] == '':
            telegram = 'None'

        vk = partner['vk']
        if partner['vk'] == '':
            vk = 'None'

        # thematics = partner['thematics']
        # if partner['thematics'] == '':
        #     thematics = 'None'

        sources_lm = partner['sources_lm']
        if partner['sources_lm'] == '':
            sources_lm = 'None'

        # common_roi = partner['common_roi']
        # if partner['common_roi'] == '':
        #     common_roi = 'None'

        db = sqlite3.connect('../database/novoreg.db')
        cur = db.cursor()
        cur.execute(f""" UPDATE crm_main SET name = '{name}', 
                    phone = '{phone}', 
                    telegram = '{telegram}', 
                    vk = '{vk}', 
                    sources_lm = '{sources_lm}'
                    WHERE partner_id = '{partner['partner_id']}' """)
        db.commit()
        db.close()
        print('Успешно обновили статусы в базе')
    return True




def set_segmentation(partner_id, segment: str):
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    cur.execute(f""" UPDATE crm_main SET segment_onboarding = '{segment}' WHERE partner_id = '{partner_id}' """)
    db.commit()
    db.close()


def get_crm_update_partners():
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    db_res = cur.execute(f"SELECT crm_partner_id, name FROM crm_main WHERE crm_partner_id != 0").fetchall()
    res = tuple((i[0], i[1]) for i in db_res)
    db.commit()
    db.close()
    return res


def add_crm_partner_id(crm_partner_id, partner_id):
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    cur.execute(f"UPDATE crm_main SET crm_partner_id = '{crm_partner_id}' WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True

def get_partners_by_id(partners_sheets_list: list):
    partners_info_list = []
    for partner in partners_sheets_list:
        db = sqlite3.connect('../database/novoreg.db')
        cur = db.cursor()
        db_res = cur.execute(f""" SELECT * FROM crm_main WHERE partner_id = '{partner['partner_id']}' """).fetchall()
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

def get_update_partner_for_sheets(partner_id: int):
    db = sqlite3.connect('../database/novoreg.db')
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




