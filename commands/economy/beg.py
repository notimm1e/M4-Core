import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="beg", description="request spare cores")
    @commands.cooldown(1, 3000, commands.BucketType.user)
    async def beg(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        
        embed = discord.Embed(color=0x2b2d31)

        if random.random() < 0.3:
            embed.description = "⊘ request denied by network users."
            return await ctx.send(embed=embed)

        earnings = random.randint(10, 85)
        user_id = str(ctx.author.id)
        data[user_id]["wallet"] += earnings
        save_bank(data)
        
        embed.description = f"⌬ **{earnings}** cores added to your wallet."
        await ctx.send(embed=embed)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            sec = round(error.retry_after)
            embed = discord.Embed(description=f"⧖ retry in {sec}s", color=0xff4500)
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Beg(bot))
