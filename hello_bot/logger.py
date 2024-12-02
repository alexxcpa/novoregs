import logging


def init_logger(name):
    logger = logging.getLogger(name)  # из пакета logging получаем логгер и даем ему какое то имя.
    FORMAT = '%(asctime)s :: %(name)s :: %(funcName)s:%(lineno)s :: %(levelname)s :: %(message)s'  # Это те данные, которые мы хотим выводить в наш лог.
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename="logs/logs.log") # пишем наши логи в лог файл
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)



# init_logger(f'{script_name}')
init_logger('hello_bot')

msg = logging.getLogger('hello_bot')

