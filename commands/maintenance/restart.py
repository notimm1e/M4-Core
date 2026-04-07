import discord
from discord.ext import commands
import os
import sys

AUTHORIZED = {779653730978103306, 500683600614785025}

class restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart")
    async def restart(self, ctx):
        if ctx.author.id not in AUTHORIZED:
            return

        await ctx.send(embed=discord.Embed(
            title="⟳ restarting",
            description="restarting bot process...",
            color=discord.Color.blue()
        ))

        await self.bot.close()
        os.execv(sys.executable, [sys.executable, "main.py"])

async def setup(bot):
    await bot.add_cog(restart(bot))
