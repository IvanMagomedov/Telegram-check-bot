import requests
from config_data.config import IP_API
from main import bot
from handlers.custom_handlers.history import add_history_entry
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


@bot.message_handler(commands=['ip_check'])
def get_ip_info(message: Message):
    bot.send_message(message.chat.id, 'Введите IP-адрес')
    bot.register_next_step_handler(message, check_ip)


def check_ip(message: Message):
    ip_address = message.text.strip()
    response = requests.get(f'https://ipinfo.io/{ip_address}?token={IP_API}')
    if response.status_code == 200:
        data = response.json()
        message_text = (f"IP-адрес: {data['ip']}\n"
                        f"Город: {data['city']}\n"
                        f"Регион: {data['region']}\n"
                        f"Страна: {data['country']}\n"
                        f"Организация: {data['org']}\n"
                        f"Почтовый индекс: {data['postal']}\n"
                        f"Часовой пояс: {data['timezone']}")
        button = InlineKeyboardButton(text='Проверить еще раз', callback_data='repeat_ip_check')
        keyboard = [[button]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        sent_message = bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)
        add_history_entry(message.chat.id, message.text, sent_message.text)



@bot.callback_query_handler(func=lambda call: call.data == 'repeat_ip_check')
def callback_check_ip(call):
    bot.send_message(call.message.chat.id, 'Введите IP-адрес')
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, check_ip)