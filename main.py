import requests
import os
import bs4
import nltk


class Bot:
    def __init__(self, token):
        self.token = token
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

    @staticmethod
    def idea_gen():
        r = requests.get("https://www.wolframcloud.com/objects/microsites/ProjectGenerator/idea")
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        return (soup.find(id="doimage")["src"][4:].replace("+", " ") + " "
                + soup.find(id="thingimage")["src"][7:].replace("+", " "))

    @staticmethod
    def search(text, type):
        print(text)
        if len(text.split()) == 0:
            return []
        r = requests.get("https://api.publicapis.org/entries",
                         params={type: text}, verify=False)
        # print(len(r.json()["entries"]), r.json()["entries"])
        arr = []
        print(r.json())
        if r.json()["count"] == 0:
            return []
        for it in r.json()["entries"]:
            arr.append(f"{it['API']}\nОписание: {it['Description']}\nКатегория: {it['Category']}\nИнформация: {it['Link']}")
        return arr

    @staticmethod
    def random():
        r = requests.get("https://api.publicapis.org/random", verify=False)
        print(len(r.json()["entries"]), r.json()["entries"])
        it = r.json()["entries"][0]
        return [f"{it['API']}\nОписание: {it['Description']}\nКатегория: {it['Category']}\nИнформация: {it['Link']}"]

    @staticmethod
    def categories():
        r = requests.get("https://api.publicapis.org/categories", verify=False)
        print(r.json())
        text = ""
        for it in r.json():
            text += it + "\n"
        return [text]

    @staticmethod
    def help():
        return ["""Я бот для поиска API, доступны следующие команды:
/search arg - поиск по описанию по слову arg
/title arg - поиск по названию по подстроке arg
/substr arg - поиск по описанию по подстроке arg
/random - случайное API
/categories - список доступных категорий
/category arg - получить список API из категории arg
/idea - получить идею для проекта и список API, которые могут помочь при реализации"""]

    @staticmethod
    def idea():
        idea = Bot.idea_gen()
        arr = [f"Idea for a project: {idea}", "Suggested APIs:"]
        tokenized = nltk.word_tokenize(idea)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if pos[:2] == "NN"]
        for noun in nouns:
            arr += Bot.search(" " + noun, "description")
            arr += Bot.search(noun + " ", "description")
        return arr

    def answer(self, update):
        user_id = update["message"]["from"]["id"]
        username = update["message"]["from"]["username"]
        chat_id = update["message"]["chat"]["id"]
        message_id = update["message"]["message_id"]
        text = update["message"]["text"]
        command = text.split()[0].replace('/', '')
        text = text[len(text.split()[0]) + 1:]
        if command == "title":
            arr = self.search(text, "title")
        elif command == "search":
            arr = self.search(text + " ", "description")
            arr += self.search(" " + text, "description")
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
        elif command == "idea":
            arr = self.idea()
        else:
            arr = ["Something went wrong"]
        if not arr:
            arr = ["Nothing was found"]
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
