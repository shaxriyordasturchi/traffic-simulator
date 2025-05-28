from telegram import Bot

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_CHAT_ID = "YOUR_ADMIN_CHAT_ID"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        print(f"[Telegram Error] {e}")
