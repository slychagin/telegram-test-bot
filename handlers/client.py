from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog.widgets.kbd import Button, Column, Keyboard
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Window, Dialog, StartMode
from aiogram import types, Dispatcher
from create_bot import bot, registry
from data_base import mongo_db
from keyboards.client_keyboard import chose_kb, start_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


test_id = None


class TestState(StatesGroup):
    """Create states for switch windows with questions"""
    # Get 100 states (this states we use for questions from 1 to n - 1, were n < 100)
    state_list = [f'state_{i}=State()' for i in range(101)]
    for state in state_list:
        exec(state)

    # State fo last question
    finish_state = State()


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
    global test_id
    test_id = callback_query.data.replace('show ', '')
    test_data = await mongo_db.db_read_one(test_id)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f'{test_data["test_name"]}\n\n'
             f'{test_data["test_description"]}\n\n'
             f'Для прохождения теста нажмите "Начать"\n'
             f'Для выбора другого теста нажмите "Выбрать тест"',
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


async def to_next(callback: CallbackQuery, button: Button, manager: DialogManager):
    """Switch to the next question"""
    await manager.dialog().next()


async def start_test(m: Message, dialog_manager: DialogManager):
    """Show questions with answers on buttons one by one"""
    test_data = await mongo_db.db_read_one(test_id)
    questions_amount = len(test_data['test_questions'])
    states = TestState.all_states
    print(test_data)

    window_list = []

    # Create windows for questions from first to lust by one
    for i, question in enumerate(test_data['test_questions']):
        question = test_data['test_questions'][i]['question_description']
        answers_list = test_data['test_questions'][i]['answers']

        if i < questions_amount:
            window = Window(
                Const(f'Вопрос {i + 1} из {questions_amount}\n{question}'),
                Column(
                    *[Button(
                        Const(f'{list(answer.keys())[0]}'),
                        id=f'{n}',
                        on_click=to_next
                    ) for n, answer in enumerate(answers_list)]),
                state=states[i],
            )
        else:
            window = Window(
                Const(f'Вопрос {questions_amount} из {questions_amount}\n{question}'),
                Column(
                    *[Button(
                        Const(f'{list(answer.keys())[0]}'),
                        id=f'{n}',
                        on_click=to_next
                    ) for n, answer in enumerate(answers_list)]),
                state=TestState.finish_state,
            )

        window_list.append(window)


    registry.register(Dialog(*window_list))

    await dialog_manager.start(state=TestState.all_states[0], mode=StartMode.RESET_STACK)






# async def start_test(m: Message, dialog_manager: DialogManager):
#     test_data = await mongo_db.db_read_one(test_id)
#     print(test_data)
#     questions_amount = len(test_data['test_questions'])
#
#
#     window_1 = Window(
#         Const("Вопрос 1"),
#         Column(
#             Button(Const("1"), id="1", on_click=to_next),
#             Button(Const("2"), id="2", on_click=to_next),
#             Button(Const("3"), id="3", on_click=to_next)
#         ),
#         state=TestState.all_states[0],
#     )
#
#     window_2 = Window(
#         Const("Вопрос 2"),
#         Column(
#             Button(Const("10"), id="4", on_click=to_next),
#             Button(Const("20"), id="5", on_click=to_next),
#             Button(Const("30"), id="6", on_click=to_next)
#         ),
#         state=TestState.all_states[1],
#     )
#
#     window_3 = Window(
#         Const("Вопрос 3"),
#         Column(
#             Button(Const("100"), id="7", on_click=to_next),
#             Button(Const("200"), id="8", on_click=to_next),
#             Button(Const("300"), id="9", on_click=to_next)
#         ),
#         state=TestState.all_states[-1],
#     )
#
#     registry.register(
#         Dialog(
#             window_1,
#             window_2,
#             window_3
#         )
#     )
#
#     await dialog_manager.start(state=TestState.all_states[0], mode=StartMode.RESET_STACK)




def register_client_handlers(dp: Dispatcher):
    """Register all client handlers"""
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(chose_test, commands=['Выбрать_тест'])
    dp.register_message_handler(parse_test_in_request, lambda message: 'тест' in message.text.lower())
    dp.register_callback_query_handler(callback_run_test, lambda x: x.data and x.data.startswith('show '))
    dp.register_message_handler(start_test, commands=['Начать'])
