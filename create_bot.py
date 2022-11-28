from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram_dialog import DialogRegistry

storage = MemoryStorage()

bot = Bot(token='5619553113:AAHKZ_tsmp5UBmoiPBxK39_0xo4qLE3sqVw')
dp = Dispatcher(bot, storage=storage)

registry = DialogRegistry(dp)
