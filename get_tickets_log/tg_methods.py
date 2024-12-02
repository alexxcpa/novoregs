import os.path
import requests
import datetime as dt
import pandas as pd
import time
import telebot

# user api data for support tg_account
# TG_APP_API_ID = 23290491
# TG_APP_API_HASH = '50178fc36db4006742b7fbe2f44bae5d'




# bot = telebot.TeleBot(MANAGER_BOT_TOKEN)



MANAGER_BOT_TOKEN = '6444085476:AAESgETTwFsi_HPRuXzUpxok6AqXAPFXg0s'
MANAGER_CHAT_ID = '1457459092'

HELLO_BOT_TOKEN = '6597425495:AAHmSK9oVddKxa31yGVIb3E-oxkaJoVO0xA'


def send_msg_tg_bot_manager(mess):
    try:
        r = requests.get(
            f'https://api.telegram.org/bot{MANAGER_BOT_TOKEN}/sendMessage?chat_id={MANAGER_CHAT_ID}&text={mess}&parse_mode=markdown')
        return True if r.status_code == 200 else False
    except:
        return False

def send_msg_tg_bot_partner(mess, chat_id):
    try:
        r = requests.get(
            f'https://api.telegram.org/bot{HELLO_BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={mess}&parse_mode=markdown')
        return True if r.status_code == 200 else False
    except:
        return False



