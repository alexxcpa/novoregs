from telegram.tg_auth_acc_1 import tg_auth_acc_1 as tg_1
from telegram.tg_auth_acc_2 import tg_auth_acc_2 as tg_2
from database import db
import time


def add_to_contacts():
    for partner in db.get_partners_for_hello():
            tg_1.add_to_contact_acc_1(partner['telegram'], partner['id'], partner['sources_lm'])
            time.sleep(5)
            tg_2.add_to_contact_acc_2(partner['telegram'], partner['id'], partner['sources_lm'])
            time.sleep(5)
            db.add_good_hello_status(partner['id'])






