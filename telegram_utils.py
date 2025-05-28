from telegram import Bot
from config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        print("Telegram xatosi:", e)
