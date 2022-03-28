from youtubeTOKEN import TOKEN  
import telebot
import youtube_dl  
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os  
import glob  
  
bot = telebot.TeleBot(TOKEN)  
@bot.message_handler(commands="start")  
def welcome(message):  
    text = """Вас приветствует бот-помощник Youtube.  
В мои функции входит установка видео или аудио с ютуб хостинга!  
Выберите функцию:"""  
    sti = open("ded.webp","rb")  
    markup = InlineKeyboardMarkup()  
    dwld_vidio_btn = InlineKeyboardButton("Скачать видео", callback_data="download_video")  
    dwld_audio_btn = InlineKeyboardButton("Скачать аудио", callback_data="download_audio")  
    markup.add(dwld_audio_btn,dwld_vidio_btn)  
    bot.send_sticker(message.chat.id,sti)  
    bot.send_message(message.chat.id,text,reply_markup=markup)  
      
      
  
  
@bot.callback_query_handler(func=lambda call: call.data == "download_video")  
def download_video_step1(call):  
    message = call.message  
    markup = InlineKeyboardMarkup()  
    exit_but=InlineKeyboardButton("Назад",callback_data="back_menu")  
    markup.add(exit_but)  
    text = """Отправьте ссылку, с которой вы хотите скачать видео: """  
    bot.edit_message_text(text,message.chat.id,message.id,reply_markup=markup)  
  
    bot.register_next_step_handler(message=message, callback=download_video_step2)  
def download_video_step2(message):  
    bot.send_message(message.chat.id,"Загрузка началась, это может занять долгое время из-за ограничений Youtube. Ожидайте")  
    url = message.text  
    print(url)  
    if str(url).startswith("https://www.youtube") or str(url).startswith("https://youtu") or str(url).startswith("https://m.youtu"):  
        with youtube_dl.YoutubeDL() as ydl:  
            ydl.download([url])  
        list_of_files = glob.glob("*")  
        last_file = max(list_of_files, key=os.path.getctime)  
        video = open(f"{last_file}","rb")  
        bot.send_video(message.chat.id,video)  
        bot.send_message(message.chat.id,"Спасибо за использование нашего бота!")  
    else:  
        bot.send_message(message.chat.id,"Данной ссылки не существует!")  
        welcome(message)  
      
      
      
@bot.callback_query_handler(func=lambda call: call.data == "download_audio")  
def download_audio_step1(call):  
    message = call.message  
    markup = InlineKeyboardMarkup()  
    exit_but=InlineKeyboardButton("Назад",callback_data="back_menu")  
    markup.add(exit_but)  
    text = """Отправьте ссылку, с которой вы хотите скачать аудио: """  
    bot.edit_message_text(text,message.chat.id,message.id,reply_markup=markup)  
      
    bot.register_next_step_handler(message=message, callback=download_audio_step2)  
def download_audio_step2(message):  
    bot.send_message(message.chat.id,"Загрузка началась, это может занять долгое время из-за ограничений Youtube. Ожидайте")  
    url = message.text  
    ydl_opts = {  
    'format': 'bestaudio/best',  
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',  
        'preferredcodec': 'mp3',  
        'preferredquality': '192',  
    }]  
}  
    if str(url).startswith("https://www.youtube") or str(url).startswith("https://youtu") or str(url).startswith("https://m.youtu"):  
        try:  
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:  
                ydl.download([url])  
        except:  
            list_of_files = glob.glob("*")  
            last_file = max(list_of_files, key=os.path.getctime)  
            audio = open(f"{last_file}","rb")  
            bot.send_audio(message.chat.id,audio)  
            bot.send_message(message.chat.id,"Спасибо за использование нашего бота!")  
    else:  
        bot.send_message(message.chat.id,"Данной ссылки не существует в ютуб")  
        welcome(message)  
      
  
@bot.callback_query_handler(func = lambda call: call.data == "back_menu")  
def back_menu(call):  
    message = call.message  
    bot.delete_message(message.chat.id,message.id)  
    welcome(message)  
  
  
bot.infinity_polling()