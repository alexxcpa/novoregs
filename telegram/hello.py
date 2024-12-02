from telegram.tg_auth_acc_1 import tg_auth_acc_1 as tg_1
from telegram.tg_auth_acc_2 import tg_auth_acc_2 as tg_2
from database import db
import time
from telegram.messages import acc1_hello_msg_1, acc2_hello_msg_1, partner_id_msg, welcome_msg
from logs import logger as log

def hello_sendler():
    for partner in db.get_partners_for_hello():
        tg_1_res = tg_1.hello_sendler_acc_1(partner['telegram'], partner['id'], f"{welcome_msg} {partner_id_msg} {partner['id']} {acc1_hello_msg_1}")
        if tg_1_res is True:
            db.add_good_hello_status(partner['id'])
            tg_1.add_to_contact_acc_1(partner['telegram'], partner['id'], partner['sources_lm'])
            time.sleep(60)
            continue
        elif tg_1_res == "[400 USERNAME_INVALID]" or tg_1_res == "[400 USERNAME_NOT_OCCUPIED]":
            tg_1.add_to_contact_acc_1(partner['telegram'], partner['id'], partner['sources_lm'])
            db.add_bad_hello_status("Невалидный тг", partner['id'])
        elif tg_1_res == "[403 CHAT_WRITE_FORBIDDEN]":
            db.add_bad_hello_status("Указан канал или группа", partner['id'])
            continue
        elif tg_1_res is False:
            db.add_bad_hello_status("Не смогли отправить привет в тг", partner['id'])
            continue
        elif tg_1_res == "[400 PEER_FLOOD]":
            tg_1.add_to_contact_acc_1(partner['telegram'], partner['id'], partner['sources_lm'])
            tg_2_res = tg_2.hello_sendler_acc_2(partner['telegram'], partner['id'], f"{welcome_msg} {partner_id_msg} {partner['id']} {acc2_hello_msg_1}")
            if tg_2_res is True:
                db.add_good_hello_status(partner['id'])
                tg_2.add_to_contact_acc_2(partner['telegram'], partner['id'], partner['sources_lm'])
                time.sleep(60)
                continue
            elif tg_2_res is False:
                db.add_bad_hello_status("Не смогли отправить привет в тг", partner['id'])
                tg_2.add_to_contact_acc_2(partner['telegram'], partner['id'], partner['sources_lm'])
                continue
            elif tg_2_res == "[400 USERNAME_NOT_OCCUPIED]" or tg_2_res == "[400 USERNAME_INVALID]":
                db.add_bad_hello_status("Невалидный тг", partner['id'])
            elif tg_2_res == "[403 CHAT_WRITE_FORBIDDEN]":
                db.add_bad_hello_status("Указан канал или группа", partner['id'])
                continue
            elif tg_2_res == "[400 PEER_FLOOD]":
                tg_2.add_to_contact_acc_2(partner['telegram'], partner['id'], partner['sources_lm'])
                log.msg.error('Не смогли отправить приветы с обоих аккаунтов. Бан на обоих')
                db.add_bad_hello_status("Бан на обоих аккаунтах", partner['id'])
                break








