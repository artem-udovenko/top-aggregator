# top-aggregator
### _pet project by [artem-udovenko](https://github.com/artem-udovenko)_
## Общее описание
Телеграм-бот TopAggregator позволяет в удобном формате пересылать и опубликовывать свои новости, которые поступят пользователям в рассылке.

## Использованные технологии
Проект полностью реализован на языке Python.
- telebot (синхронная библиотека для реализации бота)
- sqlite3 (взаимодействие с базами данных)
- requests + BeautifulSoup (парсинг)
- smtplib (почтовые сервера Gmail)
- встроенные библиотеки Python для работы с файлами (csv etc.)

## HowTo
1) Заполнить свои данные
- в [root.py](root.py)
```py
ROOT = "C:\\path\\to\\project"
```
- в [personal_data.py](src/smtp/personal_data.py)
```py
my_email = "your email"
my_password = "your app password"
```
- в [token.py](src/bot/token.py)
```py
TOKEN = "your token"
```
2) запустить [main.py](main.py)

