import json
import os

import geopy
import requests
from dotenv import load_dotenv
from redis import Redis
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv()

redis = Redis(host='localhost', port=6379, db=0)
geolocator = geopy.geocoders.Nominatim(user_agent="weather_bot")

BOT_TOKEN = os.getenv('BOT_TOKEN')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
URL = 'https://api.weather.yandex.ru/v2/forecast'
WEATHER_MESSAGE = """
Температура {temp} градусов по Цельсию,
Атмосферное давление {pressure_mm} мм рт. ст.,
Скорость ветра {wind_speed} м/с.
"""


def start(update, context):
    update.message.reply_text('Привет! Я бот для Telegram.')


def help_callback(update, context):
    update.message.reply_text('Напиши название города для получения погоды.')


def get_weather(update, context):
    city = update.message.text
    if redis.exists(city):
        weather = redis.get(city)
        update.message.reply_text(
            WEATHER_MESSAGE.format(**json.loads(weather)))
    else:
        location = geolocator.geocode(city)
        if not location:
            update.message.reply_text(f'Город "{city}" не найден.')
            return
        weather = request_weather(location.latitude, location.longitude)
        if not weather:
            update.message.reply_text(
                f'Информация о погоде для города "{city}" отсутствует.')
            return
        save_weather(city, json.dumps(weather, ensure_ascii=False))
        update.message.reply_text(WEATHER_MESSAGE.format(**weather))


def request_weather(latitude, longitude):
    return requests.get(
        url=URL,
        params={'lat': latitude, 'lon': longitude},
        headers={'X-Yandex-API-Key': YANDEX_API_KEY}
    ).json().get('fact')


def save_weather(city, weather, expire_time=1800):
    redis.set(city, weather)
    redis.expire(city, expire_time)


def error_callback(update, context):
    print('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_callback))
    dp.add_handler(MessageHandler(Filters.text, get_weather))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
