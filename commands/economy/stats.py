import discord
from discord.ext import commands
from helpers.economy_base import load_bank

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="leaderboard", aliases=["lb", "top"], description="view the richest users")
    async def leaderboard(self, ctx):
        data = load_bank()
        # Sort users by total wealth (wallet + bank)
        leaderboard = sorted(data.items(), key=lambda x: x[1]["wallet"] + x[1]["bank"], reverse=True)
        
        embed = discord.Embed(title="╼ core leaderboard ╾", color=0x2b2d31)
        
        description = ""
        for i, (user_id, balances) in enumerate(leaderboard[:10], 1):
            user = self.bot.get_user(int(user_id))
            name = user.display_name.lower() if user else "unknown_user"
            total = balances["wallet"] + balances["bank"]
            description += f"`{i}.` **{name}** · ⌬ {total:,}\n"

        embed.description = description or "no data available."
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
