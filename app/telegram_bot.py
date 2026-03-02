import os
import requests
import time
from dotenv import load_dotenv
from database import update_setting, get_setting

# Load local .env (harmless on Railway)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is missing. Set it in .env locally or Railway Variables.")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

last_update_id = None


def send_message(chat_id, text):
    requests.post(
        f"{BASE_URL}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text
        }
    )


def handle_updates():
    global last_update_id

    params = {"timeout": 100}

    if last_update_id:
        params["offset"] = last_update_id + 1

    response = requests.get(f"{BASE_URL}/getUpdates", params=params)
    updates = response.json()

    if not updates.get("result"):
        return

    for update in updates["result"]:
        last_update_id = update["update_id"]

        message = update.get("message")
        if not message:
            continue

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # --- COMMANDS ---

        if text.startswith("/set_salary"):
            try:
                value = text.split(" ")[1]
                update_setting("min_salary", value)
                send_message(chat_id, f"✅ Minimum salary updated to {value} GEL")
            except:
                send_message(chat_id, "Usage: /set_salary 5000")

        elif text.startswith("/set_keywords"):
            value = text.replace("/set_keywords ", "")
            update_setting("keywords", value)
            send_message(chat_id, f"✅ Keywords updated to: {value}")

        elif text.startswith("/show_settings"):
            salary = get_setting("min_salary")
            keywords = get_setting("keywords")

            send_message(
                chat_id,
                f"📌 Current Settings:\n\n"
                f"💰 Min Salary: {salary} GEL\n"
                f"🔎 Keywords: {keywords}"
            )