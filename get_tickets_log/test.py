import os.path
import requests
import datetime as dt
import pandas as pd
import time
import telebot

# user api data for support tg_account
# TG_APP_API_ID = 23290491
# TG_APP_API_HASH = '50178fc36db4006742b7fbe2f44bae5d'

TG_BOT_TOKEN = '6444085476:AAESgETTwFsi_HPRuXzUpxok6AqXAPFXg0s'
API_ID_ACC_1 = 23290491

CHAT_ID = '1457459092'

bot = telebot.TeleBot(TG_BOT_TOKEN)



TG_BOT_TOKEN = '6444085476:AAESgETTwFsi_HPRuXzUpxok6AqXAPFXg0s'


def send_message_tg(mess):
    try:
        r = requests.get(
            f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mess}&parse_mode=markdown')
        return True if r.status_code == 200 else False
    except:
        return False



