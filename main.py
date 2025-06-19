import os
import threading
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

from firebase_setup import db  # Initializes Firebase
from commands.start_cmd import start
from commands.balance_cmd import balance
from commands.buy_lc_cmd import buy_lc
from logic.lc_deduction import start_daily_loop

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

# === Register Command Handlers ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("balance", balance))
dispatcher.add_handler(CommandHandler("buy_lc", buy_lc))

# === Webhook Endpoint ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# === Endpoint to set Telegram webhook ===
@app.route("/", methods=["GET"])
def set_webhook():
    r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={APP_URL}/webhook")
    return r.text

if __name__ == "__main__":
    # Run your long-running task in background thread
    thread = threading.Thread(target=start_daily_loop, daemon=True)
    thread.start()

    # Start Flask server
    app.run(host="0.0.0.0", port=8080)
