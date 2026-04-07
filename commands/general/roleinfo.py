import discord
from discord.ext import commands

class roleinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roleinfo", aliases=["ri", "role"])
    async def roleinfo(self, ctx, *, role: discord.Role):
        perms = [p.replace("_", " ") for p, v in role.permissions if v]

        embed = discord.Embed(title=role.name, color=role.color if role.color.value else discord.Color.blue())
        embed.add_field(name="id", value=f"`{role.id}`", inline=True)
        embed.add_field(name="members", value=f"`{len(role.members)}`", inline=True)
        embed.add_field(name="color", value=f"`{str(role.color)}`", inline=True)
        embed.add_field(name="mentionable", value="yes" if role.mentionable else "no", inline=True)
        embed.add_field(name="hoisted", value="yes" if role.hoist else "no", inline=True)
        embed.add_field(name="position", value=f"`{role.position}`", inline=True)
        if perms:
            perm_str = ", ".join(perms)
            if len(perm_str) > 1024:
                perm_str = perm_str[:1020] + "..."
            embed.add_field(name="permissions", value=f"```\n{perm_str}\n```", inline=False)
        embed.set_footer(text=f"requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @roleinfo.error
    async def roleinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title="✖ missing role",
                description="provide a role. (e.g. `!roleinfo moderator`)",
                color=discord.Color.red()
            ))
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(embed=discord.Embed(
                title="✖ role not found",
                description="that role doesn't exist.",
                color=discord.Color.red()
            ))

async def setup(bot):
    await bot.add_cog(roleinfo(bot))
