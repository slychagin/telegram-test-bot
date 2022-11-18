from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.client_keyboard import client_kb
from aiogram.types import ReplyKeyboardRemove


async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id,
            'Приветствую Вас!\nНажмите "Начать" для начала тестирования.',
            reply_markup=client_kb
        )
        await message.delete()
    except:
        await message.reply('Общение с ботом чрез ЛС, напишите ему:\nhttps://t.me/VirtualTestingBot')


async def start_test(message: types.Message):
    await bot.send_message(message.from_user.id, 'Тест начался!')  # reply_markup=ReplyKeyboardRemove()


def register_handlers_client(dp: Dispatcher):
    """Register all client handlers"""
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(start_test, commands=['Начать'])

