import discord
from discord.ext import commands
from datetime import datetime

class about(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()

    @commands.command(name="about", aliases=["botinfo", "bot"])
    async def about(self, ctx):
        delta = datetime.utcnow() - self.start_time
        hours, rem = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)

        parts = []
        if days: parts.append(f"`{days}d`")
        if hours: parts.append(f"`{hours}h`")
        if minutes: parts.append(f"`{minutes}m`")
        parts.append(f"`{seconds}s`")

        embed = discord.Embed(
            title="m4-core",
            description="a modular discord bot built with discord.py",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=ctx.bot.user.display_avatar.url)
        embed.add_field(name="library", value="`discord.py`", inline=True)
        embed.add_field(name="servers", value=f"`{len(ctx.bot.guilds)}`", inline=True)
        embed.add_field(name="uptime", value=" ".join(parts), inline=True)
        embed.add_field(name="latency", value=f"`{round(ctx.bot.latency * 1000)}ms`", inline=True)
        embed.add_field(name="developer", value="immie & nyx", inline=True)
        embed.add_field(name="repository", value="[github.com/immie/m4-core](https://github.com/immie/m4-core)", inline=True)
        embed.set_footer(text="m4-core · built with discord.py")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(about(bot))
