import requests
import time
import os


class Bot:
    def __init__(self, token):
        self.token = token

    @staticmethod
    def search(text, type):
        if len(text.split()) <= 1:
            return []
        r = requests.get("https://api.publicapis.org/entries",
                         params={type: text[len(f"{text.split()[0]} "):]})
        print(len(r.json()["entries"]), r.json()["entries"])
        arr = []
        for it in r.json()["entries"]:
            arr.append(f"{it['API']}\nОписание: {it['Description']}\nКатегория: {it['Category']}\nИнформация: {it['Link']}")
        return arr

    @staticmethod
    def random():
        r = requests.get("https://api.publicapis.org/random")
        print(len(r.json()["entries"]), r.json()["entries"])
        it = r.json()["entries"][0]
        return [f"{it['API']}\nОписание: {it['Description']}\nКатегория: {it['Category']}\nИнформация: {it['Link']}"]

    @staticmethod
    def categories():
        r = requests.get("https://api.publicapis.org/categories")
        print(r.json())
        text = ""
        for it in r.json():
            text += it + "\n"
        return [text]

    @staticmethod
    def help():
        return ["""Я бот для поиска API, доступны следующие команды:
/search arg - поиск по описанию по словам arg
/title arg - поиск по названию по подстроке arg
/substr arg - поиск по описанию по подстроке arg
/random - случайное API
/categories - список доступных категорий
/category arg - получить список API из категории arg
/idea - coming soon"""]

    def idea(self):
        pass

    def answer(self, update):
        user_id = update["message"]["from"]["id"]
        username = update["message"]["from"]["username"]
        chat_id = update["message"]["chat"]["id"]
        message_id = update["message"]["message_id"]
        text = update["message"]["text"]
        command = text.split()[0].replace('/', '')
        if command == "title":
            arr = self.search(text, "title")
        elif command == "search":
            arr = self.search(" " + text + " ", "description")
        elif command == "substr":
            arr = self.search(text, "description")
        elif command == "random":
            arr = self.random()
        elif command == "categories":
            arr = self.categories()
        elif command == "help" or command == "start":
            arr = self.help()
        elif command == "category":
            arr = self.search(text, "category")
        else:
            arr = ["Что-то пошло не так"]
        for it in arr:
            r = requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage",
                             params={"chat_id": chat_id, "text": it})

    def poll(self):
        offset = 0
        while True:
            r = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates",
                             params={"timeout": 5, "offset": offset})
            updates = r.json()["result"]
            print(updates)
            if len(updates):
                for it in updates:
                    self.answer(it)
                offset = updates[-1]["update_id"] + 1


bot = Bot(os.getenv("TOKEN"))
bot.poll()
