import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="daily", description="claim your daily allowance of cores")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        
        earnings = random.randint(100, 300)
        user_id = str(ctx.author.id)
        data[user_id]["wallet"] += earnings
        save_bank(data)
        
        embed = discord.Embed(
            description=f"╼ **daily reward** ╾\n\nyou received **⌬ {earnings}** cores.",
            color=0x2b2d31
        )
        embed.set_footer(text=f"current wallet: {data[user_id]['wallet']} cores")
        
        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            hours = round(error.retry_after / 3600)
            embed = discord.Embed(description=f"⧖ come back in {hours}h", color=0xff4500)
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Daily(bot))
