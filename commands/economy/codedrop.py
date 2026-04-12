import discord
import random
import string
import time
from discord.ext import commands, tasks
from commands.economy.codes import load_codes, save_codes

DROP_CHANNEL_ID = 1491254006117564496
DROP_INTERVAL = 5
DROP_CHANCE = 0.25
CODE_EXPIRE_SECONDS = 600

def generate_code(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

class CodeDrop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drop_loop.start()
        self.cleanup_loop.start()

    def cog_unload(self):
        self.drop_loop.cancel()
        self.cleanup_loop.cancel()

    @tasks.loop(minutes=DROP_INTERVAL)
    async def drop_loop(self):
        # 1. Random Chance Check
        if random.random() > DROP_CHANCE:
            return

        channel = self.bot.get_channel(DROP_CHANNEL_ID)
        if not channel:
            return

        # 2. Generate Unique Code
        codes = load_codes()
        code = generate_code().upper()
        while code in codes:
            code = generate_code().upper()

        # 3. Setup Data with Expiry Timestamp
        amount = random.randint(250, 500)
        uses = random.randint(1, 5)
        expiry_timestamp = time.time() + CODE_EXPIRE_SECONDS

        codes[code] = {
            "amount": amount,
            "uses": uses,
            "redeemed_by": [],
            "expires_at": expiry_timestamp,
            "message_id": None # We'll update this in a second
        }

        # 4. Send Embed
        embed = discord.Embed(title="╼ code drop ╾", color=0xfee75c)
        embed.description = (
            f"code: `{code}`\n"
            f"amount: ⌬ {amount:,}\n"
            f"uses: {uses}\n\n"
            f"use `!redeem {code}` to claim!\n"
            f"expires <t:{int(expiry_timestamp)}:R>." # Discord dynamic timestamp
        )

        msg = await channel.send(embed=embed)
        codes[code]["message_id"] = msg.id
        save_codes(codes)

    @tasks.loop(seconds=30)
    async def cleanup_loop(self):
        """Separate loop to handle expiring messages and deleting data."""
        codes = load_codes()
        if not codes:
            return

        changed = False
        now = time.time()
        channel = self.bot.get_channel(DROP_CHANNEL_ID)

        # We use list(codes.keys()) so we can delete items while looping
        for code_str, data in list(codes.items()):
            if now > data.get("expires_at", 0):
                # Edit the message to show it expired
                if channel and data.get("message_id"):
                    try:
                        msg = await channel.fetch_message(data["message_id"])
                        expired_embed = discord.Embed(title="╼ code drop ╾", color=0x555555)
                        expired_embed.description = "⊘ this drop has expired."
                        await msg.edit(embed=expired_embed)
                    except:
                        pass # Message was likely deleted manually

                del codes[code_str]
                changed = True

        if changed:
            save_codes(codes)

    @drop_loop.before_loop
    async def before_drop_loop(self):
        await self.bot.wait_until_ready()

    @cleanup_loop.before_loop
    async def before_cleanup_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(CodeDrop(bot))
