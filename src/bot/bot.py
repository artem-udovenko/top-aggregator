import telebot
from telebot import types
from src.bot.token import TOKEN
from src.news.archive_manager import ArchiveManager
from src.news.news import News
from src.news.queue_manager import QueueManager
import src.parsing.parser
from src.bot.external import External
from src.smtp.smtp import Smtp
from src.smtp.user import User
from src.smtp.users_manager import UsersManager
from tools.tools import Tools

bot = telebot.TeleBot(TOKEN)

commands = [
    types.BotCommand('start', 'начать работу с ботом'),
    types.BotCommand('add_user', 'добавить пользователя'),
    types.BotCommand('remove_user', 'удалить пользователя'),
    types.BotCommand('users', 'посмотреть пользователей'),
    types.BotCommand('archive', 'посмотреть архив новостей'),
    types.BotCommand('publish', 'опубликовать новость'),
    types.BotCommand('parse', 'спарсить новости'),
    types.BotCommand('cancel', 'отмена'),
    types.BotCommand('exit', 'завершение работы')
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def start(message):
    print("SMTP...")
    server = Smtp.connect()
    print(server)
    print("OK")
    bot.send_message(message.chat.id, f'Добро пожаловать! smtp-сервер: {server.local_hostname}')
    bot.send_message(message.chat.id, '❗️Выберите команду ⏩')
    bot.send_message(message.chat.id, '/add_user - добавить пользователя 😐')
    bot.send_message(message.chat.id, '/remove_user - удалить пользователя 🫥')
    bot.send_message(message.chat.id, '/users - посмотреть пользователей 😐😐😐')
    bot.send_message(message.chat.id, '/archive - посмотреть архив новостей 📁')
    bot.send_message(message.chat.id, '/publish - опубликовать новость 📤')
    bot.send_message(message.chat.id, '/parse - спарсить новости ⌨️')
    bot.send_message(message.chat.id, '/exit - завершение работы 🛠')

@bot.message_handler(commands=['add_user'])
def add_user(message):
    bot.send_message(message.chat.id, 'Если данные отсутствуют, вводите \'-\'')
    bot.send_message(message.chat.id, 'Фамилия:')
    user = User()
    bot.register_next_step_handler(message, External.get_surname, bot, user)

@bot.message_handler(commands=['remove_user'])
def remove_user(message):
    bot.send_message(message.chat.id, 'id пользователя:')
    bot.register_next_step_handler(message, External.remove_user, bot)

@bot.message_handler(commands=['users'])
def users(message):
    Tools.display_users(message, bot, UsersManager.get_users())

@bot.message_handler(commands=['archive'])
def archive(message):
    news_list = ArchiveManager.get_archive()
    if news_list:
        bot.send_message(message.chat.id, 'Выберите id новости:')
        for (id, news) in news_list:
            bot.send_message(message.chat.id, f'*#{id}* {news.header} _{news.date}, {news.time}_',
                             parse_mode="Markdown")
        bot.register_next_step_handler(message, External.get_news_id, bot, news_list, False)
    else:
        bot.send_message(message.chat.id, 'Архив пуст')


@bot.message_handler(commands=['publish'])
def publish(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Опубликовать свою новость'))
    markup.add(types.KeyboardButton('Выбрать из очереди'))
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(commands=['parse'])
def parse(message):
    news_list = src.parsing.parser.parse(['https://tass.ru/'])
    bot.send_message(message.chat.id, f'Спарсено {len(news_list)} новостей')
    QueueManager.push_to_queue(news_list)

@bot.message_handler(commands=['cancel'])
def cancel(message):
    External.cancel(message, bot)

@bot.message_handler(commands=['exit'])
def exit(message):
    bot.send_message(message.chat.id, 'Завершение работы...')
    bot.send_message(message.chat.id, 'Для последующей работы используйте /start')
    Smtp.quit()

@bot.message_handler(content_types=['text'])
def handle_buttons(message):
    if message.text == 'Опубликовать свою новость':
        bot.send_message(message.chat.id, 'Заголовок новости:', reply_markup=types.ReplyKeyboardRemove())
        news = News()
        bot.register_next_step_handler(message, External.get_header, bot, news)
    elif message.text == 'Выбрать из очереди':
        news_list = QueueManager.get_queue()
        if news_list:
            bot.send_message(message.chat.id, 'Выберите id новости:', reply_markup=types.ReplyKeyboardRemove())
            for (id, news) in news_list:
                bot.send_message(message.chat.id, f'*#{id}* {news.header} _{news.date}, {news.time}_', parse_mode="Markdown")
            bot.register_next_step_handler(message, External.get_news_id, bot, news_list)
        else:
            bot.send_message(message.chat.id, 'Очередь новостей пуста. Попробуйте сделать /parse', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == '/cancel':
        cancel(message)

print("Queue... ", end="")
QueueManager.create_queue()
print("OK")
print("Archive... ", end="")
ArchiveManager.create_archive()
print("OK")
print("Users...", end="")
UsersManager.create_users()
print("OK")
print("Polling...")
bot.polling()