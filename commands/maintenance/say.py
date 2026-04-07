import discord
from discord.ext import commands

AUTHORIZED = {779653730978103306, 500683600614785025}

class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        if ctx.author.id not in AUTHORIZED:
            return

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(say(bot))
