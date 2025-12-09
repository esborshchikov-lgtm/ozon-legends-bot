import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
import telegram

# 🔴 ВСТАВЬ СВОЙ ТОКЕН
TOKEN = "8057481014:AAF_Q-jQgw46hi9FUOUhAAU5EtmpP4NOwW4"

# 🔴 ВСТАВЬ ССЫЛКУ НА WEBAPP
WEBAPP_URL = "https://luminous-marigold-1576fd.netlify.app"

# 🔴 ССЫЛКА НА СЕРВЕР RENDER (после деплоя заменить)
WEBHOOK_URL = "https://ozon-legends-bot.onrender.com"

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [telegram.KeyboardButton(
            text="🚀 Открыть OZON LEGENDS",
            web_app=telegram.WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Нажми кнопку, чтобы открыть игру:",
        reply_markup=markup
    )

dispatcher.add_handler(CommandHandler("start", start))

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.get("/")
def home():
    return "Bot is running!"

@app.get("/setwebhook")
def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook установлен!"
