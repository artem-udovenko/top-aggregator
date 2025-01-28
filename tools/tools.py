import csv
import os


class Tools:
    @staticmethod
    def format(message, bot, news):
        bot.send_message(message.chat.id, f"*{news.header}*\n{news.text}\n_{news.author}\n{news.date}, {news.time}_",
                         parse_mode="Markdown")

    @staticmethod
    def display_users(message, bot, users_list):
        filename = "users.csv"
        try:
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Фамилия", "Имя", "Отчество", "Email"])
                for user_id, user in users_list:
                    writer.writerow([
                        user_id or "",
                        user.surname or "",
                        user.name or "",
                        user.patronymic or "",
                        user.email or ""
                    ])
            with open(filename, "rb") as file:
                bot.send_document(message.chat.id, file)
        finally:
            if os.path.exists(filename):
                os.remove(filename)