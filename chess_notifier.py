import requests
import json
import time
import os
from telegram import Bot
from bs4 import BeautifulSoup
print(get_tournaments())
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔥 küçük güvenlik: bot başlamasın diye kontrol
if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN veya CHAT_ID eksik!")

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
    url = "https://izmir.tsf.org.tr/turnuvalar"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    tournaments = []

    for a in soup.find_all("a"):
        href = a.get("href")
        title = a.text.strip()

        if not href or not title:
            continue

        if "turnuva" in href or "etkinlik" in href:
            if not href.startswith("http"):
                href = "https://izmir.tsf.org.tr" + href

            tournaments.append({
                "id": href,
                "fullName": title,
                "url": href
            })

    return tournaments


def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)


def main():
    seen = load_seen()

    print("Bot started... TSF İzmir tracking active")

    while True:
        try:
            tournaments = get_tournaments()

            print("Found:", len(tournaments))

            for t in tournaments:
                tid = t["id"]

                if tid not in seen:
                    name = t["fullName"]
                    url = t["url"]

                    send_message(f"♟ Yeni Turnuva!\n{name}\n{url}")

                    seen.add(tid)
                    save_seen(seen)

        except Exception as e:
            print("Error:", e)

        time.sleep(60)


if __name__ == "__main__":
    main()
