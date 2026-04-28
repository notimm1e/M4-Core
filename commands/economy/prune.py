import discord
import msgpack
import os
import time
from discord.ext import commands, tasks
from helpers.economy_base import load_bank, save_bank

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEPARTED_FILE = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "data", "departed.msgpack"))
PURGE_AFTER = 15 * 86400

def load_departed():
    if os.path.exists(DEPARTED_FILE):
        try:
            with open(DEPARTED_FILE, "rb") as f:
                data = msgpack.unpackb(f.read(), raw=False)
                return data if data else {}
        except (msgpack.UnpackException, OSError):
            pass
    return {}

def save_departed(data):
    os.makedirs(os.path.dirname(DEPARTED_FILE), exist_ok=True)
    tmp = DEPARTED_FILE + ".tmp"
    with open(tmp, "wb") as f:
        f.write(msgpack.packb(data, use_bin_type=True))
    os.replace(tmp, DEPARTED_FILE)

class AutoPurge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.purge_loop.start()

    def cog_unload(self):
        self.purge_loop.cancel()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        departed = load_departed()
        departed[str(member.id)] = time.time()
        save_departed(departed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        departed = load_departed()
        uid = str(member.id)
        if uid in departed:
            del departed[uid]
            save_departed(departed)

    @tasks.loop(hours=24)
    async def purge_loop(self):
        departed = load_departed()
        if not departed:
            return

        bank = load_bank()

        now = time.time()
        changed_departed = False
        changed_bank = False

        for uid, left_at in list(departed.items()):
            if now - left_at >= PURGE_AFTER:
                if uid in bank:
                    del bank[uid]
                    changed_bank = True
                del departed[uid]
                changed_departed = True

        if changed_bank:
            save_bank(bank)

        if changed_departed:
            save_departed(departed)

    @purge_loop.before_loop
    async def before_purge_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AutoPurge(bot))