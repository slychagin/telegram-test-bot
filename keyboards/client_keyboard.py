from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# Buttons
btn_chose_test = KeyboardButton('Выбрать тест')
btn_cancel = KeyboardButton('Выйти')
btn_start_test = KeyboardButton('Начать')

btn_next_test = InlineKeyboardButton(
                text='Выбрать другой тест',
                callback_data='Выбрать тест')


# Keyboards
chose_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
chose_kb.add(btn_chose_test).add(btn_cancel)

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_kb.add(btn_start_test).add(btn_cancel)

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_kb.add(btn_cancel)

chose_next_kb = InlineKeyboardMarkup()
chose_next_kb.add(btn_next_test)
