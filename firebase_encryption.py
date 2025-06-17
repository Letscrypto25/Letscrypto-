from cryptography.fernet import Fernet
import base64

# Generate a Fernet key (only once)
fernet_key = Fernet.generate_key()
print("Save this secret key securely:", fernet_key.decode())

# Encrypt the credentials file
with open("firebase_key.json", "rb") as f:
    data = f.read()

fernet = Fernet(fernet_key)
encrypted_data = fernet.encrypt(data)

# Save encrypted string to set as secret
with open("firebase_key_encrypted.txt", "wb") as f:
    f.write(encrypted_data)
