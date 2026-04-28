import discord
from discord.ext import commands
from helpers.admins_config import is_admin

class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(description="⊘ unauthorized.", color=0xff4500))

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(say(bot))
