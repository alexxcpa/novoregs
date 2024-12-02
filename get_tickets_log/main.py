from get_affise_tickets import get_affise_tickets
import time

import logger as log

from approve_tickets import approve_tickets

if __name__ == '__main__':
    script_name = "get_tickets_log"
    version = "1.0"
    while True:
        approve_tickets(get_affise_tickets())
        log.msg.info(f'Спим 5 минут и повторяем попытку')
        time.sleep(300)



