import requests

# Telegram bot token va chat_id ni o'zgartiring
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def send_telegram_message(text):
    """
    Telegramga matnli xabar yuboradi.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("Telegramga xabar yuborishda xatolik:", response.text)
        else:
            print("Telegramga xabar yuborildi.")
    except Exception as e:
        print("Telegramga xabar yuborishda xatolik:", e)

def send_telegram_photo(photo_path, caption=""):
    """
    Telegramga rasm va xabar yuboradi.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    files = {"photo": open(photo_path, "rb")}
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code != 200:
            print("Telegramga rasm yuborishda xatolik:", response.text)
        else:
            print("Telegramga rasm yuborildi.")
    except Exception as e:
        print("Telegramga rasm yuborishda xatolik:", e)
