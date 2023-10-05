import os
from dotenv import load_dotenv


load_dotenv()

bot = os.getenv('TELEGRAM_TOKEN')
PHONE_API = os.getenv('PHONE_API_TOKEN')
EMAIL_API = os.getenv("EMAIL_API_TOKEN")
IP_API = os.getenv('IP_API_TOKEN')
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("email", "Проверка email-адреса"),
    ("phone", "Информация о номере телефона"),
    ("ip_check", "Информация о ip-адресе"),
    ("history", "История команд")
)
