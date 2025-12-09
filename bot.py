import logging
from flask import Flask, request
from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler

# 🔴 ВСТАВЬ СВОЙ ТОКЕН
TOKEN = "8057481014:AAF_Q-jQgw46hi9FUOUhAAU5EtmpP4NOwW4"

# 🔴 ВСТАВЬ ССЫЛКУ НА WEBAPP
WEBAPP_URL = "https://luminous-marigold-1576fd.netlify.app"

# 🔴 ССЫЛКА НА СЕРВЕР RENDER (после деплоя заменить)
WEBHOOK_URL = "https://ozon-legends-bot.onrender.com"

# Flask
app = Flask(__name__)

# Telegram bot
bot = Bot(token=TOKEN)

# Application (замена Dispatcher)
application = Application.builder().token(TOKEN).build()

# ===== Команда /start =====

async def start(update: Update, context):
    keyboard = [
        [KeyboardButton(
            text="🚀 Открыть OZON LEGENDS",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Нажми кнопку, чтобы открыть игру:",
        reply_markup=markup
    )

application.add_handler(CommandHandler("start", start))

# ===== Обработка Webhook Telegram =====

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    application.update_queue.put_nowait(update)
    return "OK"


@app.get("/")
def home():
    return "Bot is running!"


@app.get("/setwebhook")
def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)
    return "Webhook установлен!"
