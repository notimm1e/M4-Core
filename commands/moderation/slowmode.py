import discord
from discord.ext import commands

class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slowmode", aliases=["sm"], description="set channel slowmode in seconds (0 to disable)")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds < 0 or seconds > 21600:
            return await ctx.send(embed=discord.Embed(
                title="✖ invalid value",
                description="must be between `0` and `21600` (6 hours).",
                color=discord.Color.red()
            ))

        await ctx.channel.edit(slowmode_delay=seconds)

        if seconds == 0:
            desc = f"◈ slowmode disabled in {ctx.channel.mention}."
        else:
            desc = f"◈ slowmode set to **{seconds}s** in {ctx.channel.mention}."

        await ctx.send(embed=discord.Embed(description=desc, color=0x2b2d31))

async def setup(bot):
    await bot.add_cog(Slowmode(bot))
