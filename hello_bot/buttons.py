from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keaboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Я новичок')],

    [KeyboardButton(text='Как получить выплату')],

    [KeyboardButton(text='Как подключить офферы')],

    [KeyboardButton(text='Про лимит в 100 конверсий')],

    [KeyboardButton(text='Реферальная программа')],


], resize_keyboard=True)

keaboard2 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Я новичок'),
    KeyboardButton(text='Как получить выплату')],

    [KeyboardButton(text='Как подключить офферы'),
     KeyboardButton(text='Про лимит в 100 конверсий')],

    [KeyboardButton(text='Реферальная программа')],


], resize_keyboard=True)