# from tracemalloc import start
# from webbrowser import get


from email import message
from pydoc import text
from aza_bot_id import TOKEN
import telebot

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["text"])
def check_text_message(message):
    status = int()
    try:
        status = config.current_users[message.chat.id][0]
    except Exception as er:
        status = 0
    if status == 0:
        bot.send_message(message.chat.id, 'Извините, я запутался. Давайте начнем сначала')
        first_step(message)
    elif status == 10:
        if message.text == 'Сделать заказ':
            Dialogs.order(message) ...6
bot.infinity_polling()


