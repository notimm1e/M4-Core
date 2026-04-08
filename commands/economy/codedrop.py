import discord
import random
import string
import asyncio
from discord.ext import commands, tasks
from commands.economy.codes import load_codes, save_codes

DROP_CHANNEL_ID = 1491254006117564496
DROP_INTERVAL = 5
DROP_CHANCE = 0.15
CODE_EXPIRE_SECONDS = 600

def generate_code(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

class CodeDrop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drop_loop.start()

    def cog_unload(self):
        self.drop_loop.cancel()

    @tasks.loop(minutes=DROP_INTERVAL)
    async def drop_loop(self):
        if random.random() > DROP_CHANCE:
            return

        channel = self.bot.get_channel(DROP_CHANNEL_ID)
        if not channel:
            return

        codes = load_codes()

        code = generate_code()
        while code in codes:
            code = generate_code()

        amount = random.randint(250, 500)
        uses = random.randint(1, 5)

        codes[code] = {
            "amount": amount,
            "uses": uses,
            "redeemed_by": []
        }
        save_codes(codes)

        embed = discord.Embed(title="╼ code drop ╾", color=0xfee75c)
        embed.description = (
            f"code: `{code}`\n"
            f"amount: ⌬ {amount:,}\n"
            f"uses: {uses}\n\n"
            f"use `!redeem {code}` to claim!\n"
            f"expires in 10 minutes."
        )

        msg = await channel.send(embed=embed)

        await asyncio.sleep(CODE_EXPIRE_SECONDS)

        codes = load_codes()
        if code in codes:
            del codes[code]
            save_codes(codes)

        expired_embed = discord.Embed(title="╼ code drop ╾", color=0x555555)
        expired_embed.description = (
            f"~~code: `{code}`~~\n"
            f"~~amount: ⌬ {amount:,}~~\n"
            f"~~uses: {uses}~~\n\n"
            f"⊘ this drop has expired."
        )
        await msg.edit(embed=expired_embed)

    @drop_loop.before_loop
    async def before_drop_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(CodeDrop(bot))
