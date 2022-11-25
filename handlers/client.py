from pprint import pprint

from aiogram import types, Dispatcher
from create_bot import bot
from data_base import mongo_db
from keyboards.client_keyboard import chose_kb, start_kb
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def parse_test_in_request(message: types.Message):
    """If the client request contains a test, then the bot starts the test"""
    await command_start(message)


async def command_start(message: types.Message):
    """Bot starts test"""
    try:
        await bot.send_message(
            message.from_user.id,
            'Приветствую Вас! \U0001F44B'
            '\nНажмите "Выбрать тест" для выбора теста.',
            reply_markup=chose_kb,

        )
        await message.delete()
    except:
        await message.reply('Общение с ботом чрез ЛС, напишите ему:\nhttps://t.me/VirtualTestingBot')


async def callback_run_test(callback_query: types.CallbackQuery):
    """Run chosen test"""
    test_id = callback_query.data.replace('show ', '')
    test_data = await mongo_db.db_read_one(test_id)
    print(test_data)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f'{test_data["test_name"]}\n\n'
             f'{test_data["test_description"]}\n\n'
             f'Для прохождения теста нажмите "Начать"',
        reply_markup=start_kb
    )


async def chose_test(message: types.Message):
    """Get data from db and send inline buttons with test names"""
    tests = await mongo_db.db_read_all()
    count_test = await mongo_db.db_count_test()
    inline_buttons_kb = InlineKeyboardMarkup()

    # Add inline buttons
    for test in tests:
        inline_buttons_kb.add(
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
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='\U0001F447 Выберите тест \U0001F447',
            reply_markup=inline_buttons_kb
        )


async def start_test(message: types.Message):
    """Start test, show question with answers one by one"""
    pass













def register_client_handlers(dp: Dispatcher):
    """Register all client handlers"""
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(chose_test, commands=['Выбрать_тест'])
    dp.register_message_handler(parse_test_in_request, lambda message: 'тест' in message.text.lower())
    dp.register_callback_query_handler(callback_run_test, lambda x: x.data and x.data.startswith('show '))
    dp.register_message_handler(start_test, commands=['Начать'])
