import discord
import random
from discord.ext import commands
# This imports the "Manager" functions from your base file
from commands.economy.economy_base import load_bank, save_bank, open_account

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="work", description="Work a shift to earn money")
    @commands.cooldown(1, 600, commands.BucketType.user) # 10 Minute Cooldown
    async def work(self, ctx):
        # 1. Load the current data from bank.json
        data = load_bank()
        
        # 2. Ensure the user has an account
        data = open_account(ctx.author.id, data)
        
        # 3. Calculate earnings
        earnings = random.randint(100, 500)
        
        # 4. Update the user's wallet
        user_id = str(ctx.author.id)
        data[user_id]["wallet"] += earnings
        
        # 5. Save the updated data back to the file
        save_bank(data)
        
        # 6. Send the response
        jobs = [
            f"You delivered some packages and earned **${earnings}**.",
            f"You spent the day coding and earned **${earnings}**.",
            f"You helped a neighbor with yard work and got **${earnings}**."
        ]
        
        await ctx.send(random.choice(jobs))

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # Formats the wait time into minutes
            minutes = round(error.retry_after / 60)
            if minutes < 1:
                await ctx.send(f"⏳ Slow down! You can work again in {round(error.retry_after)} seconds.", ephemeral=True)
            else:
                await ctx.send(f"⏳ You're exhausted. Try again in {minutes} minutes.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Work(bot))