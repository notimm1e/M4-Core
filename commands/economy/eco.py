import discord
import json
import os
import random
from discord import app_commands
from discord.ext import commands

# The file where money is saved
BANK_FILE = "bank.json"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accounts = self.load_bank()

    def load_bank(self):
        if os.path.exists(BANK_FILE):
            with open(BANK_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_bank(self):
        with open(BANK_FILE, "w") as f:
            json.dump(self.accounts, f, indent=4)

    def open_account(self, user_id):
        user_id = str(user_id)
        if user_id not in self.accounts:
            # Starting balance: 100
            self.accounts[user_id] = {"wallet": 100, "bank": 0}
            self.save_bank()
            return True
        return False

    @commands.hybrid_command(name="balance", description="Check your current wallet and bank balance")
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        self.open_account(member.id)
        
        user_data = self.accounts[str(member.id)]
        wallet = user_data["wallet"]
        bank = user_data["bank"]

        embed = discord.Embed(title=f"{member.name}'s Balance", color=discord.Color.gold())
        embed.add_field(name="Wallet", value=f"${wallet}", inline=True)
        embed.add_field(name="Bank", value=f"${bank}", inline=True)
        embed.set_footer(text="M4-Core Economy")
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="beg", description="Ask for some spare change")
    @commands.cooldown(1, 30, commands.BucketType.user) # 30-second cooldown
    async def beg(self, ctx):
        self.open_account(ctx.author.id)
        
        earnings = random.randint(5, 50)
        self.accounts[str(ctx.author.id)]["wallet"] += earnings
        self.save_bank()

        responses = [
            f"Someone felt generous and gave you **${earnings}**!",
            f"You found **${earnings}** on the sidewalk.",
            f"A stranger tossed **${earnings}** into your hat."
        ]
        
        await ctx.send(random.choice(responses))

    # Error handler for the beg cooldown
    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Slow down! You can beg again in {round(error.retry_after)} seconds.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Economy(bot))