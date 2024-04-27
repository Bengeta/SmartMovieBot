from nis import match
from strings import *
import telebot
from telebot import types
from config import *

predict_data = {
    'metascore': None,
    'runtime': None,
    'revenue': None,
    'votes': None,
    'rank': None,
    
}

current_state = 'start'

BOT_TOKEN = TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    current_state = 'start'
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=BOT_PREDICT_MOVIE_RATING_LABEL, callback_data='predict_rating')
    markup.add(btn1)
    bot.reply_to(message, TELEGRAM_BOT_GRETTING, reply_markup = markup)
    

@bot.message_handler(commands=['predict_rating'])
def start_predict_asking_parametrs(message):
    current_state = 'predict_ask_metascore'
    bot.reply_to(message, BOT_ASKING_METASCORE)  
    
@bot.message_handler()
def start_predict_asking_parametrs(message):
    try:
        match current_state:
            case 'predict_ask_metascore':
                predict_data['metascore'] = float(message.text)
                current_state = 'predict_ask_votes'
                bot.reply_to(message, BOT_ASKING_VOTES)
            case 'predict_ask_votes':
                predict_data['votes'] = float(message.text)
                current_state = 'predict_ask_runtime'
                bot.reply_to(message, BOT_ASKING_RUNTIME)
            case 'predict_ask_runtime':
                predict_data['runtime'] = float(message.text)
                current_state = 'predict_ask_revenue'
                bot.reply_to(message, BOT_ASKING_REVENUE)
            case 'predict_ask_revenue':
                predict_data['revenue'] = float(message.text)
                current_state = 'predict_ask_rank'
                bot.reply_to(message, BOT_ASKING_RANK)
            case 'predict_ask_votes':
                predict_data['rank'] = float(message.text)
                current_state = 'predict_ask_year'
                bot.reply_to(message, BOT_ASKING_YEAR)
    except:
       bot.reply_to(message, BOT_BAD_INPUT) 
    
def start_bot():
    bot.polling(none_stop=True)
     