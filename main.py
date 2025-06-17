# main.py
import base64
import os
import json
import requests
from flask import Flask, request
from firebase_admin import credentials, db, initialize_app
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from telegram.ext import MessageHandler, filters

# === Load Secrets ===
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set in Fly.io secrets
APP_URL = os.getenv("APP_URL")      # e.g. https://your-app.fly.dev

# === Firebase Setup ===
with open("firebase_key_encoded.txt", "r") as f:
    decoded = base64.b64decode(f.read())
    with open("firebase_key.json", "wb") as key_file:
        key_file.write(decoded)

cred = credentials.Certificate("firebase_key.json")
initialize_app(cred, {'databaseURL': 'https://your-firebase-db.firebaseio.com'})

# === Flask App ===
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# === Telegram Dispatcher ===
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# === Helper: Get Tier Based on Wallet ===
def get_tier(wallet_value):
    if wallet_value < 1000:
        return 1, 0.3
    elif wallet_value < 5000:
        return 2, 0.5
    elif wallet_value < 15000:
        return 3, 1.0
    elif wallet_value < 25000:
        return 4, 1.5
    return 5, 2.0

# === Command Handlers ===
def start(update: Update, context: CallbackContext):
    uid = str(update.effective_user.id)
    ref = db.reference(f"/users/{uid}")
    if not ref.get():
        ref.set({
            "lc_balance": 0,
            "wallet_value": 0,
            "tier": 1,
            "is_active": True
        })
    update.message.reply_text("👋 Welcome to LC Bot! You're now registered.")

def balance(update: Update, context: CallbackContext):
    uid = str(update.effective_user.id)
    user = db.reference(f"/users/{uid}").get()
    if user:
        tier, daily_cost = get_tier(user.get("wallet_value", 0))
        msg = f"💰 LC Balance: {user['lc_balance']:.2f} LC\n" \
              f"🏦 Wallet Value: R{user['wallet_value']}\n" \
              f"📊 Tier: {tier} | Daily Cost: {daily_cost} LC\n" \
              f"🔛 Active: {'Yes' if user.get('is_active') else 'No'}"
        update.message.reply_text(msg)
    else:
        update.message.reply_text("Please /start first.")

def buy_lc(update: Update, context: CallbackContext):
    uid = str(update.effective_user.id)
    try:
        amount = float(context.args[0])
        user_ref = db.reference(f"/users/{uid}")
        current = user_ref.child("lc_balance").get() or 0
        user_ref.child("lc_balance").set(current + amount)
        update.message.reply_text(f"✅ Topped up {amount} LC.")
    except:
        update.message.reply_text("❌ Use: /buy_lc 10")

# === Add Handlers ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("balance", balance))
dispatcher.add_handler(CommandHandler("buy_lc", buy_lc))

# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# === Set Webhook Route ===
@app.route("/", methods=["GET"])
def set_webhook():
    r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={APP_URL}/webhook")
    return r.text
