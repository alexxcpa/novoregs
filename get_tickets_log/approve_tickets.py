import requests
import time

import logger as log

from database import db, hello_bot_db

from tg_methods import send_msg_tg_bot_partner, send_msg_tg_bot_manager

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'
# OFFER_BLACK_LIST = [686, 1233, 1486, 848, 1299, 1370, 1421, 1527, 1586, 1553, 1460, 1658, 1760, 1761, 1762]

# OFFER_BLACK_LIST = [1683, 1682, 1681, 1680, 1679, 1678, 1677, 1845, 1735, 1278, 1074, 1071, 1780, 1702, 1598, 1597, 1584,
#               1900, 1899, 1782, 1725, 1755, 1586, 1553, 1460, 1233, 1876, 1348, 1347, 1346, 1345, 1344, 1343, 1211,
#               1858, 1736, 1874, 1873, 1872, 1722, 1721, 1686, 1685, 1684, 1643, 1599, 1569, 1342, 1329, 1324, 1229,
#                 1832, 1692, 1636, 1884, 1842, 1799, 1772, 1890, 1824, 1844, 1826, 1813, 1796, 1786, 1785, 1720, 1719,
#             1717, 1449, 1307, 1225, 1116, 999, 927, 926, 925, 885, 871, 1790, 1789, 1458, 1313, 1311, 1299, 1298, 958,
#             778, 528, 489, 429, 1655, 1647, 1567, 1867, 1837, 1729, 1745, 1508, 1063]


OFFER_BLACK_LIST = [1949,1939,1929,1928,1845,1914,1735,1278,1911,1815,1814,1368,1367,1319,1755,1460,1233,1790,1789,1458,1299,1298,958,
        778,1884,1842,1799,1772,1832,1692,1636,1890,1655,1647,1567, 1683,1682,1681,1680,1679,1678,1677,1900,1899,1782,1725,
        1809,1808,1807,1806,1805,1804,1803,1766,1765,1644]



FROD_MSG = """
🚯Обращаем внимание, что у нас проводится глубокая проверка на фрод и мотивированный трафик.

Также отметим, что для оценки качества трафика рекламодатель требует, чтобы от партнера было не менее 50 конверсий на 1 оффер. 
Если будет по несколько конверсий на 5-10 офферов, рекламодатель может попросить отключить партнера от оффера.😞 Мы хотим, чтобы каждому партнеру было с нами комфортно работать, 
поэтому призываем соблюдать эти простые правила.

Надеемся на понимание и плодотворное сотрудничество😉"""

ABOUT_LIMIT ='\n' + """
[Подробнее про лимит в 100 конверсий](https://docs.google.com/d, ment/d/1FqOnKFEzHI7SvmyVSloW78ehxLy6MctDqFpminFCUHo/edit?usp=sharing) """

ABOUT_DELAY = '\n' + """
После подключения офферы появятся в разделе "Доступные" в течение 2-3 минут."""

def tg_send_info(ticket, good_connect_offers_list, black_list_offers_list, frod_msg: bool):
    msg_title = f"Партнеру {ticket['partner']} подключили офферы:"
    black_list_msg = '🛑 Следующие офферы временно не доступны для подключения новым вебмастерам. Для уточнения деталей обратись к личному менеджеру' '\n \n👉' + '\n \n👉'.join(black_list_offers_list)
    good_connect_offers_msg = '\n \n👉' + '\n \n👉'.join(good_connect_offers_list) + '\n \n' + 'На каждый оффер стартовый лимит 100 конверсий'

    if frod_msg is True:
        frod_msg = f"\n{FROD_MSG}"
    else:
        frod_msg = ""

    if len(good_connect_offers_list) > 0 and len(black_list_offers_list) > 0:
        offers_msg = msg_title + good_connect_offers_msg + frod_msg + ABOUT_LIMIT + ABOUT_DELAY + '\n'+'\n' + black_list_msg
    elif len(good_connect_offers_list) > 0 and len(black_list_offers_list) == 0:
        offers_msg = msg_title + good_connect_offers_msg + frod_msg + ABOUT_LIMIT + ABOUT_DELAY
    elif len(good_connect_offers_list) == 0 and len(black_list_offers_list) > 0:
        offers_msg = black_list_msg


    send_msg_tg_bot_manager(offers_msg)

    if hello_bot_db.validation_by_partner_id(int(ticket['partner'])):
        chat_id = hello_bot_db.get_chat_id_by_partner(int(ticket['partner']))
        send_msg_tg_bot_partner(offers_msg, chat_id)


def approve_tickets(ticket_list):
    if ticket_list is None:
        log.msg.info(f'Нет доступных тикетов')
        return None
    try:
        for ticket in ticket_list:
            time.sleep(1)
            log.msg.info(f"Партнер {ticket['partner']} Пробуем подключить офферы")
            good_connect_offers_list = []
            black_list_offers_list = []
            # if len(ticket['offers_list']) > 10:
            #     log.msg.info(f"Слишком большое количество офферов за раз. Пропускаем веба {ticket['partner']}")
            #     continue
            for offer in ticket['offers_list']:
                if offer['offer_id'] in OFFER_BLACK_LIST:
                    if db.check_black_list_ticket(offer['ticket_id']):
                        continue
                    else:
                        log.msg.info(f"Партнер {ticket['partner']} : Тикет {offer['ticket_id']} : Оффер {offer['offer_id']} на данный момент находится в блек листе")
                        db.add_black_list_ticket(int(offer['ticket_id']), int(ticket['partner']), int(offer['offer_id']), str(offer['offer_title']))
                        black_list_offers_list.append(f"[{offer['offer_title'].replace('[', '(').replace(']', ')')}](https://my.leadmagnet.ru/show/{offer['offer_id']})")
                        continue
                log.msg.info(f"Партнер {ticket['partner']}: Пробуем подключить оффер {offer['offer_id']} в тикете {offer['ticket_id']}" )
                params = {'do': 'approve'}
                url = f"https://api-lead-magnet.affise.com/3.0/admin/ticket/{offer['ticket_id']}/offer"
                headers = {'API-Key': AFFISE_API_KEY}
                r = requests.post(url, headers=headers, data=params)
                res = r.json()
                if res['status'] == 1:
                    good_connect_offers_list.append(f"[{offer['offer_title'].replace('[', '(').replace(']', ')')}](https://my.leadmagnet.ru/show/{offer['offer_id']})")
                    log.msg.info(f"Партнер {ticket['partner']}: Успешно подключили оффер {offer['offer_id']}")

            # log.msg.info(f"Пробуем запросить статус подлкючения офферов у партнера {ticket['partner']}")

            db_partners_list = db.get_partners_id()
            if len(good_connect_offers_list) > 0:
                if ticket['partner'] in db_partners_list:
                    novoreg_status = db.get_novoreg_status(ticket['partner'], 'connect_offers')
                    if novoreg_status == 'None':
                        db.set_novoreg_status(ticket['partner'], 'connect_offers', 'True')
                        tg_send_info(ticket, good_connect_offers_list, black_list_offers_list,  frod_msg=True)
                    else:
                        tg_send_info(ticket, good_connect_offers_list, black_list_offers_list, frod_msg=False)
                else:
                    tg_send_info(ticket, good_connect_offers_list, black_list_offers_list, frod_msg=False)


    except Exception as err:
        log.msg.error(f'Получили ошибку: {err}')
