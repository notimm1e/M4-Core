import discord
from discord.ext import commands

class ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "no reason provided"):
        if member == ctx.author:
            return await ctx.send(embed=discord.Embed(title="✖ invalid target", description="you can't ban yourself.", color=discord.Color.red()))
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(embed=discord.Embed(title="✖ insufficient hierarchy", description="you can't ban someone with an equal or higher role.", color=discord.Color.red()))

        try:
            await member.send(embed=discord.Embed(
                title=f"you've been banned from {ctx.guild.name}",
                description=f"**reason:** {reason}\n**by:** {ctx.author.name}",
                color=discord.Color.red()
            ))
        except discord.Forbidden:
            pass

        await member.ban(reason=reason)
        await ctx.send(embed=discord.Embed(
            title="√ banned",
            description=f"banned {member.mention} · **{reason}**",
            color=discord.Color.green()
        ))

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason: str = "no reason provided"):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(embed=discord.Embed(
                title="√ unbanned",
                description=f"unbanned `{user.name}` · **{reason}**",
                color=discord.Color.green()
            ))
        except discord.NotFound:
            await ctx.send(embed=discord.Embed(title="✖ not found", description="that user isn't banned or doesn't exist.", color=discord.Color.red()))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="✖ missing permissions", description="you need `ban members` to use this.", color=discord.Color.red()))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="✖ member not found", description="that member doesn't exist.", color=discord.Color.red()))

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="✖ missing permissions", description="you need `ban members` to use this.", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(ban(bot))
