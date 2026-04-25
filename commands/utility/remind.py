import discord
import asyncio
import re
from discord.ext import commands
from datetime import timedelta

def parse_duration(s: str):
    match = re.fullmatch(r"(\d+)(s|m|h|d)", s.lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
    return value * seconds, f"{value}{unit}"

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remind", aliases=["reminder"], description="set a reminder (e.g. !remind 10m check plinko)")
    async def remind(self, ctx, duration: str, *, message: str):
        parsed = parse_duration(duration)
        if not parsed:
            return await ctx.send(embed=discord.Embed(
                description="✖ invalid duration. use `10s`, `5m`, `2h`, `1d`.",
                color=0xff4500
            ))

        seconds, label = parsed
        if seconds > 86400 * 7:
            return await ctx.send(embed=discord.Embed(
                description="✖ max reminder duration is 7 days.",
                color=0xff4500
            ))

        await ctx.send(embed=discord.Embed(
            description=f"√ i'll remind you about **{message}** in **{label}**.",
            color=0x2b2d31
        ))

        await asyncio.sleep(seconds)

        try:
            await ctx.author.send(embed=discord.Embed(
                title="⏱ reminder",
                description=message,
                color=0x5865f2
            ).set_footer(text=f"set in #{ctx.channel.name} · {ctx.guild.name}"))
        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                description=f"{ctx.author.mention} ⏱ reminder: **{message}**",
                color=0x5865f2
            ))

async def setup(bot):
    await bot.add_cog(Remind(bot))