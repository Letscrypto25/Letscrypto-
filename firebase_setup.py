import os
import json
import base64
from firebase_admin import credentials, initialize_app

# === 1. Get base64-encoded string from secrets ===
encoded_str = os.getenv("FIREBASE_CREDENTIALS_ENCRYPTED")

if not encoded_str:
    raise Exception("Missing FIREBASE_CREDENTIALS_ENCRYPTED secret")

# === 2. Decode from base64 ===
decoded_json = base64.b64decode(encoded_str).decode()

# === 3. Convert JSON string into dict ===
firebase_creds = json.loads(decoded_json)

# === 4. Initialize Firebase ===
initialize_app(
    credentials.Certificate(firebase_creds),
    {"databaseURL": "https://crypto-bot-3-default-rtdb.firebaseio.com/users/7521070576"}
)
