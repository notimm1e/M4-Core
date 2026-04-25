import discord
import random
import time
from discord.ext import commands
from helpers.economy_base import load_bank, save_bank, open_account, get_cooldown, set_cooldown, apply_earnings, debt_prompt

COOLDOWN = 180

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="work", description="work a shift to earn cores")
    async def work(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        data = await debt_prompt(ctx, self.bot, data, ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_work", COOLDOWN)
        if remaining:
            min_left = round(remaining / 60)
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ cooldown: {min_left}m remaining", color=0xff4500
            ), ephemeral=True)

        earnings = random.randint(300, 850)
        debt_paid, to_wallet = apply_earnings(user_id, data, earnings)
        set_cooldown(ctx.author.id, data, "last_work")
        save_bank(data)

        logs = ["system maintenance", "data mining", "protocol optimization", "drug dealing",
                "selling fish", "freelancing", "dog walking", "lawn mowing", "programming",
                "manual labor", "customer support", "content creation", "video editing", "graphic design",
                "accounting", "tutoring", "consulting", "espionage", "street performing"]

        desc = f"you earned **⌬ {earnings}** cores"
        if debt_paid:
            desc += f"\n⌬ {debt_paid:,} went toward your debt"

        embed = discord.Embed(
            title=f"⚒ {random.choice(logs)}",
            description=desc,
            color=0x57f287
        )
        embed.set_footer(text=f"wallet: {data[user_id]['wallet']} cores")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Work(bot))
