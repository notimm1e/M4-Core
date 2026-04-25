import json
import os

BLACKLIST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "blacklist.json")

def load_blacklist() -> set:
    if not os.path.exists(BLACKLIST_FILE):
        return set()
    with open(BLACKLIST_FILE, "r") as f:
        return set(json.load(f))

def save_blacklist(blacklist: set):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(list(blacklist), f)

def is_blacklisted(user_id: int) -> bool:
    return user_id in load_blacklist()