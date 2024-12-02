from affise import lib as affise
from crm import crm
from telegram import add_to_contact
from logs import logger as log
import time
import traceback

if __name__ == '__main__':
    while True:
        try:
            new_partners_list = affise.get_new_partners()
            # crm.crm_partners_add(new_partners_list)
            add_to_contact.add_to_contacts()
            log.msg.info('Спим 5 минут и повторяем попытку')
            time.sleep(300)
        except Exception as ex:
            log.msg.error(f"Поймали исключение {ex}, {traceback.format_exc()}")
            continue
