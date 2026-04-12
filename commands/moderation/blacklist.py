import discord
from discord.ext import commands
from commands.admins_config import is_admin
from commands.blacklist_config import load_blacklist, save_blacklist

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blacklist")
    async def add_blacklist(self, ctx, member: discord.Member):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(description="⊘ unauthorized.", color=0xff4500))

        if member.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(description="⊘ you can't blacklist yourself.", color=0xff4500))

        bl = load_blacklist()
        if member.id in bl:
            return await ctx.send(embed=discord.Embed(
                description=f"⊘ {member.display_name.lower()} is already blacklisted.",
                color=0xff4500
            ))

        bl.add(member.id)
        save_blacklist(bl)
        await ctx.send(embed=discord.Embed(
            description=f"√ {member.display_name.lower()} blacklisted.",
            color=0x57f287
        ))

    @commands.command(name="rmblacklist")
    async def remove_blacklist(self, ctx, member: discord.Member):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(description="⊘ unauthorized.", color=0xff4500))

        bl = load_blacklist()
        if member.id not in bl:
            return await ctx.send(embed=discord.Embed(
                description=f"⊘ {member.display_name.lower()} is not blacklisted.",
                color=0xff4500
            ))

        bl.discard(member.id)
        save_blacklist(bl)
        await ctx.send(embed=discord.Embed(
            description=f"√ {member.display_name.lower()} removed from blacklist.",
            color=0x57f287
        ))

    @add_blacklist.error
    @remove_blacklist.error
    async def blacklist_error(self, ctx, error):
        error.handled = True
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(description="⊘ member not found.", color=0xff4500))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(description="⊘ usage: `!blacklist @member` / `!rmblacklist @member`", color=0xff4500))

async def setup(bot):
    await bot.add_cog(Blacklist(bot))