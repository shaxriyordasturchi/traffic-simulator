from telegram import Bot

TELEGRAM_BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"
ADMIN_CHAT_ID = " 7750409176"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        print(f"[Telegram Error] {e}")
