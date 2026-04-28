import msgpack
import os

BLACKLIST_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "blacklist.msgpack"))

def load_blacklist() -> set:
    if not os.path.exists(BLACKLIST_FILE):
        return set()
    try:
        with open(BLACKLIST_FILE, "rb") as f:
            data = msgpack.unpackb(f.read(), raw=False)
            return set(data) if data else set()
    except (msgpack.UnpackException, OSError):
        return set()

def save_blacklist(blacklist: set):
    os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)
    tmp = BLACKLIST_FILE + ".tmp"
    with open(tmp, "wb") as f:
        f.write(msgpack.packb(list(blacklist), use_bin_type=True))
    os.replace(tmp, BLACKLIST_FILE)

def is_blacklisted(user_id: int) -> bool:
    return user_id in load_blacklist()
