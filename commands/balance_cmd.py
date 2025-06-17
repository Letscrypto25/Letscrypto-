from firebase_admin import db
from utils.tiers import get_tier

def balance(update, context):
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
