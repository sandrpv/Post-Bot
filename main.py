import requests
import telebot
import time
import threading
from telebot import types

urlcatfact = "https://catfact.ninja/fact"
urlcatimg = "https://cataas.com/cat?json=true"
urldogfact = "https://dog-api.kinduff.com/api/facts"
urldogimg = "https://api.thedogapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1"

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

CatChanel = 'YOUR_CHANEL_ID0'
DogChanel = 'YOUR_CHANEL_ID1'

secur = False
checkcat = False
checkdog = False

timesleep = 3600


def send_cat_facts():
    global checkcat
    global CatChanel
    global timesleep
    while checkcat:
        try:
            responsecatf = requests.get(urlcatfact)
            responsecati = requests.get(urlcatimg)

            datacatf = responsecatf.json()
            datacati = responsecati.json()

            bot.send_photo(CatChanel,
                           datacati["url"],
                           caption=f'Random fact: <span class="tg-spoiler">' +
                           datacatf["fact"] + '</span>',
                           parse_mode='html')
        except Exception as e:
            bot.send_message(CatChanel, f"Error: {str(e)}")

        time.sleep(timesleep)


def send_dog_facts():
    global checkdog
    global DogChanel
    global timesleep
    while checkdog:
        try:
            responsedogf = requests.get(urldogfact)
            responsedogi = requests.get(urldogimg)

            datadogf = responsedogf.json()
            facts1 = datadogf.get('facts', ["No fact found"])
            datadogi = responsedogi.json()

            bot.send_photo(DogChanel,
                           datadogi[0]["url"],
                           caption=f'Random fact: <span class="tg-spoiler">' +
                           ''.join(facts1) + '</span>',
                           parse_mode='html')
        except Exception as e:
            bot.send_message(DogChanel, f"Error: {str(e)}")

        time.sleep(timesleep)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('welcome.webm', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(
        message.chat.id,
        f"Hi {message.from_user.first_name}!\nI'm <b>{bot.get_me().first_name}</b>, bot - admin-panel",
        parse_mode='html')


@bot.message_handler(content_types=['text'])
def lalala(message):
    global checkcat, checkdog, secur

    if secur:
        if message.text == '🐱':
            if not checkcat:
                checkcat = True
                bot.send_message(message.chat.id, "Cat facts started!")
                threading.Thread(target=send_cat_facts, daemon=True).start()
            else:
                checkcat = False
                bot.send_message(message.chat.id, "Cat facts stopped!")

        elif message.text == '🐶':
            if not checkdog:
                checkdog = True
                bot.send_message(message.chat.id, "Dog facts started!")
                threading.Thread(target=send_dog_facts, daemon=True).start()
            else:
                checkdog = False
                bot.send_message(message.chat.id, "Dog facts stopped!")

    if message.text == "123":
        secur = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("🐱")
        item2 = types.KeyboardButton("🐶")
        markup.add(item1, item2)
        bot.send_message(message.chat.id,
                         "Access approved",
                         reply_markup=markup)

bot.polling(none_stop=True)
