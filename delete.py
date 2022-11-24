from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import mongo_db
from keyboards import admin_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ReplyKeyboardRemove

ID = None


class FSMAdmin(StatesGroup):
    test_name = State()
    test_description = State()
    test_results = State()
    test_questions = State()
    answers = State()


async def make_changes_command(message: types.Message):
    """Check is user admin. If admin then allow changes."""
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id,
        'Добро пожаловать в админ панель!\nЧто будем делать?',
        reply_markup=admin_keyboard.admin_kb
    )
    await message.delete()


async def start_state(message: types.Message):
    """Start dialog to load a new test to database"""
    if message.from_user.id == ID:
        await FSMAdmin.test_name.set()
        await message.answer('Введите название теста')


async def save_questions_handler(message: types.Message, state: FSMContext):
    """Save questions to database when admin push save button and proceed to fill in the answers"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await FSMAdmin.next()
        await message.answer('Вопросы сохранены в базу данных', reply_markup=ReplyKeyboardRemove())
        await message.answer('Далее нажмите "Добавить ответы"', reply_markup=admin_keyboard.add_answers_kb)
        await message.delete()


async def cancel_handler(message: types.Message, state: FSMContext):
    """Escaping from all states"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('ОК')


async def load_test_name(message: types.Message, state: FSMContext):
    """Save test name to db"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['test_name'] = message.text
        await mongo_db.add_test_to_db(state)
        await FSMAdmin.next()
        await message.answer('Введите описание теста')


async def load_test_description(message: types.Message, state: FSMContext):
    """Save test description to db"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['test_description'] = message.text
        await mongo_db.update_test(state)
        await FSMAdmin.next()
        await message.answer('Введите описание результатов теста')


async def load_test_results(message: types.Message, state: FSMContext):
    """Save test results description to db"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['test_results'] = message.text
        await mongo_db.update_test(state)
        await FSMAdmin.next()
        await message.answer(
            'Введите вопросы для теста.'
            '\nЧтобы закончить вводить вопросы нажмите Сохранить.',
            reply_markup=admin_keyboard.save_kb
        )


n = 0
question_lst = []


async def load_test_questions(message: types.Message, state: FSMContext):
    """Load questions"""
    global n
    global question_lst
    n += 1

    if message.from_user.id == ID:
        async with state.proxy() as data:
            question_lst.append({f'Вопрос {n}': message.text})
            data['test_questions'] = question_lst
        await mongo_db.update_test(state)


async def load_answers(message: types.Message, state: FSMContext):
    """Load answers for particular question"""
    if message.from_user.id == ID:
        questions = await mongo_db.read_all_questions(state)
        print(questions)
        for item in questions:
            for i in item:
                await bot.send_message(
                    message.from_user.id,
                    text=f'{i}\n{item[i]}',
                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                        'Добавить ответы',
                        callback_data='del'
                    ))
                )





















def register_admin_handlers(dp: Dispatcher):
    """Register all admin handlers"""
    dp.register_message_handler(start_state, commands=['Загрузить'], state=None)
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(save_questions_handler, state='*', commands=['Сохранить'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_test_name, state=FSMAdmin.test_name)
    dp.register_message_handler(load_test_description, state=FSMAdmin.test_description)
    dp.register_message_handler(load_test_results, state=FSMAdmin.test_results)
    dp.register_message_handler(load_test_questions, state=FSMAdmin.test_questions)
    dp.register_message_handler(load_answers, state=FSMAdmin.answers, commands=['Добавить_ответы'])
