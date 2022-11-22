import asyncio
import motor.motor_asyncio

from create_bot import dp


async def connect_db():
    """Connect to MongoDB Atlas"""
    global client, collection
    conn_str = 'mongodb+srv://Serhio:Pandora777@cluster0.mvbi9na.mongodb.net/?retryWrites=true&w=majority'
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
    collection = client.online_test_db.test

    try:
        print('Connecting to data base is OK!')
    except Exception:
        print("Unable to connect to the server.")


async def add_test_to_db(state):
    """Add new test to database"""
    current_state = await dp.current_state().get_data()
    print(current_state)
    await collection.insert_one(current_state)


async def update_test(state):
    """Update new test"""
    current_state = await dp.current_state().get_data()
    print(current_state)
    async with state.proxy() as data:
        await collection.update_one(
            {'test_name': data['test_name']},
            {'$set': current_state}
        )


async def read_all_questions(state):
    """Read all questions from database"""
    async with state.proxy() as data:
        questions = collection.find({'test_name': data['test_name']})

    async for document in questions:
        return document['test_questions']



# async def add_question(state):
#     """Add question to db"""
#     async with state.proxy() as data:
#         await collection.find_one(data['test_question'])





# def connect_db():
#     """Create or connect to db"""
#     global conn, cur
#     conn = db.connect('online_test.db')
#     cur = conn.cursor()
#     if conn:
#         print('Data base connected OK!')
#     cur.execute('CREATE TABLE IF NOT EXISTS test(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
#     conn.commit()
#
#
# async def db_add_command(state):
#     """Add sushi to db"""
#     async with state.proxy() as data:
#         cur.execute('SELECT count(*) FROM menu WHERE name=%s', (data['name'],))
#         res = cur.fetchone()[0]
#         values = tuple(data.values())
#         if res == 1:
#             cur.execute('UPDATE menu SET img=%s, name=%s, description=%s, price=%s WHERE name=%s',
#                         (values[0], values[1], values[2], values[3], data['name']))
#         else:
#             cur.execute('INSERT INTO menu VALUES (%s, %s, %s, %s)', tuple(data.values()))
#         db.commit()
#
#
# async def db_read(message):
#     cur.execute('SELECT * FROM menu')
#     for row in cur.fetchall():
#         await bot.send_photo(
#             message.from_user.id,
#             row[0],
#             f'{row[1]}\n'
#             f'Описание: {row[2]}\n'
#             f'Цена: {row[-1]}'
#         )
#
#
# async def db_delete_command(data):
#     """Delete item from db"""
#     cur.execute('''DELETE FROM menu WHERE name=%s''', (data,))
#     db.commit()
#
#
# async def db_read_all():
#     """Read all from db"""
#     cur.execute('''SELECT * FROM menu''')
#     return cur.fetchall()
