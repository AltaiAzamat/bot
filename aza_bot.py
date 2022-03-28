# from tracemalloc import start
# from webbrowser import get


# from email import message
# from pydoc import text
from aza_bot_id import TOKEN
import telebot

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["start"])
def check_text_message(message):
    text = "hello"
  
