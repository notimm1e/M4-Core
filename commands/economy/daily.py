import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account, get_cooldown, set_cooldown

COOLDOWN = 86400

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="daily", description="claim your daily allowance of cores")
    async def daily(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_daily", COOLDOWN)
        if remaining:
            hours = round(remaining / 3600)
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ come back in {hours}h", color=0xff4500
            ), ephemeral=True)

        earnings = random.randint(100, 300)
        data[user_id]["wallet"] += earnings
        set_cooldown(ctx.author.id, data, "last_daily")
        save_bank(data)

        embed = discord.Embed(
            description=f"╼ **daily reward** ╾\n\nyou received **⌬ {earnings}** cores.",
            color=0xeb459e
        )
        embed.set_footer(text=f"current wallet: {data[user_id]['wallet']} cores")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Daily(bot))
