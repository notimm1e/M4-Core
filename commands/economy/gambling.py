import discord
import random
import asyncio
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="coinflip", aliases=["cf"], description="flip a coin to double your cores")
    async def coinflip(self, ctx, side: str, amount: int):
        side = side.lower()
        if side not in ["heads", "tails"]:
            return await ctx.send("⊘ choose `heads` or `tails`.")

        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        if amount > data[user_id]["wallet"] or amount <= 0:
            return await ctx.send("⊘ insufficient wallet balance.")

        result = random.choice(["heads", "tails"])
        win = side == result

        if win:
            data[user_id]["wallet"] += amount
            msg = f"◈ the coin landed on **{result}**. you won **⌬ {amount:,}**."
        else:
            data[user_id]["wallet"] -= amount
            msg = f"⊘ the coin landed on **{result}**. you lost **⌬ {amount:,}**."

        save_bank(data)
        await ctx.send(embed=discord.Embed(description=msg, color=0x2b2d31))

    @commands.hybrid_command(name="blackjack", aliases=["bj"], description="play blackjack against the system")
    async def blackjack(self, ctx, amount: int):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        if amount > data[user_id]["wallet"] or amount <= 0:
            return await ctx.send("⊘ insufficient wallet balance.")

        def get_card():
            return random.randint(2, 11)

        player_total = get_card() + get_card()
        dealer_total = get_card() + get_card()

        if player_total == 21:
            data[user_id]["wallet"] += int(amount * 1.5)
            save_bank(data)
            return await ctx.send(embed=discord.Embed(description=f"╼ **blackjack** ╾\nyou won **⌬ {int(amount*1.5):,}** cores.", color=0x2b2d31))

        embed = discord.Embed(title="╼ blackjack ╾", color=0x2b2d31)
        embed.add_field(name="◈ your hand", value=f"total: `{player_total}`")
        embed.add_field(name="◈ dealer hand", value="total: `?`")
        msg = await ctx.send(embed=embed)

        # Logic for hitting/standing would go here using reactions or buttons

async def setup(bot):
    await bot.add_cog(Gambling(bot))
