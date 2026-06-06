from cryptography.fernet import Fernet
import os
import json
import base64
from app.core.config import settings

class EncryptionManager:
    def __init__(self):
        # Primary key should be in ENV. If not, we use a fallback for dev, 
        # but in production, this MUST be provided.
        key = os.getenv("MASTER_ENCRYPTION_KEY")
        if not key:
            # We generate a key and warn. In a real deploy, the app would fail to start.
            key = Fernet.generate_key().decode()
            print("WARNING: MASTER_ENCRYPTION_KEY not found. Using a temporary session key.")
            
        self.cipher = Fernet(key.encode())

    def encrypt_data(self, data: dict) -> str:
        """Encrypts a dictionary to a secure string."""
        json_data = json.dumps(data).encode("utf-8")
        return self.cipher.encrypt(json_data).decode("utf-8")

    def decrypt_data(self, token: str) -> dict:
        """Decrypts a secure string back to a dictionary."""
        decrypted_bytes = self.cipher.decrypt(token.encode("utf-8"))
        return json.loads(decrypted_bytes.decode("utf-8"))

# Singleton for the app
encryption_manager = EncryptionManager()
