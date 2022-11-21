from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Create admin buttons
load_button = KeyboardButton('/Загрузить')
delete_button = KeyboardButton('/Удалить')
save_button = KeyboardButton('/Сохранить')

# Add buttons on admin keyboard
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(load_button).add(delete_button)

# Add save button
save_kb = ReplyKeyboardMarkup(resize_keyboard=True)
save_kb.add(save_button)
