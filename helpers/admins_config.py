import yaml
import os

ADMINS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "admins.yaml")

def _resolve():
    return os.path.normpath(ADMINS_FILE)

def load_admins() -> set:
    path = _resolve()
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    return set(data.get("admins", []))

def save_admins(admins: set):
    path = _resolve()
    with open(path, "w") as f:
        yaml.dump({"admins": sorted(admins)}, f)

def is_admin(user_id: int) -> bool:
    return user_id in load_admins()
