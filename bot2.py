from webbrowser import get
from config import TOKEN
import telebot

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome_message(message):
    text = """
    Вас приветствует сервис быстрой доставки еды FastDelivery.
    Мы принимаем заказы 7/24 по городу Бишкек.
    Стоимость доставки 160сом.
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    menu = InlineKeyboardButton("Меню", callback_data="menu")
    feedback_button = InlineKeyboardButton("Написать отзыв", callback_data="feedback")
    exit_button = InlineKeyboardButton("Выйти", callback_data="exit")
    markup.add(menu, feedback_button,exit_button)
    bot.send_message(message.chat.id, text, reply_markup=markup, )

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def answer_menu_callback(call):
    message = call.message
    national = InlineKeyboardButton("Национальная", callback_data="national")
    europe = InlineKeyboardButton("Европейская",callback_data="europe")
    fastfood = InlineKeyboardButton("FastFood", callback_data="fastfood")
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(national, europe, fastfood)
    bot.edit_message_text(chat_id=call.message.chat.id, text="Выберите категорию",message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "feedback")
def answer_feedback_callback(call):
    message=call.message
    bot.edit_message_text(chat_id=message.chat.id, 
                        text="Напишите пожалуйста ваш отзыв", 
                        message_id=message.id, 
                        reply_markup=None
                        )
    bot.register_next_step_handler(message=message, callback=get_feedback)


def get_feedback(message):
    from datetime import datetime
    text = message.text
    user = message.from_user.username
    message_time = message.date
    message_time=datetime.fromtimestamp(message_time).strftime("%d-%m-%Y %H:%M:%S")
    with open("feedback.txt", "a", encoding="utf-8") as file:
            full_text = f"""
            Время создания отзыва: {message_time}
            Логин пользователя: {user}
            Текст: {text}
            """
            file.write(full_text)
    bot.send_message(chat_id=message.chat.id, text="Спасибо за ваш отзыв!")
        



@bot.message_handler(content_types=["location"])
def handle_location(message):
    print(f"lat: {message.location.latitude}")
    print(f"lon: {message.location.longitude}")
    bot.send_message(message.chat.id, "Ваша местоположение принято!")


bot.infinity_polling()