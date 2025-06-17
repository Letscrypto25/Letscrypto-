from firebase_admin import db

def buy_lc(update, context):
    uid = str(update.effective_user.id)
    try:
        amount = float(context.args[0])
        user_ref = db.reference(f"/users/{uid}")
        current = user_ref.child("lc_balance").get() or 0
        user_ref.child("lc_balance").set(current + amount)
        update.message.reply_text(f"✅ Topped up {amount} LC.")
    except:
        update.message.reply_text("❌ Use: /buy_lc 10")
