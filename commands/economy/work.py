import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="work", description="work a shift to earn cores")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        
        earnings = random.randint(300, 850)
        user_id = str(ctx.author.id)
        data[user_id]["wallet"] += earnings
        save_bank(data)
        
        logs = ["system maintenance", "data mining", "protocol optimization", "drug dealing", "selling fish", "freelancing", "dog walking", "lawn mowing"]
        
        embed = discord.Embed(
            title=f"⚒ {random.choice(logs)}",
            description=f"you earned **⌬ {earnings}** cores.",
            color=0x2b2d31
        )
        embed.set_footer(text=f"wallet: {data[user_id]['wallet']} cores")
        
        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            min_left = round(error.retry_after / 60)
            embed = discord.Embed(description=f"⧖ cooldown: {min_left}m remaining", color=0xff4500)
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Work(bot))
