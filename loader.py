from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config


storage = StateMemoryStorage()
bot = TeleBot(token=config.bot, state_storage=storage)


