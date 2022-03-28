from turtle import back
from config import TOKEN, ADMIN_USERS_ID 
import telebot 
from menu import add_new_meal, get_by_category, get_categories 
from cart import add_cart_new_meal, get_user_cart 
from telebot.types import ( 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    ReplyKeyboardMarkup, 
    KeyboardButton 
) 
 
bot = telebot.TeleBot(TOKEN)
 
 
@bot.message_handler(commands=["start"]) 
def send_welcome_message(message): 
    print(message.from_user.id) 
    text = """ 
    Вас приветствует сервис быстрой доставки еды FastDelivery. 
    Мы принимаем заказы 7/24 по городу Бишкек. 
    Стоимость доставки 160сом. 
    """ 
    markup = InlineKeyboardMarkup() 
    markup.row_width = 1
    menu = InlineKeyboardButton("Меню", callback_data="menu") 
    feedback_button = InlineKeyboardButton("Написать отзыв", callback_data="feedback") 
    cart = InlineKeyboardButton('Моя корзина', callback_data='cart') 
    exit_button = InlineKeyboardButton("Выйти", callback_data="exit") 
    markup.add(menu, feedback_button,exit_button, cart) 
    bot.send_message(message.chat.id, text, reply_markup=markup, ) 
 
@bot.callback_query_handler(func=lambda call: call.data == "menu") 
def answer_menu_callback(call): 
    message = call.message 
    categories = get_categories() 
    if categories['status']: 
        markup = InlineKeyboardMarkup() 
        markup.row_width = 1 
        for category in categories['data']: 
            btn = InlineKeyboardButton(category, callback_data=category) 
            markup.add(btn) 
        bot.edit_message_text(chat_id=call.message.chat.id, text="Выберите категорию",message_id=call.message.message_id, reply_markup=markup) 
        return 
    else: 
        bot.edit_message_text(chat_id=call.message.chat.id, text="Нету меню",message_id=call.message.message_id, reply_markup=None) 
 
 
categories = get_categories()['data'] 
@bot.callback_query_handler(func=lambda call: call.data in categories) 
def answer_category_callback(call): 
    message = call.message 
    meals_data = get_by_category(call.data) 
    if meals_data['status']: 
        markup = InlineKeyboardMarkup() 
        markup.row_width = 1 
        for meal in meals_data['data']: 
            btn = InlineKeyboardButton( 
                f"{meal['name']}-{meal['price']}cом",  
                # 'food_'+  (будут называться вот так (food_Босо)) 
                callback_data=f"food_{meal['name']}_{meal['price']}" 
                ) 
            markup.add(btn) 
        bot.edit_message_text( 
            chat_id=message.chat.id, 
            text="Пожалуйста выберите блюдо:", 
            message_id = message.id, 
            reply_markup=markup, 
        ) 
    else: 
        bot.edit_message_text( 
            chat_id=message.chat.id, 
            text=meals_data['message'], 
            message_id = message.id, 
            reply_markup=None, 
        ) 
 
@bot.callback_query_handler(func=lambda call: str(call.data).startswith('back_')) 
def get_back_menu(call): 
    message = call.message 
    if call.data == 'back_category': 
        answer_menu_callback(call) 
    elif call.data == 'back_menu': 
        send_welcome_message(message) 
 
@bot.callback_query_handler(func=lambda call: str(call.data).startswith("food_") ) 
def add_meal(call): 
    message = call.message 
    user_id = call.from_user.id 
    print(user_id) 
    text = call.data.split('_') 
    meal_name = text[1] 
    meal_price = text[2] 
    meal_data = {'name':meal_name, 'price':meal_price} 
    r=add_cart_new_meal(meal_data=meal_data, user_id=user_id) 
    bot.edit_message_text( 
        chat_id=message.chat.id, 
        text=r['message'], 
        message_id=message.id, 
        reply_markup=None  
    ) 
    answer_menu_callback(call) 
 
 
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
 
@bot.callback_query_handler(func=lambda call: call.data=='cart') 
def get_cart(call): 
    message=call.message 
    user_id = call.from_user.id 
    text = "Блюда в вашей корзине \n" 
    total_sum = 0 
    user_cart = get_user_cart(user_id=user_id) 
    for i, meal in enumerate(user_cart["data"], start=1): 
        meal_text = f"{i}){meal['name']}-{meal['price']}сом\n" 
        # f"{i}){meal['name']}-{meal['price']}сом\n" - 1) Босо 120 сомов (вот так выходит) 
        text = text + meal_text 
        total_sum += int(meal['price']) 
    text = text + f"\nПолная сумма: {total_sum}" 
    markup = InlineKeyboardMarkup() 
    checkout_button = InlineKeyboardButton("Оформить заказ", callback_data="checkout") 
    back = InlineKeyboardButton("Назад", callback_data='back_menu') 
    markup.add(checkout_button, back) 
    print(user_cart) 
    bot.edit_message_text( 
        chat_id=message.chat.id, 
        message_id=message.id, 
        text= text, 
        reply_markup=markup 
    ) 
 
@bot.message_handler(content_types=["location"]) 
def handle_location(message): 
    print(f"lat: {message.location.latitude}") 
    print(f"lon: {message.location.longitude}") 
    bot.send_message(message.chat.id, "Ваша местоположение принято!") 
 
@bot.message_handler(commands= ['leava'])
def leave_bot(message):
    bot.send_message(chat_id= message.chat.id, text =" good by") 


# @bot.message_handler(commands=["admin"]) 
# def admin_message(message): 
#     print(message.from_user.id) 
#     if str(message.from_user.id) not in ADMIN_USERS_ID: 
#         bot.send_message(message.chat.id, text="Вы не являетесь админом!") 
#         return 
#     print(message) 
#     markup = InlineKeyboardMarkup() 
#     markup.row_width = 2 
#     add = InlineKeyboardButton("Добавить", callback_data="add_meal") 
#     delete = InlineKeyboardButton("Удалить", callback_data="delete_meal") 
#     markup.add(add,delete) 
#     bot.send_message(message.chat.id, text="Выберите команду", reply_markup=markup) 
 
 
@bot.callback_query_handler(func= lambda call: call.data=="add_meal") 
def add_callback_button(call): 
    message=call.message 
    national = InlineKeyboardButton("Национальная", callback_data="admin_national") 
    europe = InlineKeyboardButton("Европейская",callback_data="admin_europe") 
    fastfood = InlineKeyboardButton("FastFood", callback_data="admin_fastfood") 
    markup = InlineKeyboardMarkup() 
    markup.row_width = 2 
    markup.add(national, europe, fastfood) 
    bot.edit_message_text( 
        chat_id=message.chat.id,  
        text="Пожалуйста, выберите категорию.",  
        message_id=message.id, 
        reply_markup=markup 
    ) 
 
@bot.callback_query_handler(func= lambda call: call.data == "admin_national") 
def add_category_new_meal(call): 
    message = call.message 
    bot.edit_message_text( 
     chat_id=message.chat.id, 
     text="Напишите название блюда:",  
     message_id = message.id,  
     reply_markup=None 
    ) 
    bot.register_next_step_handler(message=message, callback=get_new_meal_name) 
 
def get_new_meal_name(message): 
    print(message.text) 
    bot.send_message(message.chat.id, text="Название блюда сохранено!") 
    bot.send_message(message.chat.id, text="Напишите цену блюда:") 
    bot.register_next_step_handler(message=message, callback=get_new_meal_price) 
 
def get_new_meal_price(message): 
    print(message.text) 
    bot.send_message(message.chat.id, text="Цена блюда сохранено!") 
 
 
 
 
bot.infinity_polling()
