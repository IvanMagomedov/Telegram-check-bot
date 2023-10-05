from handlers.custom_handlers.history import add_history_entry
from main import bot
from telebot.types import Message


@bot.message_handler(commands=['help'])
def info_bot(message: Message):
    response = ('Привет! Я помощник этого телеграм-бота. Вот что ты можешь сделать:\n'
                '1. Запустить бота командой "/start".\n'
                '2. Получить информацию о доступных командах с помощью команды "/help".\n'
                '3. Проверить email-адрес на опечатки, наличие домена в списке провайдеров, на спам и наличие '
                'протоколов "MX" и "SMTP" с помощью команды "/email".\n'
                '4. Определить страну и оператора связи телефона по номеру с помощью команды "/phone".\n'
                '5. Получить информацию о конкретном IP-адресе с помощью команды "/ip_check".\n'
                '6. Просмотреть историю последних 10 запросов с помощью команды "/history".\n'
                '👋 Надеюсь, это поможет тебе использовать бота более эффективно!')

    sent_message = bot.send_message(message.chat.id, response)
    add_history_entry(message.chat.id, '/help', sent_message.text)