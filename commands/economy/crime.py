import discord
import random
from discord.ext import commands
from helpers.economy_base import load_bank, save_bank, open_account, get_cooldown, set_cooldown, apply_loss, apply_earnings, debt_prompt

ROB_COOLDOWN = 300
CRIME_COOLDOWN = 600

CRIMES = [
    "hacked a government server", "pickpocketed a tourist", "sold knockoff merch",
    "ran a pyramid scheme", "shoplifted a vending machine", "forged a document",
    "jaywalked aggressively", "smuggled rare cheese", "stole a car and returned it with a full tank", "illegally downloaded a movie",
    "vandalized a public statue", "committed tax fraud", "hacked into a casino and won big", "stole a bike and used it for a day before returning it",
]

class Crime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="rob", description="attempt to steal cores from a user's wallet")
    async def rob(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            return await ctx.send("⊘ you can't rob yourself!")

        data = load_bank()
        data = open_account(ctx.author.id, data)
        data = open_account(member.id, data)

        data = await debt_prompt(ctx, self.bot, data, ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_rob", ROB_COOLDOWN)
        if remaining:
            mins = round(remaining / 60, 1)
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ lay low for {mins}m", color=0xff4500
            ), ephemeral=True)

        victim_id = str(member.id)
        robber_id = str(ctx.author.id)

        if data[victim_id]["wallet"] < 150:
            return await ctx.send("⊘ this user is too poor to rob. look for someone with at least ⌬ 150 in their wallet.")

        set_cooldown(ctx.author.id, data, "last_rob")

        if random.random() < 0.45:
            max_steal = min(1000, int(data[victim_id]["wallet"] * 0.25))
            stolen = random.randint(50, max(50, max_steal))
            data[victim_id]["wallet"] -= stolen
            debt_paid, to_wallet = apply_earnings(robber_id, data, stolen)
            save_bank(data)
            desc = f"╼ **theft success** ╾\nyou stole **⌬ {stolen:,}** from {member.display_name.lower()}"
            if debt_paid:
                desc += f"\n⌬ {debt_paid:,} went toward your debt"
            embed = discord.Embed(description=desc, color=0x57f287)
        else:
            fine = random.randint(100, 500)
            apply_loss(robber_id, data, fine)
            data[victim_id]["wallet"] += fine
            save_bank(data)
            debt = data[robber_id]["debt"]
            desc = f"⊘ **caught!**\nyou were caught and fined **⌬ {fine:,}** to {member.display_name.lower()}"
            if debt > 0:
                desc += f"\n⌬ {data[robber_id]['debt']:,} now in debt"
            embed = discord.Embed(description=desc, color=0xff4500)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="crime", description="commit a crime for cores")
    async def crime(self, ctx):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        data = await debt_prompt(ctx, self.bot, data, ctx.author.id)

        remaining = get_cooldown(ctx.author.id, data, "last_crime", CRIME_COOLDOWN)
        if remaining:
            mins = round(remaining / 60)
            return await ctx.send(embed=discord.Embed(
                description=f"⧖ lay low for {mins}m", color=0xff4500
            ), ephemeral=True)

        set_cooldown(ctx.author.id, data, "last_crime")

        if random.random() < 0.4:
            fine = random.randint(100, 600)
            apply_loss(user_id, data, fine)
            save_bank(data)
            debt = data[user_id]["debt"]
            desc = f"⊘ **busted!**\ncaught in the act. fined **⌬ {fine:,}** cores"
            if debt > 0:
                desc += f"\n⌬ {debt:,} now in debt"
            embed = discord.Embed(description=desc, color=0xff4500)
        else:
            earnings = random.randint(200, 900)
            debt_paid, to_wallet = apply_earnings(user_id, data, earnings)
            save_bank(data)
            act = random.choice(CRIMES)
            desc = f"╼ **crime pays** ╾\nyou {act} and earned **⌬ {earnings:,}** cores"
            if debt_paid:
                desc += f"\n⌬ {debt_paid:,} went toward your debt"
            embed = discord.Embed(description=desc, color=0x57f287)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Crime(bot))
