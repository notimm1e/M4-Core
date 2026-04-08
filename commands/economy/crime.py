import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account, get_cooldown, set_cooldown

ROB_COOLDOWN = 300
CRIME_COOLDOWN = 600

CRIMES = [
    "hacked a government server", "pickpocketed a tourist", "sold knockoff merch",
    "ran a pyramid scheme", "shoplifted a vending machine", "forged a document",
    "jaywalked aggressively", "smuggled rare cheese", "sold cocaine", "took an assassin job", "spiked a bar drink", "robbed a bank",
]

class Crime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="rob", description="attempt to steal cores from a user's wallet")
    async def rob(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            return await ctx.send("⊘ you cannot rob yourself.")

        data = load_bank()
        data = open_account(ctx.author.id, data)
        data = open_account(member.id, data)

        remaining = get_cooldown(ctx.author.id, data, "last_rob", ROB_COOLDOWN)
        if remaining:
            hrs = round(remaining / 3600, 1)
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ lay low for {hrs}h", color=0xff4500
            ), ephemeral=True)

        victim_id = str(member.id)
        robber_id = str(ctx.author.id)

        if data[victim_id]["wallet"] < 100:
            return await ctx.send("⊘ this user is too poor to rob.")

        set_cooldown(ctx.author.id, data, "last_rob")

        if random.random() < 0.45:
            stolen = random.randint(50, data[victim_id]["wallet"])
            data[victim_id]["wallet"] -= stolen
            data[robber_id]["wallet"] += stolen
            save_bank(data)
            embed = discord.Embed(
                description=f"╼ **theft success** ╾\nyou stole **⌬ {stolen:,}** from {member.display_name.lower()}.",
                color=0x57f287
            )
        else:
            fine = random.randint(100, 500)
            data[robber_id]["wallet"] = max(0, data[robber_id]["wallet"] - fine)
            data[victim_id]["wallet"] += fine
            save_bank(data)
            embed = discord.Embed(
                description=f"⊘ **caught**\nyou were caught and paid a fine of **⌬ {fine:,}** to {member.display_name.lower()}.",
                color=0xff4500
            )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="crime", description="commit a crime for cores")
    async def crime(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_crime", CRIME_COOLDOWN)
        if remaining:
            mins = round(remaining / 60)
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ lay low for {mins}m", color=0xff4500
            ), ephemeral=True)

        set_cooldown(ctx.author.id, data, "last_crime")

        if random.random() < 0.4:
            fine = random.randint(100, 600)
            data[user_id]["wallet"] = max(0, data[user_id]["wallet"] - fine)
            save_bank(data)
            embed = discord.Embed(
                description=f"⊘ **busted**\ncaught in the act. fined **⌬ {fine:,}** cores.",
                color=0xff4500
            )
        else:
            earnings = random.randint(200, 900)
            data[user_id]["wallet"] += earnings
            save_bank(data)
            act = random.choice(CRIMES)
            embed = discord.Embed(
                description=f"╼ **crime pays** ╾\nyou {act} and pocketed **⌬ {earnings:,}** cores.",
                color=0x57f287
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Crime(bot))
