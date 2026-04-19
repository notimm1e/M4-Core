import discord
from discord.ext import commands

REVOKE_ROLES = [1490701432456876163, 1483259650983067781]

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock", description="lock the current channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        overwrites = ctx.channel.overwrites

        for role_id in REVOKE_ROLES:
            role = ctx.guild.get_role(role_id)
            if role:
                ow = overwrites.get(role, discord.PermissionOverwrite())
                ow.send_messages = False
                overwrites[role] = ow

        await ctx.channel.edit(overwrites=overwrites)
        await ctx.send(embed=discord.Embed(
            description="🔒 channel locked.",
            color=0xff4500
        ))

    @commands.command(name="unlock", description="unlock the current channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        overwrites = ctx.channel.overwrites

        for role_id in REVOKE_ROLES:
            role = ctx.guild.get_role(role_id)
            if role:
                ow = overwrites.get(role, discord.PermissionOverwrite())
                ow.send_messages = None
                overwrites[role] = ow

        await ctx.channel.edit(overwrites=overwrites)
        await ctx.send(embed=discord.Embed(
            description="🔓 channel unlocked.",
            color=0x57f287
        ))

async def setup(bot):
    await bot.add_cog(Lock(bot))
