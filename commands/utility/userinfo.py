import discord
import msgpack
import os
from discord.ext import commands
from helpers.economy_base import load_bank, open_account

EXCLUDED_ROLE = 1489622224267641043
WARNINGS_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "warnings.msgpack"))

def load_warnings():
    if os.path.exists(WARNINGS_FILE):
        try:
            with open(WARNINGS_FILE, "rb") as f:
                data = msgpack.unpack(f, raw=False)
                return data if data else {}
        except (msgpack.UnpackException, OSError):
            pass
    return {}

class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", aliases=["ui", "whois", "profile"])
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        joined_at = member.joined_at.strftime("%b %d, %Y")
        created_at = member.created_at.strftime("%b %d, %Y")

        roles = [
            role.mention for role in reversed(member.roles)
            if role != ctx.guild.default_role and role.id != EXCLUDED_ROLE
        ]
        top_role = member.top_role.mention if member.top_role != ctx.guild.default_role else "no roles"

        badges = []
        if member.bot:
            badges.append("bot")
        if member.guild_permissions.administrator:
            badges.append("admin")
        if member.premium_since:
            badges.append(f"boosting since {member.premium_since.strftime('%b %d, %Y')}")

        # economy
        data = load_bank()
        data = open_account(member.id, data)
        uid = str(member.id)
        wallet = data[uid]["wallet"]
        bank = data[uid]["bank"]
        debt = data[uid]["debt"]

        # warnings
        warnings = load_warnings()
        warn_count = len(warnings.get(str(ctx.guild.id), {}).get(uid, []))

        embed = discord.Embed(
            title=member.name,
            description=" · ".join(badges) if badges else None,
            color=member.color if member.color.value else 0x2b2d31
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="id", value=f"`{member.id}`", inline=True)
        embed.add_field(name="top role", value=top_role, inline=True)
        embed.add_field(name="nickname", value=member.nick or "none", inline=True)

        embed.add_field(name="joined server", value=joined_at, inline=True)
        embed.add_field(name="joined discord", value=created_at, inline=True)
        embed.add_field(name="warnings", value=f"`{warn_count}`", inline=True)

        embed.add_field(name="◈ wallet", value=f"⌬ {wallet:,}", inline=True)
        embed.add_field(name="◈ bank", value=f"⌬ {bank:,}", inline=True)
        if debt > 0:
            embed.add_field(name="⊘ debt", value=f"⌬ {debt:,}", inline=True)

        if roles:
            role_str = " ".join(roles)
            if len(role_str) > 1024:
                role_str = role_str[:1020] + "..."
            embed.add_field(name=f"roles [{len(roles)}]", value=role_str, inline=False)

        embed.set_footer(text=f"requested by {ctx.author.name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(userinfo(bot))