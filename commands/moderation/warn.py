import discord
import msgpack
import os
from discord.ext import commands

WARNINGS_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "warnings.msgpack"))

def load_warnings():
    if os.path.exists(WARNINGS_FILE):
        try:
            with open(WARNINGS_FILE, "rb") as f:
                data = msgpack.unpackb(f.read(), raw=False)
                return data if data else {}
        except (msgpack.UnpackException, OSError):
            pass
    return {}

def save_warnings(data):
    os.makedirs(os.path.dirname(WARNINGS_FILE), exist_ok=True)
    tmp = WARNINGS_FILE + ".tmp"
    with open(tmp, "wb") as f:
        f.write(msgpack.packb(data, use_bin_type=True))
    os.replace(tmp, WARNINGS_FILE)
    
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

async def setup(bot):
    await bot.add_cog(warn(bot))
