import json
import string
from aiogram import types, Dispatcher


async def filter_forbidden_words(message: types.Message):
    """Delete messages with forbidden words"""
    bad_words = {word.lower().translate(str.maketrans('', '', string.punctuation)) for word in message.text.split(' ')}
    if bad_words.intersection(set(json.load(open('cenzura.json')))):
        await message.reply('Нецензурные слова в чате запрещены!')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    """Register other handlers"""
    dp.register_message_handler(filter_forbidden_words)
