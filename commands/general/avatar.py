import discord
from discord.ext import commands

class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s avatar", color=discord.Color.blue())
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f"requested by {ctx.author.name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(avatar(bot))
