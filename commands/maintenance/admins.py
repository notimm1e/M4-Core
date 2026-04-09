import discord
from discord.ext import commands
from commands.admins_config import load_admins, save_admins, is_admin

class Admins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="admin")
    async def add_admin(self, ctx, member: discord.Member):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(description="⊘ unauthorized.", color=0xff4500))

        admins = load_admins()
        if member.id in admins:
            return await ctx.send(embed=discord.Embed(
                description=f"⊘ {member.display_name.lower()} is already an admin.",
                color=0xff4500
            ))

        admins.add(member.id)
        save_admins(admins)
        await ctx.send(embed=discord.Embed(
            description=f"√ {member.display_name.lower()} added to admins.",
            color=0x57f287
        ))

    @commands.command(name="rmadmin")
    async def remove_admin(self, ctx, member: discord.Member):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(description="⊘ unauthorized.", color=0xff4500))

        admins = load_admins()
        if member.id not in admins:
            return await ctx.send(embed=discord.Embed(
                description=f"⊘ {member.display_name.lower()} is not an admin.",
                color=0xff4500
            ))

        if member.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(
                description="⊘ you can't remove yourself.",
                color=0xff4500
            ))

        admins.discard(member.id)
        save_admins(admins)
        await ctx.send(embed=discord.Embed(
            description=f"√ {member.display_name.lower()} removed from admins.",
            color=0x57f287
        ))

    @commands.command(name="adminlist")
    async def admin_list(self, ctx):
        admins = load_admins()
        if not admins:
            return await ctx.send(embed=discord.Embed(description="⊘ no admins configured.", color=0xff4500))

        lines = []
        for uid in sorted(admins):
            member = ctx.guild.get_member(uid)
            lines.append(f"◈ {member.display_name.lower()} (`{uid}`)" if member else f"◈ `{uid}` *(not in server)*")

        await ctx.send(embed=discord.Embed(
            title="╼ admins ╾",
            description="\n".join(lines),
            color=0x2b2d31
        ))

    @add_admin.error
    @remove_admin.error
    async def admin_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(description="⊘ member not found.", color=0xff4500))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(description="⊘ usage: `!admin @member` / `!rmadmin @member`", color=0xff4500))

async def setup(bot):
    await bot.add_cog(Admins(bot))
