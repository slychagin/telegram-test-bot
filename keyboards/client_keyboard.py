from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_start_test = KeyboardButton('/Начать')

# button4 = KeyboardButton('Поделиться контактом', request_contact=True)
# button5 = KeyboardButton('Отправить где я', request_location=True)

client_kb = ReplyKeyboardMarkup(resize_keyboard=True)

client_kb.add(btn_start_test)  # .row(button4, button5)
