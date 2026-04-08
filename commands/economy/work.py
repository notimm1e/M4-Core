import discord
import random
import time
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account, get_cooldown, set_cooldown

COOLDOWN = 180

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="work", description="work a shift to earn cores")
    async def work(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_work", COOLDOWN)
        if remaining:
            min_left = round(remaining / 60)
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ cooldown: {min_left}m remaining", color=0xff4500
            ), ephemeral=True)

        earnings = random.randint(300, 850)
        data[user_id]["wallet"] += earnings
        set_cooldown(ctx.author.id, data, "last_work")
        save_bank(data)

        logs = ["system maintenance", "data mining", "protocol optimization", "drug dealing",
                "selling fish", "freelancing", "dog walking", "lawn mowing"]

        embed = discord.Embed(
            title=f"⚒ {random.choice(logs)}",
            description=f"you earned **⌬ {earnings}** cores.",
            color=0x57f287
        )
        embed.set_footer(text=f"wallet: {data[user_id]['wallet']} cores")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Work(bot))
