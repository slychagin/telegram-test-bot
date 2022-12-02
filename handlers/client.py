from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.kbd import Button, Column, Keyboard, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram_dialog import DialogManager, Window, Dialog, StartMode
from aiogram import types, Dispatcher
from create_bot import bot, registry
from data_base import mongo_db
from keyboards.client_keyboard import chose_kb, start_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

test_id = None


class FSMClient(StatesGroup):
    """Create client dialog states"""
    chose = State()
    show_tests = State()
    testing = State()


    # Get 51 states (this states we use for questions from 1 to n - 1, were n < 51)
    # state_list = [f'state_{i}=State()' for i in range(51)]
    # for state in state_list:
    #     exec(state)

    results = State()


async def parse_test_in_request(message: types.Message):
    """If the client request contains a test, then the bot starts the test"""
    await command_start(message)


async def command_start(message: types.Message):
    """Bot starts test"""
    try:
        await bot.send_message(
            message.from_user.id,
            'Приветствую Вас! \U0001F44B'
            '\nНажмите "Выбрать тест"',
            reply_markup=chose_kb,

        )
        await message.delete()
        await FSMClient.chose.set()
    except:
        await message.reply('Общение с ботом чрез ЛС, напишите ему:\nhttps://t.me/VirtualTestingBot')


async def chose_test(message: types.Message, state: FSMContext):
    """Get data from db and send inline buttons with test names"""
    tests = await mongo_db.db_read_all()
    count_test = await mongo_db.db_count_test()
    test_buttons_kb = InlineKeyboardMarkup()

    # Add inline buttons
    for test in tests:
        test_buttons_kb.add(
            InlineKeyboardButton(
                f'{test["test_name"]}',
                callback_data=f'show {test["_id"]}')
        )

    # Send message with inline buttons
    if count_test == 0:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Упс \U0001F615.\n'
                 'Кажется на данный момент администратор добавляет новые тесты.\n'
                 'Попробуйте написать боту немного позже \U0001F60A'
        )
        await state.finish()
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='\U0001F447 Выберите тест \U0001F447',
            reply_markup=test_buttons_kb
        )
        await FSMClient.next()


async def callback_run_test(callback_query: types.CallbackQuery, state: FSMContext):
    """Run chosen test"""
    global test_id
    test_id = callback_query.data.replace('show ', '')
    test_data = await mongo_db.db_read_one(test_id)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f'Тема:\n{test_data["test_name"]}\n\n'
             f'Описание теста:\n{test_data["test_description"]}\n\n\n'
             f'Для прохождения теста нажмите "Начать"\n'
             f'Для выбора другого теста нажмите "Выбрать тест"',
        reply_markup=start_kb
    )
    await FSMClient.next()


async def start_test(message: types.Message, state: FSMContext):
    """Show questions with answers on buttons one by one"""

    test_data = await mongo_db.db_read_one(test_id)
    questions_amount = len(test_data['test_questions'])

    async with state.proxy() as data:
        data['answers'] = []
        data['cur_question'] = 1

        for i, question in enumerate(test_data['test_questions']):
            if i != 0:
                break

            question = test_data['test_questions'][i]['question_description']
            answers_list = test_data['test_questions'][i]['answers']
            answer_buttons_kb = InlineKeyboardMarkup()

            buttons = [
                InlineKeyboardButton(
                    text=f'{list(answer.keys())[0]}',
                    callback_data=f'{list(answer.keys())[0]}'
                ) for answer in answers_list]

            for button in buttons:
                answer_buttons_kb.add(button)

            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'Вопрос {i+1} из {questions_amount}\n{question}',
                reply_markup=answer_buttons_kb
            )
    await FSMClient.results.set()


async def callback_press_answer_button(callback_query: types.CallbackQuery, state: FSMContext):
    """When answer button pressed answer send to callback_query_handler and compare with right answers"""
    test_data = await mongo_db.db_read_one(test_id)
    questions_amount = len(test_data['test_questions'])

    async with state.proxy() as data:
        data['answers'].append(callback_query.data)
        print(data['answers'])

        for i, question in enumerate(test_data['test_questions']):
            if i == data['cur_question']:
                question = test_data['test_questions'][i]['question_description']
                answers_list = test_data['test_questions'][i]['answers']
                answer_buttons_kb = InlineKeyboardMarkup()

                buttons = [
                    InlineKeyboardButton(
                        text=f'{list(answer.keys())[0]}',
                        callback_data=f'{list(answer.keys())[0]}'
                    ) for answer in answers_list]

                for button in buttons:
                    answer_buttons_kb.add(button)

                await bot.send_message(
                    chat_id=callback_query['message']['chat']['id'],
                    text=f'Вопрос {i+1} из {questions_amount}\n{question}',
                    reply_markup=answer_buttons_kb
                )
                break

        data['cur_question'] += 1












def register_client_handlers(dp: Dispatcher):
    """Register all client handlers"""
    dp.register_message_handler(command_start, commands=['start', 'help'], state=None)
    dp.register_message_handler(parse_test_in_request, lambda message: 'тест' in message.text.lower())
    dp.register_message_handler(chose_test, commands=['Выбрать_тест'], state=FSMClient.chose)
    dp.register_callback_query_handler(callback_run_test, lambda x: x.data and x.data.startswith('show '), state=FSMClient.show_tests)
    dp.register_message_handler(start_test, commands=['Начать'], state=FSMClient.testing)
    dp.register_callback_query_handler(callback_press_answer_button, state=FSMClient.results)


