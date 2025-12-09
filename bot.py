import logging
from flask import Flask, request
from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8057481014:AAF_Q-jQgw46hi9FUOUhAAU5EtmpP4NOwW4"
WEBAPP_URL = "https://luminous-marigold-1576fd.netlify.app"
WEBHOOK_URL = "https://ozon-legends-bot.onrender.com"  # твой домен

# Flask сервер
app = Flask(__name__)

# Telegram бот
bot = Bot(token=TOKEN)

# Application PTB
application = Application.builder().token(TOKEN).build()

# ======= HANDLER /start =======
async def start(update: Update, context):
    logger.info("Получена команда /start")

    keyboard = [
        [KeyboardButton(
            text="🚀 Открыть OZON LEGENDS",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]

    markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        "Привет! Нажми кнопку, чтобы открыть игру:",
        reply_markup=markup
    )


application.add_handler(CommandHandler("start", start))


# ======= WEBHOOK =======
@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    application.update_queue.put_nowait(update)
    return "OK", 200


# Домашняя страница
@app.get("/")
def home():
    return "Bot is running!"


# Установка webhook
@app.get("/setwebhook")
def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)
    return "Webhook установлен!"
