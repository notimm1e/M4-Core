import discord
import random
from discord.ext import commands
from helpers.economy_base import load_bank, save_bank, open_account, get_cooldown, set_cooldown, apply_earnings, debt_prompt

COOLDOWN = 120

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="beg", description="request spare cores")
    async def beg(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        data = await debt_prompt(ctx, self.bot, data, ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_beg", COOLDOWN)
        if remaining:
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ retry in {remaining}s", color=0xff4500
            ), ephemeral=True)

        set_cooldown(ctx.author.id, data, "last_beg")

        if random.random() < 0.3:
            save_bank(data)
            return await ctx.send(embed=discord.Embed(
                description="⊘ request denied by network users.", color=0xfee75c
            ))

        earnings = random.randint(10, 85)
        debt_paid, to_wallet = apply_earnings(user_id, data, earnings)
        save_bank(data)

        desc = f"⌬ **{earnings}** cores added to your wallet."
        if debt_paid:
            desc += f"\n⌬ {debt_paid:,} went toward your debt."

        await ctx.send(embed=discord.Embed(description=desc, color=0xfee75c))

async def setup(bot):
    await bot.add_cog(Beg(bot))
