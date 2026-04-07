import discord
from discord.ext import commands

class UserUtility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", aliases=["ui", "whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        # If no member is mentioned, use the person who typed the command
        member = member or ctx.author
        
        # Formatting dates
        joined_at = member.joined_at.strftime("%b %d, %Y")
        created_at = member.created_at.strftime("%b %d, %Y")
        
        # Getting the list of roles (excluding @everyone)
        roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
        top_role = member.top_role.mention if roles else "No Roles"

        embed = discord.Embed(
            title=f"User Info - {member.name}",
            color=member.color
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        
        embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}" if member.discriminator != "0" else member.name, inline=True)
        embed.add_field(name="ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="Top Role", value=top_role, inline=True)
        
        embed.add_field(name="Joined Server", value=joined_at, inline=True)
        embed.add_field(name="Joined Discord", value=created_at, inline=True)
        
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserUtility(bot))