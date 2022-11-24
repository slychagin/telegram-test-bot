from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

# Create admin buttons
load_button = KeyboardButton('/Загрузить')
delete_button = KeyboardButton('/Удалить')
cancel_button = KeyboardButton('/Отмена')
# save_button = KeyboardButton('/Сохранить')
# add_answers = KeyboardButton('/Добавить_ответы')

# Add buttons on admin keyboard
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(load_button).add(delete_button).add(cancel_button)

# Add save button
# save_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# save_kb.add(save_button)

# Add answers
# add_answers_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# add_answers_kb.add(add_answers)
