import requests
import time
import os


class Bot:
    def __init__(self, token):
        self.token = token

    def search(self, text):
        pass

    def title(self, text):
        if len(text.split()) <= 1:
            return 1
        r = requests.get("https://api.publicapis.org/entries", params={"title": text[len("\\title "):]})
        print(r.json())

    def description(self):
        pass

    def random(self):
        pass

    def category(self):
        pass

    def categories(self):
        pass

    def help(self):
        pass

    def idea(self):
        pass

    def answer(self, update):
        user_id = update["message"]["from"]["id"]
        chat_id = update["message"]["chat"]["id"]
        message_id = update["message"]["message_id"]
        text = update["message"]["text"]
        command = text.split()[0].replace('/', '')
        if command == "title":
            self.title(text)

    def poll(self):
        offset = 0
        while True:
            r = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates",
                             params={"timeout": 5, "offset": offset})
            updates = r.json()["result"]
            if len(updates):
                for it in updates:
                    self.answer(it)
                offset = updates[-1]["update_id"] + 1


bot = Bot(os.getenv("TOKEN"))
bot.poll()
