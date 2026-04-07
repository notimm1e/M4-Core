import discord
from discord.ext import commands

class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", aliases=["ui", "whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        joined_at = member.joined_at.strftime("%b %d, %Y")
        created_at = member.created_at.strftime("%b %d, %Y")

        roles = [role.mention for role in reversed(member.roles) if role != ctx.guild.default_role]
        top_role = member.top_role.mention if roles else "no roles"

        badges = []
        if member.bot:
            badges.append("bot")
        if member.guild_permissions.administrator:
            badges.append("admin")
        if member.premium_since:
            badges.append(f"boosting since {member.premium_since.strftime('%b %d, %Y')}")

        embed = discord.Embed(
            title=member.name,
            description=" · ".join(badges) if badges else None,
            color=member.color if member.color.value else discord.Color.blue()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="id", value=f"`{member.id}`", inline=True)
        embed.add_field(name="top role", value=top_role, inline=True)
        embed.add_field(name="nickname", value=member.nick or "none", inline=True)

        embed.add_field(name="joined server", value=joined_at, inline=True)
        embed.add_field(name="joined discord", value=created_at, inline=True)

        if roles:
            role_str = " ".join(roles)
            if len(role_str) > 1024:
                role_str = role_str[:1020] + "..."
            embed.add_field(name=f"roles [{len(roles)}]", value=role_str, inline=False)

        embed.set_footer(text=f"requested by {ctx.author.name}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(userinfo(bot))