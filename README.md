# API directory
Телеграм бот для поиска API для своих проектов.

## Доступные команды:
* **/search arg** - поиск по ключевому слову arg
* **/substr arg** - поиск по подстроке arg
* **/title arg** - поиск только по названию по подстроке arg
* **/random** - случайное API
* **/categories** - список доступных категорий
* **/category arg** - получить список API из категории arg
* **/idea** - получить идею для проекта и список API, которые могли бы помочь при реализации

## Использованные API:
* [Telegram bot API](https://core.telegram.org/bots/api)
* [Public API for Public APIs](https://github.com/davemachado/public-api)

## Web scrapping:
* [Hackathon project generator](https://www.wolframcloud.com/objects/microsites/ProjectGenerator/idea)

## Запуск:
После настроки виртуального окружения и загрузки модулей из requirements.txt необходимо ввести в терминал следующую команду:
```
python3 main.py BOT_TOKEN
```
Где BOT_TOKEN - токен бота, полученный у BotFather в телеграме
