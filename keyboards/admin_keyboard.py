from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(button_load).add(button_delete)
