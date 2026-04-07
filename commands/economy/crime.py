import discord
import random
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Crime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="rob", description="attempt to steal cores from a user's wallet")
    @commands.cooldown(1, 7200, commands.BucketType.user) # 2 hour cooldown
    async def rob(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            return await ctx.send("⊘ you cannot rob yourself.")

        data = load_bank()
        data = open_account(ctx.author.id, data)
        data = open_account(member.id, data)
        
        victim_id = str(member.id)
        robber_id = str(ctx.author.id)

        if data[victim_id]["wallet"] < 100:
            return await ctx.send("⊘ this user is too poor to rob.")

        # 45% Success Rate
        if random.random() < 0.45:
            stolen = random.randint(50, data[victim_id]["wallet"])
            data[victim_id]["wallet"] -= stolen
            data[robber_id]["wallet"] += stolen
            save_bank(data)
            
            embed = discord.Embed(
                description=f"╼ **theft success** ╾\nyou stole **⌬ {stolen:,}** from {member.display_name.lower()}.",
                color=0x2b2d31
            )
        else:
            fine = random.randint(100, 500)
            data[robber_id]["wallet"] -= fine
            data[victim_id]["wallet"] += fine
            save_bank(data)
            
            embed = discord.Embed(
                description=f"⊘ **caught**\nyou were caught and paid a fine of **⌬ {fine:,}** to {member.display_name.lower()}.",
                color=0xff4500
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Crime(bot))
