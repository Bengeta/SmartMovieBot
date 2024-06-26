from strings import *
import telebot
from telebot import types
from config import *
from models import *
from collections import defaultdict

user_data = defaultdict(lambda: {
    'predict_data': {
        'metascore': None,
        'runtime': None,
        'revenue': None,
        'votes': None,
        'rank': None,
        'main_actor_id': None,
        'main_genre_id': None,
        'director_id': None,
    },
    'current_state': 'start',
    'actors_page': 0,
    'genre_page': 0,
    'director_page': 0,
})

BOT_TOKEN = TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    clear_data(message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=BOT_PREDICT_MOVIE_RATING_LABEL, callback_data='predict_rating')
    markup.add(btn1)
    bot.reply_to(message, TELEGRAM_BOT_GRETTING, reply_markup = markup)
    

@bot.callback_query_handler(func=lambda call: call.data == 'predict_rating')
def start_predict_asking_parametrs(call):
    user_data[call.from_user.id]['current_state'] = 'predict_ask_metascore'
    bot.reply_to(call.message, BOT_ASKING_METASCORE)  

@bot.callback_query_handler(func=lambda call: call.data in ['ask_actor_next', 'ask_actor_prev'])
def ask_actor(call):
    markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton(text='->', callback_data='ask_actor_next')
    btn_prev = types.InlineKeyboardButton(text='<-', callback_data='ask_actor_prev')
    markup.add(btn_prev, btn_next)
    match call.data:
        case 'ask_actor_next':
            user_data[call.from_user.id]['actors_page'] += 1
        case 'ask_actor_prev':
            if user_data[call.from_user.id]['actors_page'] == 0:
                return
            user_data[call.from_user.id]['actors_page'] -= 1
            
    keys, values = get_items_from_storage(actors_storage, user_data[call.from_user.id]['actors_page'])
    message_text = make_message(keys, values, BOT_ASK_INPUT_ACTOR)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['ask_genre_next', 'ask_genre_prev'])
def ask_genre(call):
    markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton(text='->', callback_data='ask_genre_next')
    btn_prev = types.InlineKeyboardButton(text='<-', callback_data='ask_genre_prev')
    markup.add(btn_prev, btn_next)
    match call.data:
        case 'ask_genre_next':
            user_data[call.from_user.id]['genre_page'] += 1
        case 'ask_genre_prev':
            if user_data[call.from_user.id]['genre_page'] == 0:
                return
            user_data[call.from_user.id]['genre_page'] -= 1
            
    keys, values = get_items_from_storage(genres_storage, user_data[call.from_user.id]['genre_page'])
    message_text = make_message(keys, values, BOT_ASK_INPUT_MAIN_GENRE)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data in ['ask_director_next', 'ask_director_prev'])
def ask_director(call):
    markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton(text='->', callback_data='ask_director_next')
    btn_prev = types.InlineKeyboardButton(text='<-', callback_data='ask_director_prev')
    markup.add(btn_prev, btn_next)
    match call.data:
        case 'ask_director_next':
            user_data[call.from_user.id]['director_page'] += 1
        case 'ask_director_prev':
            if user_data[call.from_user.id]['director_page'] == 0:
                return
            user_data[call.from_user.id]['director_page'] -= 1
            
    keys, values = get_items_from_storage(directors_storage, user_data[call.from_user.id]['director_page'])
    message_text = make_message(keys, values, BOT_ASK_INPUT_DIRECTOR)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, reply_markup=markup)
    
