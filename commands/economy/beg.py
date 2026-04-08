import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account, get_cooldown, set_cooldown

COOLDOWN = 3000

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="beg", description="request spare cores")
    async def beg(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_beg", COOLDOWN)
        if remaining:
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ retry in {remaining}s", color=0xff4500
            ), ephemeral=True)

        embed = discord.Embed(color=0xfee75c)
        if random.random() < 0.3:
            embed.description = "⊘ request denied by network users."
            set_cooldown(ctx.author.id, data, "last_beg")
            save_bank(data)
            return await ctx.send(embed=embed)

        earnings = random.randint(10, 85)
        data[user_id]["wallet"] += earnings
        set_cooldown(ctx.author.id, data, "last_beg")
        save_bank(data)

        embed.description = f"⌬ **{earnings}** cores added to your wallet."
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Beg(bot))
