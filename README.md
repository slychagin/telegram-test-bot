# telegram-test-bot
### Telegram bot for online testing

This bot allows you to conduct online testing in a telegram, which is very convenient.
If necessary, it can be quickly adapted to any online tests.
The bot is written in aiogram which makes it very fast.
The MongoDB database is connected as a data store (it turned out to be very convenient in this case).
To upload tests, a simple admin panel has been implemented with the ability to upload files in JSON format.
The bot is written so that you can add an unlimited number of tests with an unlimited number of questions and answers.

### Client part:
![client](https://github.com/slychagin/telegram-test-bot/blob/master/demo_gifs/client.gif)

### Admin part:
![admin](https://github.com/slychagin/telegram-test-bot/blob/master/demo_gifs/admin.gif)

### technologies used to create the bot:
- Python 3;
- aiogram;
- MongoDB.

### To run locally:
- `git clone https://github.com/slychagin/telegram-test-bot.git`;
- install all requiremets from `requirements.txt`;
- connect the bot to Telegram and get a token;
- also you need connect to MongoDB;
- in file `create_bot.py` isert your token;
- run file `telegram_bot.py`
