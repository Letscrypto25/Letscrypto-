from firebase_admin import db

def start(update, context):
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
