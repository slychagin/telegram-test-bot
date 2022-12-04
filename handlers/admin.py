import json
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, AdminFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bot, dp
from data_base import mongo_db
from keyboards import admin_keyboard

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


async def start_command(message: types.Message):
    """Start dialog to load a new test to database"""
    if message.from_user.id == ID:
        await FSMAdmin.load_file.set()
        await message.answer('Прикрепите файл в формате JSON')


@dp.message_handler(state='*', commands=['Отмена'])
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Escaping from all states"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


async def load_test(message: types.Message, state: FSMContext):
    """Load document, get data and save it to db"""
    if message.from_user.id == ID:
        file_id = message.document.file_id
        bytes_file = await bot.download_file_by_id(file_id)
        try:
            str_data = bytes_file.getvalue().decode('utf-8')
            dict_data = json.loads(str_data)
            await mongo_db.add_test_to_db(dict_data)

            await state.finish()
            await message.answer('Тест загружен в базу данных\U0001F44C')
        except:
            await message.answer('\U0000274C Файл невозможно загрузить в базу данных.\n'
                                 'Необходим файл установленного формата.')


async def delete_test(message: types.Message):
    """Load list of tests with delete buttons. Allow to delete chosen test"""
    if message.from_user.id == ID:
        count_test = await mongo_db.db_count_test()
        if count_test == 0:
            await bot.send_message(
                message.from_user.id,
                text=f'В базе данных тестов нет.'
            )
        else:
            await bot.send_message(
                message.from_user.id,
                text=f'Количество тестов в базе данных: {count_test}'
            )

        tests = await mongo_db.db_read_all()
        for test in tests:
            await bot.send_message(
                message.from_user.id,
                text=f'{test["test_name"]}',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                    text='Удалить',
                    callback_data=f'del {test["_id"]}'
                ))
            )


async def callback_delete(callback_query: types.CallbackQuery):
    """Delete chosen test"""
    test_id = callback_query.data
    await mongo_db.db_delete_command(test_id.replace('del ', ''))
    await callback_query.answer(
        text=f'Тест удален.',
        show_alert=True
    )
    await bot.delete_message(chat_id=ID, message_id=callback_query.message['message_id'])


def register_admin_handlers(dp: Dispatcher):
    """Register all admin handlers"""
    dp.register_message_handler(make_changes_command, AdminFilter(is_chat_admin=True), commands=['admin'])
    dp.register_message_handler(start_command, commands=['Загрузить'], state=None)
    dp.register_message_handler(start_command, Text(contains='Загрузить', ignore_case=True))
    dp.register_message_handler(load_test, content_types=['document'], state=FSMAdmin.load_file)
    dp.register_message_handler(delete_test, commands=['Удалить'])
    dp.register_message_handler(delete_test, Text(contains='Удалить', ignore_case=True))
    dp.register_callback_query_handler(callback_delete, lambda x: x.data and x.data.startswith('del '))
