import discord
import random
from discord.ext import commands

class ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ship")
    async def ship(self, ctx, member1: discord.Member, member2: discord.Member):
        score = random.randint(0, 100)
        filled = score // 10
        bar = "█" * filled + "░" * (10 - filled)

        if score < 20: verdict = "absolutely not."
        elif score < 40: verdict = "it's a stretch..."
        elif score < 60: verdict = "maybe something there."
        elif score < 80: verdict = "pretty good match!"
        else: verdict = "soulmates. 💘"

        embed = discord.Embed(title="ship", color=discord.Color.pink() if hasattr(discord.Color, 'pink') else discord.Color.magenta())
        embed.description = f"{member1.mention} × {member2.mention}"
        embed.add_field(name="compatibility", value=f"`{bar}` **{score}%**", inline=False)
        embed.add_field(name="verdict", value=verdict, inline=False)
        await ctx.send(embed=embed)

    @ship.error
    async def ship_error(self, ctx, error):
        error.handled = True
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="✖ missing members", description="usage: `!ship @user1 @user2`", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(ship(bot))
