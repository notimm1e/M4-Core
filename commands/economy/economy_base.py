import json
import os
from discord.ext import commands

BANK_FILE = "bank.json"

def load_bank():
    """reads the bank.json file and returns the data as a dictionary."""
    if os.path.exists(BANK_FILE):
        try:
            with open(BANK_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_bank(data):
    """writes the current economy data back to the bank.json file."""
    with open(BANK_FILE, "w") as f:
        json.dump(data, f, indent=4)

def open_account(user_id, data):
    """ensures a user has an entry in the bank."""
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"wallet": 100, "bank": 0}
        save_bank(data)
    return data

async def setup(bot):
    """prevents extension loading errors."""
    pass
