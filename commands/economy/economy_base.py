import json
import os
import time

BANK_FILE = "bank.json"

def load_bank():
    if os.path.exists(BANK_FILE):
        try:
            with open(BANK_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except (json.JSONDecodeError, OSError):
            pass
    return {}

def save_bank(data):
    tmp = BANK_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp, BANK_FILE)

def open_account(user_id, data):
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "wallet": 100,
            "bank": 0,
            "last_work": 0,
            "last_beg": 0,
            "last_daily": 0,
            "last_crime": 0,
            "last_rob": 0,
        }
        save_bank(data)
    else:
        # Ensure existing accounts have all cooldown keys
        changed = False
        for key in ("last_work", "last_beg", "last_daily", "last_crime", "last_rob"):
            if key not in data[user_id]:
                data[user_id][key] = 0
                changed = True
        if changed:
            save_bank(data)
    return data

def get_cooldown(user_id, data, key, seconds):
    current_time = time.time()
    last_time = data[str(user_id)].get(key, 0)
    remaining = (last_time + seconds) - current_time
    return max(0, round(remaining))

def set_cooldown(user_id, data, key):
    data[str(user_id)][key] = time.time()