@bot.message_handler()
def start_predict_asking_parametrs(message):
    try:
        match user_data[message.from_user.id]['current_state']:
            case 'predict_ask_metascore':
                user_data[message.from_user.id]['predict_data']['metascore'] = float(message.text)
                bot.reply_to(message, BOT_ASKING_VOTES)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_votes'

            case 'predict_ask_votes':
                user_data[message.from_user.id]['predict_data']['votes'] = float(message.text)
                bot.reply_to(message, BOT_ASKING_RUNTIME)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_runtime'

            case 'predict_ask_runtime':
                user_data[message.from_user.id]['predict_data']['runtime'] = float(message.text)
                bot.reply_to(message, BOT_ASKING_REVENUE)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_revenue'

            case 'predict_ask_revenue':
                user_data[message.from_user.id]['predict_data']['revenue'] = float(message.text)
                bot.reply_to(message, BOT_ASKING_RANK)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_rank'

            case 'predict_ask_rank':
                user_data[message.from_user.id]['predict_data']['rank'] = float(message.text)
                bot.reply_to(message, BOT_ASKING_YEAR)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_year'

            case 'predict_ask_year':
                # Corrected line: convert year to integer
                user_data[message.from_user.id]['predict_data']['year'] = int(message.text)
                markup = types.InlineKeyboardMarkup()
                btn_next = types.InlineKeyboardButton(text='->', callback_data='ask_actor_next')
                btn_prev = types.InlineKeyboardButton(text='<-', callback_data='ask_actor_prev')
                markup.add(btn_prev, btn_next)
                keys, values = get_items_from_storage(actors_storage, user_data[message.from_user.id]['actors_page'])
                message_text = make_message(keys, values, BOT_ASK_INPUT_ACTOR)
                bot.reply_to(message, message_text, reply_markup=markup)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_actor'

            case 'predict_ask_actor':
                user_data[message.from_user.id]['predict_data']['main_actor_id'] = float(message.text)
                ask_genre(message, BOT_ASK_INPUT_MAIN_GENRE)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_main_genre'
                
            case 'predict_ask_main_genre':
                user_data[message.from_user.id]['predict_data']['main_genre_id'] = float(message.text)
                markup = types.InlineKeyboardMarkup()
                btn_next = types.InlineKeyboardButton(text='->', callback_data='ask_director_next')
                btn_prev = types.InlineKeyboardButton(text='<-', callback_data='ask_director_prev')
                markup.add(btn_prev, btn_next)
                keys, values = get_items_from_storage(directors_storage, user_data[message.from_user.id]['director_page'])
                message_text = make_message(keys, values, BOT_ASK_INPUT_DIRECTOR)
                bot.reply_to(message, message_text, reply_markup=markup)
                user_data[message.from_user.id]['current_state'] = 'predict_ask_director'
                
            case 'predict_ask_director':
                user_data[message.from_user.id]['predict_data']['director_id'] = float(message.text)
                bot.reply_to(message, predict_rating(user_data[message.from_user.id]['predict_data']))
                user_data[message.from_user.id]['current_state'] = 'start'

    except:
        bot.reply_to(message, BOT_BAD_INPUT)



def start_bot():
    print("Bot started")
    bot.polling(none_stop=True)
     
     
def get_items_from_storage(storage, page):
    page_size = 10
    start_index = page * page_size
    if start_index >= len(storage):
      return [],[] 
    values = list(storage.values())[start_index : start_index + 10]
    keys = list(storage.keys())[start_index : start_index + 10]
    return keys, values

def clear_data(user_id):
    user_data[user_id] = {
    'predict_data': {
        'metascore': None,
        'runtime': None,
        'revenue': None,
        'votes': None,
        'rank': None,
        'main_actor_id': None,
        'main_genre_id': None,
        'director_id': None,
    },
    'current_state': 'start',
    'actors_page': 0,
    'genre_page': 0,
    'director_page': 0,
}
    
def make_message(keys, values, input):
    message = input + '\n\n'
    for i in range(len(keys)):
        message += (str(values[i]) + ': ' + str(keys[i]) + '\n')
    return message

def ask_genre(message, INPUT_STRING):
    markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton(text='->', callback_data='ask_genre_next')
    btn_prev = types.InlineKeyboardButton(text='<-', callback_data='ask_genre_prev')
    markup.add(btn_prev, btn_next)
    keys, values = get_items_from_storage(genres_storage, user_data[message.from_user.id]['genre_page'])
    message_text = make_message(keys, values, INPUT_STRING)
    bot.reply_to(message, message_text, reply_markup=markup)
        