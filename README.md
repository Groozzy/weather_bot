# Бот для Telegram, который предоставляет информацию о погоде

Данный модуль представляет собой бота для Telegram, который предоставляет информацию о погоде. Бот может принимать команды 'start' и 'help', а также сообщения с названиями городов для получения погоды.

## Требования

Необходимо создать файл .env в коренной директории проекта и указать там переменные BOT_TOKEN и YANDEX_API_KEY.

## Функции

- start: отвечает на команду 'start', отправляя приветственное сообщение.
- help\_callback: отвечает на команду 'help', отправляя сообщение с инструкцией.
- get\_weather: обрабатывает сообщения с названиями городов, получая информацию о погоде и отправляя её пользователю.
- request\_weather: делает запрос к API Yandex Weather для получения информации о погоде.
- save\_weather: сохраняет информацию о погоде в Redis.
- error\_callback: обрабатывает ошибки, возникающие при работе бота.
- main: запускает бота.

## Использование

Для запуска бота необходимо:
1. В терминале запустить контейнер Redis командой: `docker run -p 6379:6379 -it redis/redis-stack:latest`
2. Установить зависимости командой `pip install -r requirements.txt`
3. В модуле bot.py выполнить функцию main().

## Примечания

- Информация о погоде сохраняется в Redis на 1800 секунд (30 минут).
- Для работы с API Yandex Weather необходим ключ API.
- Для работы с Telegram Bot API необходим токен бота.