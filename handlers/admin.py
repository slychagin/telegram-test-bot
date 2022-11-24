import json
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import mongo_db
from keyboards import admin_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ReplyKeyboardRemove, ContentTypes

ID = None


class FSMAdmin(StatesGroup):
    load_file = State()


async def make_changes_command(message: types.Message):
    """Check is user admin. If admin then allow changes."""
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id,
        'Добро пожаловать в админ панель!\n'
        'Чтобы загрузить новый тест нажмите "Загрузить".\n\n'
        'Чтобы удалить тест нажмите "Удалить" и выберите тест для удаления.\n\n'
        'Для отмены нажмите "Отмена".',
        reply_markup=admin_keyboard.admin_kb
    )
    await message.delete()


async def start_command(message: types.Message):
    """Start dialog to load a new test to database"""
    if message.from_user.id == ID:
        await FSMAdmin.load_file.set()
        await message.answer('Прикрепите файл в формате JSON.')


async def cancel_handler(message: types.Message, state: FSMContext):
    """Escaping from all states"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('ОК')


async def load_test(message: types.Message, state: FSMContext):
    """Load document, get data and save it to db"""
    if message.from_user.id == ID:
        file_id = message.document.file_id
        bytes_file = await bot.download_file_by_id(file_id)
        str_data = bytes_file.getvalue().decode('utf-8')
        dict_data = json.loads(str_data)

        print(type(dict_data))
        print(dict_data)
        await mongo_db.add_test_to_db(dict_data)

        await state.finish()
        await message.answer('Тест загружен в базу данных.')









def register_admin_handlers(dp: Dispatcher):
    """Register all admin handlers"""
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(start_command, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_test, content_types=['document'], state=FSMAdmin.load_file)
