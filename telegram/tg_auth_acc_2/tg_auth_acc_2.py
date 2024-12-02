from pyrogram import Client
from logs import logger as log

# user api data for support tg_account

API_ID_ACC_2 = 23039268
API_HASH_ACC_2 = 'e6e902e8c4abe7a71f5c9565bd137b3b'

TG_BOT_TOKEN = '6444085476:AAESgETTwFsi_HPRuXzUpxok6AqXAPFXg0s'
CHAT_ID = '1457459092'

test_user = "Alexey_Patunin_LM"
test_user_2 = "investor"
test_user_id = "32707"
message = "Привет"

WORKDIR = '../telegram/tg_auth_acc_1'

def hello_sendler_acc_2(partner_user_name, partner_id, message):
    try:
        with Client('account', API_ID_ACC_2, API_HASH_ACC_2, workdir=WORKDIR) as app:
            app.send_message(partner_user_name, message)
            log.msg.info(f"Аккаунт 2 :: Партнер {partner_id} :: Успешно отправили привет партнеру. Спим 1 минуту")
        return True
    except Exception as err:
        if "[400 PEER_FLOOD]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Не смогли отправить привет. Аккаунт временно в бане.')
            return "[400 PEER_FLOOD]"
        elif "[400 USERNAME_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Не смогли отправить привет. Некорректно введено имя пользователя')
            return "[400 USERNAME_INVALID]"
        elif "[400 USERNAME_NOT_OCCUPIED]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Не смогли отправить привет. Пользователь с именем {partner_user_name} не найден')
            return "[400 USERNAME_NOT_OCCUPIED]"
        elif "[403 CHAT_WRITE_FORBIDDEN]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Не смогли отправить привет. Указан канал или группа')
            return "[403 CHAT_WRITE_FORBIDDEN]"
        elif "[400 PEER_ID_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Указан неверный номер телефона')
            return "[400 PEER_ID_INVALID]"
        log.msg.error(f"Аккаунт 2 :: Партнер {partner_id} :: Ошибка при отправке привета", err)
        return False

def add_to_contact_acc_2(partner_user_name, partner_id, partner_sources):
    try:
        with Client('account', API_ID_ACC_2, API_HASH_ACC_2, workdir=WORKDIR) as app:
            app.add_contact(partner_user_name, first_name=f"{partner_id} {partner_sources}")
            log.msg.info(f"Аккаунт 2: Успешно добавили в контакты партнера {partner_id}.")
            return True
    except Exception as err:
        if "[400 USERNAME_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 2: Не смогли добавить в контакты  {partner_id}: Некорректно введено имя пользователя')
            return "[400 USERNAME_INVALID]"
        elif "[400 USERNAME_NOT_OCCUPIED]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Не смогли добавить в контакты. Пользователь не найден')
            return "[400 USERNAME_NOT_OCCUPIED]"
        elif "[403 CHAT_WRITE_FORBIDDEN]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Не смогли добавить в контакты. Указан канал или группа')
            return "[403 CHAT_WRITE_FORBIDDEN]"
        elif "[400 PEER_ID_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 2 :: Партнер {partner_id} :: Не смогли добавить в контакты. Указан неверный номер телефона')
            return "[400 PEER_ID_INVALID]"
        log.msg.error(f"Аккаунт 2 :: Партнер {partner_id} ::Ошибка при добавлении в контакты", err)
        return False


# hello_sendler_acc_2('alexxcpa','12345', 'Привет')
# add_to_contact_acc_2(test_user_2, test_user_id)
