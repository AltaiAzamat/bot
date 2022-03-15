from cgitb import text
from email import message
from tokenize import Token
import telebot
from youtubeTOKEN import TOKEN
from telebot.types import ( 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    ReplyKeyboardMarkup, 
    KeyboardButton 
) 

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    text = """Здарова нигер
Введи свою ссылку с ютуба"""

    bot.send_message(message.chat.id,text)

bot.infinity_polling()