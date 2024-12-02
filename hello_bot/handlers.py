from aiogram import Bot
from aiogram.types import Message
import logger as log
from messages import *
import requests
from buttons import keaboard2

from database import hello_bot_db as db

HELLO_BOT_MONITORING_API_TOKEN = "7544625663:AAHpt_v4r99ZIBHcyykxAG8hIoT_W8uWhhA"
CHAT_ID = '1457459092'

KEYBOARD = keaboard2

def send_monitoring(msg):
    try:
        r = requests.get(
            f'https://api.telegram.org/bot{HELLO_BOT_MONITORING_API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=markdown')
        return True if r.status_code == 200 else False
    except:
        return False


async def get_start(message: Message, bot: Bot):
    partner_id = message.text.replace('/start', '').strip(' ') # проверяем id веба на корректность
    if len(partner_id) != 0:
        if len(partner_id) <= 5:
            try:
                partner_id = int(partner_id)
                if db.get_tg_user_id(message.from_user.id):  # если текущий юзер id есть в базе бота
                    check_result = db.validation_by_chat_id(message.from_user.id)
                    if partner_id == check_result['partner_id']:
                        log.msg.info(f"Пользователь {message.from_user.username} попал в бота с привязанным аккаунтом")
                        await message.answer(f"И снова привет {message.from_user.first_name}! \n {SECOND_START_HELLO_MSG}", 'HTML', reply_markup=KEYBOARD)
                    else:
                        log.msg.info(f"Пользователь {message.from_user.username} попал в бота c чужим id")
                        await message.answer(f"Привет {message.from_user.first_name}! \n {STRANGE_PARTNER_ID_MSG}",
                                             'HTML')

                elif db.get_partner_from_crm(partner_id):  # если текущего юзер id нет в базе, проверяем реальность id партнера
                    if db.validation_by_partner_id(partner_id):
                        log.msg.info(f"Пользователь {message.from_user.username} попал в бота c чужим id")
                        await message.answer(f"Привет {message.from_user.first_name}! \n {STRANGE_PARTNER_ID_MSG}", 'HTML')
                    else:
                        log.msg.info(f"Пользователь {message.from_user.username} впервые попал в бота")
                        await message.answer(
                        f"Привет {message.from_user.first_name}! \n\n Твой id: {partner_id} \n {HELLO_MSG}", 'HTML',
                        reply_markup=KEYBOARD)
                        send_monitoring(f'Партнер {partner_id} успешно привязял бота с тг {message.from_user.id}')
                        db.add_user(partner_id,
                                    message.from_user.id,
                                    message.from_user.username,
                                    message.from_user.first_name,
                                    message.from_user.last_name)
            except ValueError as err:
                print(err)
                log.msg.error(
                    f"Ошибка! Пользователь {message.from_user.username} попал в бота c невалидным id аккаунта")
                await message.answer(f"Привет {message.from_user.first_name}! {INVALID_PARTNER_ID_MSG}", 'HTML')

        else:
            if db.get_tg_user_id(message.from_user.id):
                await message.answer(f"И снова привет {message.from_user.first_name}! \n {SECOND_START_HELLO_MSG}",
                                     'HTML',
                                     reply_markup=KEYBOARD)
            else:
                log.msg.info(f"Пользователь {message.from_user.username} попал в бота c невалидным id аккаунта")
                await message.answer(f"Привет {message.from_user.first_name}! {INVALID_PARTNER_ID_MSG}", 'HTML')

    else:
        if db.get_tg_user_id(message.from_user.id):
            await message.answer(f"И снова привет {message.from_user.first_name}! \n {SECOND_START_HELLO_MSG}", 'HTML',
                                 reply_markup=KEYBOARD)
        else:
            log.msg.info(f"Пользователь {message.from_user.username} попал в бота без привязки к аккаунту")
            await message.answer(f"Привет {message.from_user.first_name}! {WITHOUT_ACCOUNT_MSG}", 'HTML')


async def for_beginners(message: Message, bot: Bot):
    await message.answer(FOR_BEGINNERS_MSG, 'HTML',
        reply_markup=KEYBOARD)


async def payout(message: Message, bot: Bot):
    await message.answer(PAYOUT_MSG, 'HTML',
        reply_markup=KEYBOARD)

async def connect_offers(message: Message, bot: Bot):
    await message.answer(OFFERS_CONNECT_MANUAL, 'HTML',
        reply_markup=KEYBOARD)

async def about_caps(message: Message, bot: Bot):
    await message.answer(ABOUT_CAPS_MSG, 'HTML',
        reply_markup=KEYBOARD)
async def ref_programm(message: Message, bot: Bot):
    await message.answer(REF_PROGRAM, 'HTML',
        reply_markup=KEYBOARD)



