import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import bot, dp
from data_base import mongo_db
from keyboards.client_keyboard import chose_kb, start_kb, cancel_kb, chose_next_kb
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from lexical_data import result

test_id = None


class FSMClient(StatesGroup):
    """Create client dialog states"""
    chose = State()
    show_tests = State()
    testing = State()
    answers = State()


async def command_start(message: types.Message):
    """Bot starts test"""
    try:
        await bot.send_message(
            message.from_user.id,
            'Привет! \U0001F44B\n\nНажми "Выбрать тест"\nДля выхода "Выйти"',
            reply_markup=chose_kb)
        await FSMClient.chose.set()
    except:
        await message.reply('Общение с ботом чрез ЛС, напишите ему:\nhttps://t.me/VirtualTestingBot')


@dp.message_handler(state='*', commands='Выйти')
@dp.message_handler(Text(equals='Выйти', ignore_case=True), state='*')
async def cancel_command(message: types.Message, state: FSMContext):
    """Allow user to cancel any action"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('До свидания!', reply_markup=ReplyKeyboardRemove())


async def chose_test(message: types.Message, state: FSMContext):
    """Get data from db and send inline buttons with test names"""
    tests = await mongo_db.db_read_all()
    count_test = await mongo_db.db_count_test()
    test_buttons_kb = InlineKeyboardMarkup()

    # Add inline buttons
    for i, test in enumerate(tests):
        test_buttons_kb.add(
            InlineKeyboardButton(
                f'Тест {i+1}: "{test["test_name"]}"',
                callback_data=f'show {test["_id"]}'),
        )

    # Send message with inline buttons
    if count_test == 0:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Упс \U0001F615.\n'
                 'На данный момент администратор добавляет тесты.\n'
                 'Попробуйте написать боту немного позже \U0001F60A'
        )
        await state.finish()
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='\U0001F447 Выбери тест \U0001F447',
            reply_markup=test_buttons_kb
        )
        await FSMClient.next()


async def callback_run_test(callback_query: types.CallbackQuery):
    """Run chosen test"""
    global test_id
    test_id = callback_query.data.replace('show ', '')
    test_data = await mongo_db.db_read_one(test_id)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f'\U0001F4D6 {test_data["test_name"]}\n\n'
             f'\U0000270F {test_data["test_description"]}\n\n\n'
             f'\U00002757 Для прохождения теста нажми "Начать"'
             f'\n\U00002753 Для выхода "Выйти"',
        reply_markup=start_kb
    )
    await FSMClient.next()


async def start_test(message: types.Message, state: FSMContext):
    """Show questions with answers on buttons one by one"""
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='\U000026AA\U000026AA\U000026AA\U000026AA\U000026AA\U000026AA\U000026AA'
             '\U000026AA\U000026AA\U000026AA\U000026AA\U000026AA',
        reply_markup=cancel_kb
    )

    test_data = await mongo_db.db_read_one(test_id)
    questions_amount = len(test_data['test_questions'])

    async with state.proxy() as data:
        data['answers'] = []
        data['cur_question'] = 1

        for i, question in enumerate(test_data['test_questions']):
            if i != 0:
                break

            question = test_data['test_questions'][i]['question_description']
            answers = test_data['test_questions'][i]['answers']
            answer_buttons_kb = InlineKeyboardMarkup()

            buttons = [InlineKeyboardButton(text=f'{answer}', callback_data=f'{answer}') for answer in answers]

            for button in buttons:
                answer_buttons_kb.add(button)

            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'Вопрос {i+1} из {questions_amount}\n\n{question}',
                reply_markup=answer_buttons_kb
            )
    await FSMClient.answers.set()


async def callback_press_answer_button(callback_query: types.CallbackQuery, state: FSMContext):
    """When answer button pressed answer send to callback_query_handler and compare with right answers"""
    test_data = await mongo_db.db_read_one(test_id)
    questions_amount = len(test_data['test_questions'])

    # Create dict with all answers
    all_answers = {}
    for question in test_data['test_questions']:
        all_answers.update(question['answers'])

    async with state.proxy() as data:
        data['answers'].append(callback_query.data)

        # Send message if first question right or wrong
        point = len([1 for i in data['answers'] if all_answers[i] == 1])
        if len(data['answers']) == 1 and point == 1:
            await bot.edit_message_text(
                chat_id=callback_query['message']['chat']['id'],
                message_id=callback_query['message']['message_id'],
                text=f'{result.get_right_answer()}')
            await asyncio.sleep(1.2)

        if len(data['answers']) == 1 and point == 0:
            for answer in test_data['test_questions'][0]['answers']:
                if test_data['test_questions'][0]['answers'][answer] == 1:
                    right_answer = answer

            await bot.edit_message_text(
                chat_id=callback_query['message']['chat']['id'],
                message_id=callback_query['message']['message_id'],
                text=f'{result.get_wrong_answer()}\n\nПравильный ответ:\n"{right_answer}"')
            await asyncio.sleep(3)

        # Send questions to user one by one
        for i, question in enumerate(test_data['test_questions']):
            if i == data['cur_question']:

                # Send message if question right or wrong
                if all_answers[data['answers'][-1]] == 1 and len(data['answers']) > 1:
                    await bot.edit_message_text(
                        chat_id=callback_query['message']['chat']['id'],
                        message_id=callback_query['message']['message_id'],
                        text=f'{result.get_right_answer()}')
                    await asyncio.sleep(1.2)

                if all_answers[data['answers'][-1]] == 0 and len(data['answers']) > 1:
                    for answer in test_data['test_questions'][i-1]['answers']:
                        if test_data['test_questions'][i-1]['answers'][answer] == 1:
                            right_answer = answer
                    await bot.edit_message_text(
                        chat_id=callback_query['message']['chat']['id'],
                        message_id=callback_query['message']['message_id'],
                        text=f'{result.get_wrong_answer()}\n\nПравильный ответ:\n"{right_answer}"')
                    await asyncio.sleep(3)

                question = test_data['test_questions'][i]['question_description']
                answers = test_data['test_questions'][i]['answers']
                answer_buttons_kb = InlineKeyboardMarkup()

                buttons = [InlineKeyboardButton(text=f'{answer}', callback_data=f'{answer}') for answer in answers]

                for button in buttons:
                    answer_buttons_kb.add(button)

                await bot.edit_message_text(
                    chat_id=callback_query['message']['chat']['id'],
                    message_id=callback_query['message']['message_id'],
                    text=f'Вопрос {i + 1} из {questions_amount}\n\n{question}',
                    reply_markup=answer_buttons_kb
                )

                break
        data['cur_question'] += 1

        # Count results
        if len(data['answers']) == questions_amount:
            # Send message if last question right or wrong
            if all_answers[data['answers'][-1]] == 1:
                await bot.edit_message_text(
                    chat_id=callback_query['message']['chat']['id'],
                    message_id=callback_query['message']['message_id'],
                    text=f'{result.get_right_answer()}')
                await asyncio.sleep(1.2)

            if all_answers[data['answers'][-1]] == 0:
                for answer in test_data['test_questions'][i]['answers']:
                    if test_data['test_questions'][i]['answers'][answer] == 1:
                        right_answer = answer
                await bot.edit_message_text(
                    chat_id=callback_query['message']['chat']['id'],
                    message_id=callback_query['message']['message_id'],
                    text=f'{result.get_wrong_answer()}\n\nПравильный ответ:\n"{right_answer}"')
                await asyncio.sleep(3)

            points = len([1 for i in data['answers'] if all_answers[i] == 1])

            result_message = f'{result.get_result_congrat(points, questions_amount)}' \
                             f'\n\n\U00002705 Тест пройден с результатом {points} из {questions_amount}'

            await bot.edit_message_text(
                chat_id=callback_query['message']['chat']['id'],
                message_id=callback_query['message']['message_id'],
                text=result_message,
                reply_markup=chose_next_kb
            )

            await state.finish()


async def callback_next_test(callback_query: types.CallbackQuery, state: FSMContext):
    """After complete test user can choose another test"""
    await FSMClient.chose.set()
    await bot.send_message(
        chat_id=callback_query['message']['chat']['id'],
        text='Для выбора теста нажми "Выбрать тест" \U0001F447',
        reply_markup=chose_kb
    )


def register_client_handlers(dp: Dispatcher):
    """Register all client handlers"""
    dp.register_message_handler(command_start, commands=['start', 'help'], state=None)
    dp.register_message_handler(chose_test, commands=['Выбрать тест'], state=FSMClient.chose)
    dp.register_message_handler(chose_test, Text(contains='Выбрать тест', ignore_case=True), state=FSMClient.chose)
    dp.register_callback_query_handler(callback_run_test, lambda x: x.data and x.data.startswith('show '), state=FSMClient.show_tests)
    dp.register_message_handler(start_test, commands=['Начать'], state=FSMClient.testing)
    dp.register_message_handler(start_test, Text(contains='Начать', ignore_case=True), state=FSMClient.testing)
    dp.register_callback_query_handler(callback_press_answer_button, state=FSMClient.answers)
    dp.register_callback_query_handler(callback_next_test, lambda x: x.data and x.data.startswith('Выбрать тест'))

