from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Create admin buttons
load_button = KeyboardButton(text='Загрузить')
delete_button = KeyboardButton(text='Удалить')
cancel_button = KeyboardButton(text='Отмена')

# Add buttons on admin keyboard
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(load_button).add(delete_button).add(cancel_button)
