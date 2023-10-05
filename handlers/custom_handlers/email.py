import requests
import json
from config_data.config import EMAIL_API
from handlers.custom_handlers.history import add_history_entry
from main import bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

processing_email = False
response = False


@bot.message_handler(commands=['email'])
def get_email(message: Message):
    global processing_email
    if processing_email:
        bot.send_message(message.chat.id, 'Предыдущий запрос еще не обработан, пожалуйста, подождите.')
        return
    processing_email = True
    bot.send_message(message.chat.id, 'Напишите email-адрес(Формат: address @ domain . TLD)')
    bot.register_next_step_handler(message, check_email)


def check_email(message: Message):
    global processing_email, response
    email = message.text.strip()
    res_email = requests.get(f'https://emailvalidation.abstractapi.com/v1/?api_key={EMAIL_API}&email={email}')
    data_email = json.loads(res_email.text)
    quality_score = data_email['quality_score']
    if 'is_valid_format' in data_email and not data_email['is_valid_format']['value']:
        response = 'Неправильно написан email'
    elif float(quality_score) > 0.5:
        response = ('Имеет положительный балл по верссии портала "Abstract."\n'
                    f'Общий балл составляет - {quality_score}/1\n'
                    'Этому email-адресу можно доверять.')
    elif float(quality_score) < 0.5:
        response = ('Имеет отрицательный балл по верссии портала "Abstract."\n'
                    f'Общий балл составляет - {quality_score}/1\n'
                    'Этому email-адресу не стоит доверять.')
    processing_email = False

    button = InlineKeyboardButton('Проверить еще один email', callback_data='check_email')
    keyboard = [[button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent_message = bot.send_message(message.chat.id, response, reply_markup=reply_markup)
    add_history_entry(message.chat.id, message.text, sent_message.text)


@bot.callback_query_handler(func=lambda call: call.data == 'check_email')
def callback_check_email(call):
    bot.send_message(call.message.chat.id, 'Напишите email-адрес(Формат: address @ domain . TLD)')
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, check_email)