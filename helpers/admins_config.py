import yaml
import os

ADMINS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "admins.yaml")

def _resolve():
    return os.path.normpath(ADMINS_FILE)

_cache: set | None = None

def load_admins() -> set:
    global _cache
    if _cache is not None:
        return _cache
    path = _resolve()
    if not os.path.exists(path):
        _cache = set()
        return _cache
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    _cache = set(data.get("admins", []))
    return _cache

def save_admins(admins: set):
    global _cache
    _cache = admins
    path = _resolve()
    with open(path, "w") as f:
        yaml.dump({"admins": sorted(admins)}, f)

def is_admin(user_id: int) -> bool:
    return user_id in load_admins()