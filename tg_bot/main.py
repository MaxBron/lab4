import telebot
from pyowm import OWM
import requests
from telebot import types

TOKEN = '5606653542:AAHzpBel_JoCbPa2uOeQv9kZMF9EwJoC8NI'
# https://t.me/w4lun_bot
bot = telebot.TeleBot(TOKEN)
data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('курс валют')
    item2 = types.KeyboardButton('погода')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'курс валют':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('курс доллара', callback_data='USD')
            item2 = types.InlineKeyboardButton('курс евро', callback_data='EUR')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Выберите валюту', reply_markup=markup)
        if message.text == 'погода':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('Москва', callback_data='Moscow')
            item2 = types.InlineKeyboardButton('Нью Йорк', callback_data='New York')
            item3 = types.InlineKeyboardButton('Лондон', callback_data='London')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'Выберите город', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    owm = OWM('2eec61c6b82ecc52dd8349e111e747a7')
    mgr = owm.weather_manager()
    if call.message:
        if call.data == 'USD':
            bot.send_message(call.message.chat.id, 'курс доллара: {0}'
                             .format(data['Valute']['USD']['Value']))
        if call.data == 'EUR':
            bot.send_message(call.message.chat.id, 'курс евро: {0}'
                             .format(data['Valute']['EUR']['Value']))
        if call.data == 'Moscow':
            observation = mgr.weather_at_place('Moscow')
            w = observation.weather
            bot.send_message(call.message.chat.id, 'Температура в Москве: {0} °C, влажность: {1}, скорость ветра: {2}'
                             .format(w.temperature('celsius')['temp'], w.humidity, w.wind()['speed']))
        if call.data == 'New York':
            observation = mgr.weather_at_place('New York')
            w = observation.weather
            bot.send_message(call.message.chat.id, 'Температура в Нью Йорке: {0} °C, влажность: {1}, '
                                                   'скорость ветра: {2}'
                             .format(w.temperature('celsius')['temp'], w.humidity, w.wind()['speed']))
        if call.data == 'London':
            observation = mgr.weather_at_place('London')
            w = observation.weather
            bot.send_message(call.message.chat.id, 'Температура в Лондоне: {0} °C, влажность: {1}, скорость ветра: {2}'
                             .format(w.temperature('celsius')['temp'], w.humidity, w.wind()['speed']))


bot.polling(none_stop=True)
