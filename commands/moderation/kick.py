import discord
from discord.ext import commands

class kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "no reason provided"):
        if member == ctx.author:
            return await ctx.send(embed=discord.Embed(title="✖ invalid target", description="you can't kick yourself.", color=discord.Color.red()))
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(embed=discord.Embed(title="✖ insufficient hierarchy", description="you can't kick someone with an equal or higher role.", color=discord.Color.red()))

        try:
            await member.send(embed=discord.Embed(
                title=f"you've been kicked from {ctx.guild.name}",
                description=f"**reason:** {reason}\n**by:** {ctx.author.name}",
                color=discord.Color.red()
            ))
        except discord.Forbidden:
            pass

        await member.kick(reason=reason)
        await ctx.send(embed=discord.Embed(
            title="√ kicked",
            description=f"kicked {member.mention} · **{reason}**",
            color=discord.Color.green()
        ))

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="✖ missing permissions", description="you need `kick members` to use this.", color=discord.Color.red()))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="✖ member not found", description="that member doesn't exist.", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(kick(bot))
