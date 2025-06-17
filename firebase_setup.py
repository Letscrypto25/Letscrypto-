import os
import json
from firebase_admin import credentials, initialize_app, db

# Load the raw JSON from env (not base64 encoded)
firebase_creds_str = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_creds_str:
    raise Exception("FIREBASE_CREDENTIALS env var not found")

# Parse string into JSON dict
firebase_creds_dict = json.loads(firebase_creds_str)

# Initialize Firebase with dict (no file written)
cred = credentials.Certificate(firebase_creds_dict)
initialize_app(cred, {'databaseURL': 'https://your-firebase-db.firebaseio.com'})
