import json
import os
import string

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот вышел онлайн.')


# CLIENT
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствую Вас!')
        await message.delete()
    except:
        await message.reply('Общение с ботом чрез ЛС, напишите ему:\nhttps://t.me/VirtualTestingBot')


@dp.message_handler(commands=['Начать'])
async def start_test(message: types.Message):
    await bot.send_message(message.from_user.id, 'Начнем тестирование!')


# ADMIN




# OTHER
@dp.message_handler()
async def filter_forbidden_words(message: types.Message):
    """Delete messages with forbidden words"""
    bad_words = {word.lower().translate(str.maketrans('', '', string.punctuation)) for word in message.text.split(' ')}
    if bad_words.intersection(set(json.load(open('cenzura.json')))):
        await message.reply('Нецензурные слова в чате запрещены!')
        await message.delete()





executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
