from dataclasses import dataclass
from enum import Enum
import os
import json
import shutil
import logging
from typing import Optional, Dict, Any
from .secure_storage import SecureStorage

class NetworkMode(Enum):
    STANDARD = "standard"
    TOR = "tor"

@dataclass
class StandardIdentity:
    wallet_address: str
    username: str
    network_id: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "wallet_address": self.wallet_address,
            "username": self.username,
            "network_id": self.network_id
        }

@dataclass 
class TorIdentity:
    onion_address: str
    anonymous_id: str
    routing_id: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "onion_address": self.onion_address,
            "anonymous_id": self.anonymous_id,
            "routing_id": self.routing_id
        }

class NetworkManager:
    def __init__(self):
        self.current_mode = NetworkMode.STANDARD
        self.storage = SecureStorage(self.current_mode.value)
        self.identity = None
        self._load_config()

    def _load_config(self):
        try:
            stored_config = self.storage.retrieve("config")
            if stored_config:
                self.current_mode = NetworkMode(stored_config.get("mode", "standard"))
                identity_data = stored_config.get("identity")
                if identity_data:
                    if self.current_mode == NetworkMode.STANDARD:
                        self.identity = StandardIdentity(**identity_data)
                    else:
                        self.identity = TorIdentity(**identity_data)
        except Exception as e:
            logging.error(f"Error loading network config: {e}")

    def switch_mode(self, new_mode: NetworkMode):
        """Switch between Standard and Tor modes with secure cleanup"""
        if new_mode == self.current_mode:
            return

        # Securely clear current mode data
        self.storage.secure_wipe()
        self.identity = None
        
        # Initialize new mode
        self.current_mode = new_mode
        self.storage = SecureStorage(new_mode.value)
        
        # Save new configuration
        self._save_config()
        logging.info(f"Switched to {new_mode.value} mode")

    def _save_config(self):
        config = {
            "mode": self.current_mode.value,
            "identity": self.identity.to_dict() if self.identity else None
        }
        self.storage.store("config", config)

    def set_identity(self, identity: Union[StandardIdentity, TorIdentity]):
        """Set and store identity for current mode"""
        if isinstance(identity, StandardIdentity) and self.current_mode != NetworkMode.STANDARD:
            raise ValueError("Cannot set StandardIdentity in Tor mode")
        if isinstance(identity, TorIdentity) and self.current_mode != NetworkMode.TOR:
            raise ValueError("Cannot set TorIdentity in Standard mode")
            
        self.identity = identity
        self._save_config()

    def clear_data(self):
        """Securely clear all mode data"""
        self.storage.secure_wipe()
        self.identity = None
        logging.info("Network data cleared")