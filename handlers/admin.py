from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import admin_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None


class FSMAdmin(StatesGroup):
    test_name = State()
    test_description = State()
    test_results = State()
    # question = State()
    # answer = State()


async def make_changes_command(message: types.Message):
    """Check is user admin. If admin then allow changes."""
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id,
        'Добро пожаловать в админ панель!\nЧто будем делать?',
        # reply_markup=admin_keyboard.admin_kb
    )
    await message.delete()


async def start_state(message: types.Message):
    """Start dialog to load a new test to database"""
    if message.from_user.id == ID:
        await FSMAdmin.test_name.set()
        await message.answer('Введите название теста')


async def cancel_handler(message: types.Message, state: FSMContext):
    """Escaping from all states"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('ОК')


async def load_test_name(message: types.Message, state: FSMContext):
    """Get first answer and save test name to dictionary"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['test_name'] = message.text
        await FSMAdmin.next()
        await message.answer('Введите описание теста')


async def load_test_description(message: types.Message, state: FSMContext):
    """Get second answer and save test description to dictionary"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['test_description'] = message.text
        await FSMAdmin.next()
        await message.answer('Введите описание результатов теста')


async def load_test_results(message: types.Message, state: FSMContext):
    """Get third answer and save test results description ti dictionary"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['test_results'] = message.text

        async with state.proxy() as data:
            await message.answer(str(data))

        await state.finish()








def register_admin_handlers(dp: Dispatcher):
    """Register all admin handlers"""
    dp.register_message_handler(start_state, commands='Загрузить', state=None)
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_test_name, state=FSMAdmin.test_name)
    dp.register_message_handler(load_test_description, state=FSMAdmin.test_description)
    dp.register_message_handler(load_test_results, state=FSMAdmin.test_results)



