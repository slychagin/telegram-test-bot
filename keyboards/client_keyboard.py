from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


# Add chose button
btn_chose_test = KeyboardButton('/Выбрать_тест')
chose_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
chose_kb.add(btn_chose_test)

# Add start test button
btn_start_test = KeyboardButton('/Начать')
start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_kb.add(btn_start_test).add(btn_chose_test)
