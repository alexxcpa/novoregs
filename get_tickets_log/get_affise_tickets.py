import os.path
import requests
import datetime as dt
import pandas as pd
import time
import telebot

import logger as log

# user api data for support tg_account
# TG_APP_API_ID = 23290491
# TG_APP_API_HASH = '50178fc36db4006742b7fbe2f44bae5d'

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'


def get_affise_tickets():
    # manager_list = ['5fcf594293079980c967281a', '6059a302c3c1c3e3b2466d63']
    manager_list = ['6059a302c3c1c3e3b2466d63']
    ak_manager_list = ['6059a302c3c1c3e3b2466d63']
    today = str(dt.date.today())
    yesterday = str(dt.date.today() - dt.timedelta(days=1))
    # today = "2024-02-07"
    # yesterday = "2024-02-06"

    test_partners = [24894, 28572, 28736]


    res = None
    affise_tickets_list = []
    partners_set = set([])
    connect_tickets_list = []
    for _ in range(5):
        try:
            url = f'https://api-lead-magnet.affise.com/3.0/admin/tickets?status=open&page=1'
            headers = {'API-Key': AFFISE_API_KEY}
            log.msg.info(f"Запрос тикетов в аффайз")
            r = requests.get(url, headers=headers)
            res = r.json()
            if res['status'] == 1:
                log.msg.info(f"Успешно получили тикеты в аффайз")
                time.sleep(1)
                break
            elif res['status'] == 2:
                log.msg.info(f"Получили ошибку: {res['message']} Спим 1 минуту и повторяем попытку")
                time.sleep(60)
                continue
        except Exception as http_error:
            # print(f'Не смогли получить тикеты от affise. {http_error} ')
            log.msg.error(f'Не смогли получить тикеты от affise. {http_error} ')
            log.msg.error(f'Спим минуту и повторяем попытку')
            time.sleep(60)
            continue

    for ticket in res['tickets']:
        try:
            if ticket['type'] == 'offer_request' and str(ticket['partner']['manager']['id']) in manager_list:
                if today in ticket['created'] or yesterday in ticket['created']:
                        # if ticket['partner']['id'] in test_partners:
                        ticket_info = {'id': ticket['id'],
                                        'partner': ticket['partner']['id'],
                                        'offer': ticket['offer']['id'],
                                        'date': ticket['created'],
                                        'title': str(ticket['title']).strip('Connect offer')
                                    }
                        affise_tickets_list.append(ticket_info)
                        partners_set.add(ticket['partner']['id'])
            else:
                # log.msg.error(f'Нет подходящих тикетов')
                continue

        except Exception as err:
            log.msg.error(f'{err}')
            # print(err)
            continue

    for partner in partners_set:
        offers_list = []
        offer_connect_info = {'partner': partner}
        for ticket in affise_tickets_list:
            if ticket['partner'] == partner:
                offer = {'ticket_id': ticket['id'], 'offer_id': ticket['offer'], 'offer_title': ticket['title']}
                offers_list.append(offer)
                offer_connect_info['offers_list'] = offers_list
        connect_tickets_list.append(offer_connect_info)

    if len(connect_tickets_list) == 0:
        return None
    else:
        log.msg.info(f'Успешно сформировали список тикетов для подключения')

        # for i in connect_tickets_list:
        #     print(i)
        # print(len(connect_tickets_list))
        return connect_tickets_list


