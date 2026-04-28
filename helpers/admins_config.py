import yaml
import os

ADMINS_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "admins.yaml"))
DEFAULT_ADMINS = [779653730978103306, 500683600614785025]

def load_admins() -> set:
    if not os.path.exists(ADMINS_FILE):
        defaults = set(DEFAULT_ADMINS)
        save_admins(defaults)
        return defaults
    with open(ADMINS_FILE, "r") as f:
        data = yaml.safe_load(f) or {}
    return set(data.get("admins", []))

def save_admins(admins: set):
    with open(ADMINS_FILE, "w") as f:
        yaml.dump({"admins": sorted(admins)}, f)

def is_admin(user_id: int) -> bool:
    return user_id in load_admins()
