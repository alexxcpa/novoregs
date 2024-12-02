from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command
import asyncio
import logger as log
from handlers import get_start, for_beginners, payout, connect_offers, about_caps, ref_programm

HELLO_BOT_API_TOKEN = "6597425495:AAHmSK9oVddKxa31yGVIb3E-oxkaJoVO0xA"

HELLO_BOT_TEST_API_TOKEN = "6811279790:AAGXBBFnO4eR3GMhZ1kBY_nn8-tsFp719LY"

TOKEN = HELLO_BOT_TEST_API_TOKEN

async def start():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(for_beginners, F.text == 'Я новичок')
    dp.message.register(payout, F.text == 'Как получить выплату')
    dp.message.register(connect_offers, F.text == 'Как подключить офферы')
    dp.message.register(about_caps, F.text == 'Про лимит в 100 конверсий')
    dp.message.register(ref_programm, F.text == 'Реферальная программа')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    log.msg.info('Бот начал работу')
    asyncio.run(start())
