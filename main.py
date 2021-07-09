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
        arr = r.json()["entries"]

    @staticmethod
    def random():
        r = requests.get("https://api.publicapis.org/random")
        print(len(r.json()["entries"]), r.json()["entries"])
        arr = r.json()["entries"]

    @staticmethod
    def categories():
        r = requests.get("https://api.publicapis.org/categories")
        print(r.json())
        arr = r.json()

    @staticmethod
    def help():
        pass

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
            self.search(text, "title")
        elif command == "search":
            self.search(text, "description")
        elif command == "random":
            self.random()
        elif command == "categories":
            self.categories()
        elif command == "help" or command == "start":
            self.help()
        elif command == "category":
            self.search(text.split()[1], "category")


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
