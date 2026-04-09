import discord
from discord.ext import commands
from datetime import datetime

class uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        delta = datetime.utcnow() - self.start_time
        hours, rem = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)

        parts = []
        if days: parts.append(f"`{days}d`")
        if hours: parts.append(f"`{hours}h`")
        if minutes: parts.append(f"`{minutes}m`")
        parts.append(f"`{seconds}s`")

        await ctx.send(embed=discord.Embed(
            title="⟳ uptime",
            description=" ".join(parts),
            color=discord.Color.blue()
        ))

async def setup(bot):
    await bot.add_cog(uptime(bot))
