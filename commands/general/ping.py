import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(
            title="⟳ pong!",
            description=f"`{round(self.bot.latency * 1000)}ms`",
            color=discord.Color.blue()
        ))

async def setup(bot):
    await bot.add_cog(ping(bot))