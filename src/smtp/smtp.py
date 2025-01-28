import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.news.news import News
from src.smtp.personal_data import my_email, my_password
from src.smtp.users_manager import UsersManager

server = None

class Smtp:
    @staticmethod
    def connect():
        global server
        sender_email = my_email
        password = my_password
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            return server
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    @staticmethod
    def quit():
        global server
        if server:
            server.quit()
        server = None
        print(f"{server} quit")

    @staticmethod
    def send(news: News):
        global server
        sender_email = my_email
        password = my_password
        recipients = UsersManager.get_emails()
        subject = f"{news.header}"
        body = f"""
        <html>
          <body>
            <h4 style="color: blue;"><strong>{("", news.author)[bool(news.author)]}</strong><br><em>{("", news.date + ", ")[bool(news.date)]}{("", news.time)[bool(news.time)]}</em></h4>
            <p>{news.text}</p>
          </body>
        </html>
        """

        try:
            for recipient in recipients:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                text = msg.as_string()
                server.sendmail(sender_email, recipient, text)
                print(f"отправлено на {recipient}")
            print("завершено")

        except Exception as e:
            print(f"{e}")
