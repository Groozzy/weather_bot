import pytest
from unittest.mock import Mock

from bot import get_weather, help_callback, start, WEATHER_MESSAGE


def test_start(monkeypatch):
    update = Mock()
    context = Mock()
    update.message = Mock()
    update.message.reply_text = Mock()
    monkeypatch.setattr('bot.start', start)
    start(update, context)
    update.message.reply_text.assert_called_with('Привет! Я бот для Telegram.')


def test_help_callback(monkeypatch):
    update = Mock()
    context = Mock()
    update.message = Mock()
    update.message.reply_text = Mock()
    monkeypatch.setattr('bot.help_callback', help_callback)
    help_callback(update, context)
    update.message.reply_text.assert_called_with(
        'Напиши название города для получения погоды.')


def test_get_weather(monkeypatch):
    update = Mock()
    context = Mock()
    update.message = Mock()
    update.message.text = 'Москва'
    redis = Mock()
    redis.exists = Mock(return_value=True)
    redis.get = Mock(
        return_value='{"temp": 20, "pressure_mm": 760, "wind_speed": 5}')
    monkeypatch.setattr('bot.get_weather', get_weather)
    get_weather(update, context, redis)
    update.message.reply_text.assert_called_with(
        WEATHER_MESSAGE.format(temp=20, pressure_mm=760, wind_speed=5)
    )


