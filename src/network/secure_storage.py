import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import Any, Dict
import logging

class SecureStorage:
    def __init__(self, mode: str):
        self.mode = mode
        self.base_path = os.path.join("config", "secure", mode)
        self._init_storage()
        self.key = self._generate_key()
        self.fernet = Fernet(self.key)
        
    def _init_storage(self):
        """Initialize storage directory with proper permissions"""
        try:
            os.makedirs(self.base_path, exist_ok=True)
            os.chmod(self.base_path, 0o700)  # Restrictive permissions
        except Exception as e:
            logging.error(f"Failed to initialize storage: {e}")
            raise
        
    def _generate_key(self) -> bytes:
        """Generate encryption key for current mode"""
        try:
            key_file = os.path.join(self.base_path, ".key")
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.mode.encode()))
            
            # Save key securely
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)
            
            return key
        except Exception as e:
            logging.error(f"Failed to generate key: {e}")
            raise
        
    def store(self, key: str, data: Any):
        """Securely store encrypted data"""
        try:
            path = os.path.join(self.base_path, f"{key}.enc")
            encrypted = self.fernet.encrypt(json.dumps(data).encode())
            
            # Atomic write
            temp_path = f"{path}.tmp"
            with open(temp_path, 'wb') as f:
                f.write(encrypted)
            os.chmod(temp_path, 0o600)
            os.replace(temp_path, path)
        except Exception as e:
            logging.error(f"Failed to store data: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
        
    def retrieve(self, key: str) -> Any:
        """Retrieve and decrypt data"""
        try:
            path = os.path.join(self.base_path, f"{key}.enc")
            if not os.path.exists(path):
                return None
                
            with open(path, 'rb') as f:
                encrypted = f.read()
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted)
        except FileNotFoundError:
            return None
        except Exception as e:
            logging.error(f"Failed to retrieve data: {e}")
            raise
            
    def secure_wipe(self):
        """Securely wipe all mode-specific data"""
        try:
            for file in os.listdir(self.base_path):
                path = os.path.join(self.base_path, file)
                # Don't delete the key file
                if file == ".key":
                    continue
                # Overwrite with random data
                with open(path, 'wb') as f:
                    f.write(os.urandom(1024))
                os.remove(path)
        except Exception as e:
            logging.error(f"Failed to wipe data: {e}")
            raise