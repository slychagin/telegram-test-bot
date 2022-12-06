from random import choice

wrong_answer = [
    'Неверно\U0001F622',
    'Да нет же\U0001F61E',
    'Ну как же так?\U0001F928',
    'Тебе бы подучиться немного\U0001F615',
    'Возьми себя в руки!\U0001F629',
    'Ну вот еще\U0001F61E',
    'Да что ж такое?\U0001F62D',
    'Неправильно\U0001F612',
    'Совсем не то\U0001F641',
    'Истина где-то рядом\U0001F625']

right_answer = [
    'Отлично!\U0001F600',
    'Превосходно!\U0001F603',
    'В точку!\U0001F3AF',
    'Супер! Все верно\U0001F44D',
    'Ума тебе не занимать\U0001F60F',
    'Так держать!\U0001F44C',
    'Гениально\U0001F60E',
    'Я в тебе не сомневался\U0001F609',
    'Замечательно\U0001F929',
    'Да ты умён\U0001F60E']

congratulations = [
    'Твоей гениальности позавидовал бы сам Эйнштейн!\U0001F913',
    'Да у нас здесь новый гений!\U0001F60E',
    'Уровень твоей гениальности зашкаливает!\U0001F60E'
]


def get_wrong_answer():
    """
    If the user answers incorrectly,
    then the bot sends a disapproving answer
    """
    return f'\U0000274C {choice(wrong_answer)}'


def get_right_answer():
    """
    If the user answers correctly,
    then the bot sends an approving message
    """
    return f'\U00002705 {choice(right_answer)}'


def get_result_congrat(right_answers, questions_amount):
    """Depending on the number of correctly answered questions,
    the bot sends an appropriate message
    """
    right_answer_percent = right_answers / questions_amount

    if right_answer_percent < 0.1:
        return 'Даа, не ожидал я от тебя такого\U0001F622'
    if right_answer_percent < 0.25:
        return 'Похоже у кого-то сегодня день не задался? \U0001F614'
    if right_answer_percent < 0.5:
        return 'Не так плохо!\nНо могло быть и лучше\U0001F60F'
    if right_answer_percent < 0.75:
        return 'Отлично!\U0001F600\nДа ты практически гений\U0001F609'
    if right_answer_percent < 0.9:
        return 'Еще немного и ты достигнешь полного просветления\U0001F60C'
    if right_answer_percent < 1:
        return 'Отлично!\nПрактически 100% правильных ответов!\nТак держать\U0001F60C'
    if right_answer_percent == 1:
        return choice(congratulations)
