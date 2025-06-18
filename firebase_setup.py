import os
import json
from firebase_admin import credentials, initialize_app
from cryptography.fernet import Fernet

# === 1. Get encrypted string and key from secrets ===
encrypted_str = os.getenv("FIREBASE_CREDENTIALS_ENCRYPTED")
fernet_key = os.getenv("SECRET_KEY")

if not encrypted_str or not fernet_key:
    raise Exception("Missing secrets")

# === 2. Decrypt ===
fernet = Fernet(fernet_key.encode())
decrypted_json = fernet.decrypt(encrypted_str.encode()).decode()

# === 3. Convert decrypted string into a dict ===
firebase_creds = json.loads(decrypted_json)

# === 4. Initialize Firebase ===
initialize_app(
    credentials.Certificate(firebase_creds),
    {"databaseURL": "https://console.firebase.google.com/u/0/project/crypto-bot-3/database/crypto-bot-3-default-rtdb/data/~2F"}
)
