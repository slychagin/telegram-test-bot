from aiogram import types, Dispatcher
from create_bot import bot


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствую Вас!')
        await message.delete()
    except:
        await message.reply('Общение с ботом чрез ЛС, напишите ему:\nhttps://t.me/VirtualTestingBot')


async def start_test(message: types.Message):
    await bot.send_message(message.from_user.id, 'Начнем тестирование!')


def register_handlers_client(dp: Dispatcher):
    """Register all client handlers"""
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(start_test, commands=['Начать'])

