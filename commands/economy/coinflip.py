import discord
import random
from discord.ext import commands
from helpers.economy_base import load_bank, save_bank, open_account, apply_loss, apply_earnings, debt_prompt

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="coinflip", aliases=["cf"], description="bet cores on heads or tails")
    async def coinflip(self, ctx, side: str, amount: int):
        side = side.lower()
        if side not in ("heads", "tails", "h", "t"):
            return await ctx.send(embed=discord.Embed(
                description="✖ choose `heads` or `tails`.",
                color=0xff4500
            ))

        side = "heads" if side in ("heads", "h") else "tails"

        if amount <= 0:
            return await ctx.send(embed=discord.Embed(
                description="⊘ bet must be greater than 0.",
                color=0xff4500
            ))

        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        data = await debt_prompt(ctx, self.bot, data, ctx.author.id)

        if amount > data[user_id]["wallet"]:
            return await ctx.send(embed=discord.Embed(
                description="⊘ insufficient cores in wallet.",
                color=0xff4500
            ))

        result = random.choice(["heads", "tails"])
        won = result == side
        coin = "🪙"

        if won:
            debt_paid, to_wallet = apply_earnings(user_id, data, amount)
            desc = f"{coin} **{result}** — you won **⌬ {amount:,}** cores."
            if debt_paid:
                desc += f"\n⌬ {debt_paid:,} went toward your debt."
            color = 0x57f287
        else:
            apply_loss(user_id, data, amount)
            debt = data[user_id]["debt"]
            desc = f"{coin} **{result}** — you lost **⌬ {amount:,}** cores."
            if debt > 0:
                desc += f"\n⌬ {debt:,} now in debt."
            color = 0xff4500

        save_bank(data)

        embed = discord.Embed(description=desc, color=color)
        embed.set_footer(text=f"wallet: {data[user_id]['wallet']:,} cores")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Coinflip(bot))
