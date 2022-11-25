import asyncio
from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import mongo_db


async def on_startup(_):
    print('Бот вышел онлайн.')
    await mongo_db.connect_db()


admin.register_admin_handlers(dp)
client.register_client_handlers(dp)
other.register_other_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

