
import telebot 
from botTOCEN import TOKEN 
from lib_sql.user_sql import UserSQL 
from lib_sql.authors_sql import AuthorsSQL 
from lib_sql.genre_sql import GenreSQL 
from lib_sql.books_sql import BookSQL 
from telebot import types 
import mysql.connector
bot = telebot.TeleBot(token=TOKEN) 
db = mysql.connector.connect(
   host="localhost",
    user="root",
    password="Abc12345!",
    db="chat",
    autocommit=True
)
cursor = db.cursor()


@bot.message_handler(commands=['start']) 
def send_wellcome_message(message): 
    text = """ 
    Добро пожаловать в бота нашей библиотеки имени Ч. Айтматова 
    """ 
    markup = types.InlineKeyboardMarkup() 
    my_cart = types.InlineKeyboardButton("Моя карточка", callback_data="my_cart") 
    genres = types.InlineKeyboardButton("Жанры", callback_data="genre") 
    search = types.InlineKeyboardButton("Поиск", callback_data="search") 
    markup.row_width = 1 
    markup.add(my_cart, genres, search) 
 
    bot.send_message(message.chat.id, text=text, reply_markup=markup) 
@bot.callback_query_handler(func= lambda call: call.data=='genre')
def send_all_genres(call):
    message = call.message
    genre_manger = GenreSQL(cursor)
    genres = genre_manger.get_all_genres()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2 
    for (id,name) in genres:
        button = types.InlineKeyboardButton(name, callback_data=f"genre_{id}")
        markup.add(button)
    bot.edit_message_text(
        chat_id=message.chat.id, 
        text="Выберите жанр",
        message_id=message.id,
        reply_markup=markup
    )
bot.infinity_polling()