import discord
from discord.ext import commands
import os
import sys
from helpers.admins_config import is_admin

class restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart")
    async def restart(self, ctx):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(description="⊘ unauthorized.", color=0xff4500))

        await ctx.send(embed=discord.Embed(
            title="⟳ restarting",
            description="restarting bot process...",
            color=discord.Color.blue()
        ))

        await self.bot.close()
        os.execv(sys.executable, [sys.executable, "main.py"])

async def setup(bot):
    await bot.add_cog(restart(bot))
