from handlers.custom_handlers.history import create_history_table
from main import bot


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, с чего начнем?\n'
                                      '/help - если нужна помощь.\n'
                                      '/email - проверка email-адреса.\n'
                                      '/phone - информация по номеру телефона.\n'
                                      '/ip_check - информация по ip-адресу.\n'
                                      '/history - последняя история запросов.\n')
    create_history_table()