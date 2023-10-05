import sqlite3
from loader import bot


@bot.message_handler(commands=['history'])
def get_history(message):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message, response, timestamp FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10', (message.chat.id,))
    history_entries = cursor.fetchall()
    conn.close()

    if history_entries:
        response = "Последняя история запросов:\n"
        for entry in history_entries:
            response += f"Пользователь: {entry[0]}\nБот: {entry[1]}\nВремя: {entry[2]}\n\n"
    else:
        response = "У вас пока нет истории запросов."

    bot.send_message(message.chat.id, response)


def create_history_table():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_history_entry(user_id, message, response):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history (user_id, message, response) VALUES (?, ?, ?)', (user_id, message, response))
    conn.commit()
    conn.close()