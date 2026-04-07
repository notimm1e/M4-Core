import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="work", description="work a shift to earn money")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        
        earnings = random.randint(100, 500)
        user_id = str(ctx.author.id)
        data[user_id]["wallet"] += earnings
        save_bank(data)
        
        jobs = ["delivery completed", "shift finished", "freelance task done"]
        
        embed = discord.Embed(
            title=f"⚒ {random.choice(jobs)}",
            description=f"you earned **⌬ {earnings}** for your labor.",
            color=0x77dd77
        )
        embed.set_footer(text=f"new wallet balance: {data[user_id]['wallet']}")
        
        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            min_left = round(error.retry_after / 60)
            embed = discord.Embed(description=f"⧖ shift ended: return in {min_left}m", color=0xff4500)
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Work(bot))
