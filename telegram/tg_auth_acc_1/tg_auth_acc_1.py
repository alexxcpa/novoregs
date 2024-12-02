from pyrogram import Client

from logs import logger as log

# user api data for support tg_account
API_ID_ACC_1 = 23290491
API_HASH_ACC_1 = '50178fc36db4006742b7fbe2f44bae5d'

TG_BOT_TOKEN = '6444085476:AAESgETTwFsi_HPRuXzUpxok6AqXAPFXg0s'
CHAT_ID = '1457459092'


partner_id = "137963878"
test_user_id = 137963878
message = "Привет, отправили с помощью user_id из бота"

WORKDIR = '../telegram/tg_auth_acc_1'

def hello_sendler_acc_1(partner_user_name, partner_id, message):
    try:
        with Client('account', API_ID_ACC_1, API_HASH_ACC_1, workdir=WORKDIR) as app:
            app.send_message(partner_user_name, message)
            log.msg.info(f"Аккаунт 1 :: Партнер {partner_id} :: Успешно отправили привет партнеру. Спим 1 минуту")
        return True
    except Exception as err:
        if "[400 PEER_FLOOD]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли отправить привет. Аккаунт временно в бане.')
            return "[400 PEER_FLOOD]"
        elif "[400 USERNAME_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли отправить привет. Некорректно введено имя пользователя')
            return "[400 USERNAME_INVALID]"
        elif "[400 USERNAME_NOT_OCCUPIED]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли отправить привет. Пользователь с именем {partner_user_name} не найден')
            return "[400 USERNAME_NOT_OCCUPIED]"
        elif "[403 CHAT_WRITE_FORBIDDEN]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли отправить привет. Указан канал или группа')
            return "[403 CHAT_WRITE_FORBIDDEN]"
        elif "[400 PEER_ID_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Указан неверный номер телефона')
            return "[400 PEER_ID_INVALID]"

        log.msg.error(f"Аккаунт 1 :: Партнер {partner_id} :: Ошибка при отправке привета", err)
        return False

def add_to_contact_acc_1(partner_user_name, partner_id, partner_sources):
    try:
        with Client('account', API_ID_ACC_1, API_HASH_ACC_1, workdir=WORKDIR) as app:
            app.add_contact(partner_user_name, first_name=f"{partner_id} {partner_sources}")
            # app.add_contact(user_idfirst_name=partner_user_name, phone_number=str(partner_id))
            log.msg.info(f"Аккаунт 1: Успешно добавили в контакты партнера {partner_id}.")
            return True
    except Exception as err:
        if "[400 USERNAME_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 1: Не смогли добавить в контакты  {partner_id}: Некорректно введено имя пользователя')
            return "[400 USERNAME_INVALID]"
        elif "[400 USERNAME_NOT_OCCUPIED]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли добавить в контакты. Пользователь не найден')
            return "[400 USERNAME_NOT_OCCUPIED]"
        elif "[403 CHAT_WRITE_FORBIDDEN]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли добавить в контакты. Указан канал или группа')
            return "[403 CHAT_WRITE_FORBIDDEN]"
        elif "[400 PEER_ID_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли добавить в контакты. Указан неверный номер телефона')
            return "[400 PEER_ID_INVALID]"
        elif "[420 FLOOD_WAIT_X]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли добавить в контакты. Привышение лимита для контактов')
            return "[420 FLOOD_WAIT_X]"


        log.msg.error(f"Аккаунт 1 :: Партнер {partner_id} :: Ошибка при добавлении в контакты", err)
        return False

async def get_chat_history(partner_user_name, partner_id):
    try:
        with Client('account', API_ID_ACC_1, API_HASH_ACC_1, workdir="./tg_auth_acc_1") as app:
            # res = app.get_chat_history(partner_user_name)
            # app.add_contact(user_idfirst_name=partner_user_name, phone_number=str(partner_id))
            # log.msg.info(f"Аккаунт 1: Успешно получили историю партнера {partner_id}.")
            async for message in app.get_chat_history(partner_user_name):
                print(message)
            return True
    except Exception as err:
        if "[400 USERNAME_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 1: Не смогли получили историю партнера  {partner_id}: Некорректно введено имя пользователя')
            return "[400 USERNAME_INVALID]"
        elif "[400 USERNAME_NOT_OCCUPIED]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли получили историю партнера. Пользователь не найден')
            return "[400 USERNAME_NOT_OCCUPIED]"
        elif "[403 CHAT_WRITE_FORBIDDEN]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли получили историю партнера. Указан канал или группа')
            return "[403 CHAT_WRITE_FORBIDDEN]"
        elif "[400 PEER_ID_INVALID]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли получили историю партнера. Указан неверный номер телефона')
            return "[400 PEER_ID_INVALID]"
        elif "[420 FLOOD_WAIT_X]" in str(err):
            log.msg.error(f'Аккаунт 1 :: Партнер {partner_id} :: ННе смогли получили историю партнера. Привышение лимита для контактов')
            return "[420 FLOOD_WAIT_X]"



        log.msg.error(f"Аккаунт 1 :: Партнер {partner_id} :: Ошибка при запросе сообщений", err)
        return False






# hello_sendler_acc_1('alexxcpa','12345', 'Привет')

# app = Client('account', API_ID_ACC_1, API_HASH_ACC_1)

# async def main():
#     async with app:
#         # "me" refers to your own chat (Saved Messages)
#         async for message in app.get_chat_history("Dimitriy6666"):
#             log.msg.info(message)
#
# app.run(main())


