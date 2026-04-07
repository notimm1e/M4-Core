import discord
from discord.ext import commands
from commands.economy.economy_base import load_bank, open_account

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="balance", aliases=["bal"], description="check your current wallet and bank")
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = load_bank()
        data = open_account(member.id, data)
        
        user_id = str(member.id)
        wallet = data[user_id]["wallet"]
        bank = data[user_id]["bank"]

        embed = discord.Embed(
            title=f"╼ {member.display_name.lower()}'s ledger ╾",
            color=0x2b2d31
        )
        embed.add_field(name="◈ wallet", value=f"⌬ {wallet:,} cores", inline=True)
        embed.add_field(name="◈ bank", value=f"⌬ {bank:,} cores", inline=True)
        embed.add_field(name="▼ total", value=f"**⌬ {wallet + bank:,} cores**", inline=False)
        embed.set_footer(text="m4-core systems")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Balance(bot))
