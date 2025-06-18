# firebase_setup.py
import os
import json
from cryptography.fernet import Fernet
from firebase_admin import credentials, initialize_app, db

def initialize_firebase():
    encrypted = os.getenv("FIREBASE_ENCRYPTED")
    secret_key = os.getenv("SECRET_KEY")

    if not encrypted or not secret_key:
        raise Exception("Missing Firebase secrets.")

    # Decrypt the credentials
    fernet = Fernet(secret_key.encode())
    decrypted_bytes = fernet.decrypt(encrypted.encode())

    # Load JSON and init Firebase
    creds_dict = json.loads(decrypted_bytes.decode())
    cred = credentials.Certificate(creds_dict)
    initialize_app(cred, {
        'databaseURL': 'https://console.firebase.google.com/u/0/project/crypto-bot-3/database/crypto-bot-3-default-rtdb/data/~2F'  # URL
    })
