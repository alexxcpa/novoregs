import logging


def init_logger(name):
    logger = logging.getLogger(name)  # из пакета logging получаем логгер и даем ему какое то имя.
    FORMAT = '%(asctime)s :: %(name)s :: %(funcName)s:%(lineno)s :: %(levelname)s :: %(message)s'  # Это те данные, которые мы хотим выводить в наш лог.
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename="../manualy/logs.log") # пишем наши логи в лог файл
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)


init_logger('update_status_new')

msg = logging.getLogger('update_status_new')

