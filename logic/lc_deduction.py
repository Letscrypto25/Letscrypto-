from firebase_admin import db
from utils.tiers import get_tier
from datetime import datetime
import time
import threading

def deduct_daily_fees():
    print(f"[{datetime.now()}] Running daily LC deduction...")

    users_ref = db.reference("/users")
    users = users_ref.get()

    if not users:
        print("No users found.")
        return

    for uid, user in users.items():
        wallet = user.get("wallet_value", 0)
        balance = user.get("lc_balance", 0)

        tier, cost = get_tier(wallet)

        if balance >= cost:
            new_balance = round(balance - cost, 2)
            users_ref.child(uid).update({
                "lc_balance": new_balance,
                "is_active": True,
                "tier": tier
            })
            print(f"✅ User {uid}: Deducted {cost} LC. New balance = {new_balance}")
        else:
            users_ref.child(uid).update({"is_active": False})
            print(f"⛔ User {uid}: Insufficient LC. Marked inactive.")

def start_daily_loop():
    deduct_daily_fees()
    threading.Thread(target=lambda: loop_24h(), daemon=True).start()

def loop_24h():
    while True:
        time.sleep(86400)
        deduct_daily_fees()
