import motor.motor_asyncio


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


async def add_test_to_db(data):
    """Add new test to database"""
    await collection.insert_one(data)


async def db_count_test():
    """Count tests in db"""
    count_test = await collection.count_documents({})
    return count_test


async def db_read_all():
    """Read all data from db"""
    documents = [document async for document in collection.find({})]
    return documents


async def db_delete_command(test_name):
    """Delete test from db by test name"""
    await collection.delete_one({'test_name': test_name})
