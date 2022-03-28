
import telebot 
from youtubeTOKEN import TOKEN
from bs4 import BeautifulSoup
from time import sleep 

 
 
driver = BeautifulSoup
 
bot = telebot.TeleBot(TOKEN) 
 
@bot.message_handler(commands=['start']) 
def start(message): 
    bot.send_message(message.chat.id, "Привет") 
 
@bot.message_handler(commands=['search_videos']) 
def search_videos(message): 
    msg = bot.send_message(message.chat.id, "Введите текст, который вы хотите найти в YouTube") 
    bot.register_next_step_handler(msg, search) 
 
@bot.message_handler(commands=['search_channel']) 
def search_channel(message): 
    msg = bot.send_message(message.chat.id, "Введите YouTube канал") 
    bot.register_next_step_handler(msg, search_from_channel) 
 
 
 
@bot.message_handler(content_types=['text']) 
def text(message): 
    bot.send_message(message.chat.id, "Ты что-то хотел?") 
 
def search_from_channel(message): 
    bot.send_message(message.chat.id, "Начинаю поиск") 
    driver.get(message.text + "/videos") 
    videos = driver.find_elements_by_id("video-title") 
    for i in range(len(videos)): 
        bot.send_message(message.chat.id, videos[i].get_attribute('href')) 
        if i == 10: 
            break 
 
def search(message): 
    bot.send_message(message.chat.id, "Начинаю поиск") 
    video_href = "https://www.youtube.com/results?search_query=" + message.text 
    driver.get(video_href) 
    sleep(2) 
    videos = driver.find_elements_by_id("video-title") 
    for i in range(len(videos)): 
        bot.send_message(message.chat.id, videos[i].get_attribute('href')) 
        if i == 10: 
            break 
 
 
bot.polling()
