import requests
import json
from config_data.config import PHONE_API
from handlers.custom_handlers.history import add_history_entry
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from main import bot

processing_phone = False


@bot.message_handler(commands=['phone'])
def get_phone(message: Message):
    global processing_phone
    if processing_phone:
        bot.send_message(message.chat.id, 'Предыдущий запрос еще не обработан, пожалуйста, подождите.')
        return
    processing_phone = True
    bot.send_message(message.chat.id, 'Напишите номер телефона(Пример: +72223334455, +14152007986)')
    bot.register_next_step_handler(message, check_phone)


def check_phone(message: Message):
    global processing_phone
    phone = message.text.strip().lower()
    res_phone = requests.get(f'https://phonevalidation.abstractapi.com/v1/?api_key={PHONE_API}&phone={phone}')
    print(res_phone.text)
    data = json.loads(res_phone.text)
    if 'valid' in data and not data['valid']:
        response = 'Неправильно набран номер'
    elif 'country' in data:
        name = data['country']['name']
        carrier = data['carrier']
        response = f'Название страны: {name}\n' \
                   f'Название оператора: {carrier}'
    else:
        response = 'Не удалось получить информацию о номере телефона'

    processing_phone = False

    button = InlineKeyboardButton('Проверить еще один номер телефона', callback_data='check_phone')
    keyboard = [[button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent_message = bot.send_message(message.chat.id, response, reply_markup=reply_markup)
    add_history_entry(message.chat.id, message.text, sent_message.text)


@bot.callback_query_handler(func=lambda call: call.data == 'check_phone')
def callback_check_phone(call):
    bot.send_message(call.message.chat.id, 'Напишите номер телефона(Пример: +72223334455, +14152007986)')
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, check_phone)