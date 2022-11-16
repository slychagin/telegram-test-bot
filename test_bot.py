import os


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler()
async def welcome_message(message: types.Message):
    # await message.answer(message.text)
    # await message.reply(message.text)
    await bot.send_message(message.from_user.id, message.text)





executor.start_polling(dp, skip_updates=True)
