import discord
from discord.ext import commands
from datetime import timedelta
import re

def parse_duration(s: str) -> timedelta | None:
    match = re.fullmatch(r"(\d+)(s|m|h|d)", s.lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    return timedelta(seconds=value, minutes=0, hours=0, days=0) if unit == "s" else \
           timedelta(minutes=value) if unit == "m" else \
           timedelta(hours=value) if unit == "h" else \
           timedelta(days=value)

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="timeout", aliases=["mute"], description="timeout a member for a duration (e.g. 10m, 1h, 2d)")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason: str = "no reason provided"):
        if member == ctx.author:
            return await ctx.send(embed=discord.Embed(
                title="✖ invalid target", description="you can't timeout yourself.", color=discord.Color.red()
            ))
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(embed=discord.Embed(
                title="✖ insufficient hierarchy", description="you can't timeout someone with an equal or higher role.", color=discord.Color.red()
            ))

        delta = parse_duration(duration)
        if not delta:
            return await ctx.send(embed=discord.Embed(
                title="✖ invalid duration",
                description="use format: `10s`, `5m`, `2h`, `1d`",
                color=discord.Color.red()
            ))
        if delta.total_seconds() > 60 * 60 * 24 * 28:
            return await ctx.send(embed=discord.Embed(
                title="✖ too long", description="max timeout is 28 days.", color=discord.Color.red()
            ))

        await member.timeout(delta, reason=reason)

        try:
            await member.send(embed=discord.Embed(
                title=f"you've been timed out in {ctx.guild.name}",
                description=f"**duration:** {duration}\n**reason:** {reason}\n**by:** {ctx.author.name}",
                color=discord.Color.red()
            ))
        except discord.Forbidden:
            pass

        await ctx.send(embed=discord.Embed(
            title="√ timed out",
            description=f"timed out {member.mention} for **{duration}** · {reason}",
            color=discord.Color.green()
        ))

    @commands.command(name="untimeout", aliases=["unmute"], description="remove a timeout from a member")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member):
        if not member.is_timed_out():
            return await ctx.send(embed=discord.Embed(
                description="⊘ that member is not timed out.", color=0xff4500
            ))
        await member.timeout(None)
        await ctx.send(embed=discord.Embed(
            description=f"√ removed timeout from {member.mention}.", color=discord.Color.green()
        ))

async def setup(bot):
    await bot.add_cog(Timeout(bot))
