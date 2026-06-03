import requests
import json
import time
import os
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

SEEN_FILE = "seen_tournaments.json"


def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def get_tournaments():
    url = "https://lichess.org/api/tournament"
    r = requests.get(url)
    return r.json().get("created", [])


def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)


def main():
    seen = load_seen()

    while True:
        tournaments = get_tournaments()

        for t in tournaments:
            tid = t["id"]

            if tid not in seen:
                name = t.get("fullName", "Chess Tournament")

                send_message(f"♟ Yeni turnuva:\n{name}\nhttps://lichess.org/tournament/{tid}")

                seen.add(tid)
                save_seen(seen)

        time.sleep(60)


if __name__ == "__main__":
    main()
