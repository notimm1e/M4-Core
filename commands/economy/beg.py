import discord
import random
from discord.ext import commands
# Importing the shared functions from your base file
from commands.economy.economy_base import load_bank, save_bank, open_account

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="beg", description="Ask strangers for some spare change (50 min cooldown)")
    @commands.cooldown(1, 3000, commands.BucketType.user) # 3000 seconds = 50 minutes
    async def beg(self, ctx):
        # 1. Load the data
        data = load_bank()
        data = open_account(ctx.author.id, data)
        
        # 2. 30% chance of getting rejected
        if random.random() < 0.3:
            responses = [
                "A stranger looked at you and kept walking.",
                "Someone told you to 'get a real job.'",
                "You found a penny, but it was stuck to the ground with gum.",
                "A rich person laughed at you and drove away."
            ]
            return await ctx.send(f"❌ {random.choice(responses)}")

        # 3. Calculate small earnings
        earnings = random.randint(10, 85)
        
        # 4. Update the wallet
        user_id = str(ctx.author.id)
        data[user_id]["wallet"] += earnings
        
        # 5. Save the data back to your Mac
        save_bank(data)
        
        # 6. Success response
        success_messages = [
            f"A kind stranger tossed **${earnings}** into your hat.",
            f"You found **${earnings}** tucked inside a discarded wallet!",
            f"Someone felt bad for you and gave you **${earnings}**.",
            f"You begged near the pier and earned **${earnings}** from tourists."
        ]
        
        await ctx.send(f"🪙 {random.choice(success_messages)}")

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # Calculate remaining time
            minutes = round(error.retry_after / 60)
            if minutes < 1:
                await ctx.send(f"⏳ You just begged! Wait {round(error.retry_after)} more seconds.", ephemeral=True)
            else:
                await ctx.send(f"⏳ Everyone is tired of your begging. Try again in {minutes} minutes.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Beg(bot))