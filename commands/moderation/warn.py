import discord
import json
import os
from discord.ext import commands

WARNINGS_FILE = "warnings.json"

def load_warnings():
    if os.path.exists(WARNINGS_FILE):
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_warnings(data):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="warn")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "no reason provided"):
        if member == ctx.author:
            return await ctx.send(embed=discord.Embed(title="✖ invalid target", description="you can't warn yourself.", color=discord.Color.red()))
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(embed=discord.Embed(title="✖ insufficient hierarchy", description="you can't warn someone with an equal or higher role.", color=discord.Color.red()))

        data = load_warnings()
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in data:
            data[guild_id] = {}
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = []

        data[guild_id][user_id].append({
            "reason": reason,
            "by": str(ctx.author.id),
            "at": ctx.message.created_at.strftime("%b %d, %Y %H:%M")
        })
        save_warnings(data)

        count = len(data[guild_id][user_id])

        try:
            await member.send(embed=discord.Embed(
                title=f"⚠ warning in {ctx.guild.name}",
                description=f"**reason:** {reason}\n**warned by:** {ctx.author.name}\n**total warnings:** `{count}`",
                color=discord.Color.yellow()
            ))
        except discord.Forbidden:
            pass

        await ctx.send(embed=discord.Embed(
            title="√ warned",
            description=f"warned {member.mention} · **{reason}**\ntotal warnings: `{count}`",
            color=discord.Color.green()
        ))

    @commands.command(name="warnings", aliases=["warnlist"])
    @commands.has_permissions(moderate_members=True)
    async def warnings(self, ctx, member: discord.Member):
        data = load_warnings()
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        warns = data.get(guild_id, {}).get(user_id, [])

        if not warns:
            return await ctx.send(embed=discord.Embed(
                title="warnings",
                description=f"{member.mention} has no warnings.",
                color=discord.Color.blue()
            ))

        embed = discord.Embed(
            title=f"warnings · {member.name}",
            description=f"total: `{len(warns)}`",
            color=discord.Color.yellow()
        )

        for i, w in enumerate(warns, 1):
            embed.add_field(
                name=f"#{i} · {w['at']}",
                value=f"**reason:** {w['reason']}\n**by:** <@{w['by']}>",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="rmwarn", aliases=["delwarn", "removewarn"])
    @commands.has_permissions(moderate_members=True)
    async def rmwarn(self, ctx, member: discord.Member, index: int):
        data = load_warnings()
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        warns = data.get(guild_id, {}).get(user_id, [])

        if not warns:
            return await ctx.send(embed=discord.Embed(
                title="✖ no warnings",
                description=f"{member.mention} has no warnings.",
                color=discord.Color.red()
            ))

        if index < 1 or index > len(warns):
            return await ctx.send(embed=discord.Embed(
                title="✖ invalid index",
                description=f"provide a number between `1` and `{len(warns)}`.",
                color=discord.Color.red()
            ))

        removed = data[guild_id][user_id].pop(index - 1)
        save_warnings(data)

        await ctx.send(embed=discord.Embed(
            title="√ warning removed",
            description=f"removed warning `#{index}` from {member.mention}\n**reason was:** {removed['reason']}",
            color=discord.Color.green()
        ))

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="✖ missing permissions", description="you need `moderate members` to warn.", color=discord.Color.red()))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="✖ member not found", description="that member doesn't exist.", color=discord.Color.red()))

    @warnings.error
    async def warnings_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="✖ missing permissions", description="you need `moderate members` to view warnings.", color=discord.Color.red()))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="✖ member not found", description="that member doesn't exist.", color=discord.Color.red()))

    @rmwarn.error
    async def rmwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="✖ missing permissions", description="you need `moderate members` to remove warnings.", color=discord.Color.red()))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="✖ member not found", description="that member doesn't exist.", color=discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="✖ missing argument", description="usage: `!rmwarn @member <index>`\nuse `!warnings @member` to see indices.", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(warn(bot))