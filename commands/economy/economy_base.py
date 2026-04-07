import json
import os
import time

BANK_FILE = "bank.json"

def load_bank():
    if os.path.exists(BANK_FILE):
        try:
            with open(BANK_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_bank(data):
    with open(BANK_FILE, "w") as f:
        json.dump(data, f, indent=4)

def open_account(user_id, data):
    user_id = str(user_id)
    if user_id not in data:
        # Added tracking keys for persistent cooldowns
        data[user_id] = {
            "wallet": 100, 
            "bank": 0,
            "last_work": 0,
            "last_beg": 0,
            "last_daily": 0
        }
        save_bank(data)
    return data

def get_cooldown(user_id, data, key, seconds):
    """Returns remaining seconds if on cooldown, else 0."""
    current_time = time.time()
    last_time = data[str(user_id)].get(key, 0)
    remaining = (last_time + seconds) - current_time
    return max(0, round(remaining))
