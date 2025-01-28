from telebot import types
from src.smtp.smtp import Smtp, server
from src.smtp.users_manager import UsersManager
from src.news.queue_manager import QueueManager
from src.news.archive_manager import ArchiveManager
from tools.tools import Tools

class External:
    @staticmethod
    def cancel(message, bot):
        print(bot.set_message_reaction(message.chat.id, message.message_id, reaction=[types.ReactionTypeEmoji("❤️")]))
        bot.send_message(message.chat.id, 'Отмена', reply_markup=types.ReplyKeyboardRemove())

    @staticmethod
    def validate_news(message, bot, news):
        print(str(news))
        if server:
            Smtp.send(news)
            bot.send_message(message.chat.id, "❗️Опубликована новость❗️")
            Tools.format(message, bot, news)
            ArchiveManager.put_to_archive(news)
        else:
            bot.send_message(message.chat.id, "Ошибка, сервер не активен. Используйте /start")

    @staticmethod
    def validate_user(message, bot, user):
        print(str(user))
        bot.send_message(message.chat.id, "❗️Добавлен пользователь❗️")
        bot.send_message(message.chat.id, str(user))
        UsersManager.add_to_users(user)

    @staticmethod
    def get_header(message, bot, news):
        news.header = message.text
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        bot.send_message(message.chat.id, 'Текст новости:')
        bot.register_next_step_handler(message, External.get_text, bot, news)

    @staticmethod
    def get_text(message, bot, news):
        news.text = message.text
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        bot.send_message(message.chat.id, 'Автор новости:')
        bot.register_next_step_handler(message, External.get_author, bot, news)

    @staticmethod
    def get_author(message, bot, news):
        news.author = message.text
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        bot.send_message(message.chat.id, 'Дата новости:')
        bot.register_next_step_handler(message, External.get_date, bot, news)

    @staticmethod
    def get_date(message, bot, news):
        news.date = message.text
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        bot.send_message(message.chat.id, 'Время новости:')
        bot.register_next_step_handler(message, External.get_time, bot, news)

    @staticmethod
    def get_time(message, bot, news):
        news.time = message.text
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        External.validate_news(message, bot, news)

    @staticmethod
    def get_news_id(message, bot, news_list, publish=True):
        try:
            if message.text == '/cancel':
                External.cancel(message, bot)
                return
            id = int(message.text)
            for (i, news) in news_list:
                if i == id:
                    if publish:
                        External.validate_news(message, bot, news)
                        QueueManager.pop_queue(id)
                    else:
                        Tools.format(message, bot, news)
                    return
            bot.send_message(message.chat.id, 'id не найден.')
        except ValueError:
            bot.send_message(message.chat.id, 'Неправильный id новости.')

    @staticmethod
    def get_surname(message, bot, user):
        user.surname = (message.text, None)[message.text == '-']
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        bot.send_message(message.chat.id, 'Имя:')
        bot.register_next_step_handler(message, External.get_name, bot, user)

    @staticmethod
    def get_name(message, bot, user):
        user.name = (message.text, None)[message.text == '-']
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        bot.send_message(message.chat.id, 'Отчество:')
        bot.register_next_step_handler(message, External.get_patronymic, bot, user)

    @staticmethod
    def get_patronymic(message, bot, user):
        user.patronymic = (message.text, None)[message.text == '-']
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        bot.send_message(message.chat.id, 'email:')
        bot.register_next_step_handler(message, External.get_email, bot, user)

    @staticmethod
    def get_email(message, bot, user):
        user.email = (message.text, None)[message.text == '-']
        if message.text == '/cancel':
            External.cancel(message, bot)
            return
        External.validate_user(message, bot, user)

    @staticmethod
    def remove_user(message, bot):
        id = 0
        try:
            if message.text == '/cancel':
                External.cancel(message, bot)
                return
            id = int(message.text)
            UsersManager.remove_from_users(id)
        except ValueError:
            bot.send_message(message.chat.id, 'Неправильный id пользователя.')
        finally:
            print(id)
            bot.send_message(message.chat.id, f'Пользователь #{id} удален.')
            sticker_id = "CAACAgIAAxkBAAEL_Ntnl92QFsydw8Ozw1huRveMlr2XvgACVGcAAkOZwEjJ055Wuh42mDYE"
            bot.send_sticker(message.chat.id, sticker_id)
