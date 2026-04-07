import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Plinko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="plinko")
    async def plinko(self, ctx, amount: int):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        if amount > data[user_id]["wallet"] or amount <= 0:
            return await ctx.send("⊘ insufficient cores.")

        # Multipliers: 0.2x, 0.5x, 1.2x, 1.5x, 3x
        outcomes = [0.2, 0.5, 1.2, 1.5, 3.0]
        weights = [25, 35, 20, 15, 5] # probabilities
        multiplier = random.choices(outcomes, weights=weights)[0]
        
        winnings = int(amount * multiplier)
        data[user_id]["wallet"] = (data[user_id]["wallet"] - amount) + winnings
        save_bank(data)

        path = " ".join([random.choice(["↙", "↘"]) for _ in range(4)])
        
        embed = discord.Embed(
            title="╼ plinko ╾",
            description=f"ball path: `{path}`\n\nmultiplier: **{multiplier}x**\nresult: **⌬ {winnings:,}** cores",
            color=0x2b2d31 if multiplier >= 1 else 0xff4500
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Plinko(bot))
