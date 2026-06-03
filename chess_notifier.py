import requests
import json
import time
import os
from telegram import Bot
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("bot8842981825:AAGJ7W4lHLWNKrqIHW5HgQqFXGdW64Tk-MQ")
CHAT_ID = os.getenv("7643653960")

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


# 🔥 TSF İZMİR HTML SCRAPER
def get_tournaments():
    url = "https://izmir.tsf.org.tr/turnuvalar"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    tournaments = []

    for a in soup.find_all("a"):
        href = a.get("href")
        title = a.text.strip()

        if not href:
            continue

        # TSF turnuva linklerini filtrele
        if "turnuva" in href or "etkinlik" in href:
            if not href.startswith("http"):
                href = "https://izmir.tsf.org.tr" + href

            tid = href  # unique ID olarak URL kullanıyoruz

            if title:
                tournaments.append({
                    "id": tid,
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
        tournaments = get_tournaments()

        print("Found:", len(tournaments))

        for t in tournaments:
            tid = t["id"]

            if tid not in seen:
                name = t.get("fullName", "Chess Tournament")
                url = t.get("url")

                send_message(
                    f"♟ Yeni Turnuva!\n{name}\n{url}"
                )

                seen.add(tid)
                save_seen(seen)

        time.sleep(60)


if __name__ == "__main__":
    main()
