import discord
import msgpack
import os
import time
from discord.ext import commands, tasks

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEPARTED_FILE = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "data", "departed.msgpack"))
PURGE_AFTER = 15 * 86400

def load_departed():
    if os.path.exists(DEPARTED_FILE):
        try:
            with open(DEPARTED_FILE, "rb") as f:
                data = msgpack.unpack(f, raw=False)
                return data if data else {}
        except (msgpack.UnpackException, OSError):
            pass
    return {}

def save_departed(data):
    tmp = DEPARTED_FILE + ".tmp"
    with open(tmp, "wb") as f:
        msgpack.pack(data, f, use_bin_type=True)
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

        bank_file = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "data", "bank.msgpack"))
        if not os.path.exists(bank_file):
            return

        with open(bank_file, "rb") as f:
            bank = msgpack.unpack(f, raw=False) or {}

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
            tmp = bank_file + ".tmp"
            with open(tmp, "wb") as f:
                msgpack.pack(bank, f, use_bin_type=True)
            os.replace(tmp, bank_file)

        if changed_departed:
            save_departed(departed)

    @purge_loop.before_loop
    async def before_purge_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AutoPurge(bot))