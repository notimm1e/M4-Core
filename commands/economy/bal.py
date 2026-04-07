import discord
from discord.ext import commands
# Importing the shared functions to read the bank data
from commands.economy.economy_base import load_bank, open_account

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="balance", aliases=["bal"], description="Check your current wallet and bank balance")
    async def balance(self, ctx, member: discord.Member = None):
        """Displays the balance of a user in a clean embed."""
        # If no member is mentioned, check the author's balance
        member = member or ctx.author
        
        # 1. Load data and ensure the account exists
        data = load_bank()
        data = open_account(member.id, data)
        
        # 2. Extract values
        user_id = str(member.id)
        wallet = data[user_id]["wallet"]
        bank = data[user_id]["bank"]

        # 3. Create a professional-looking embed
        embed = discord.Embed(
            title=f"💰 {member.display_name}'s Finances",
            color=discord.Color.gold(),
            timestamp=ctx.message.created_at if ctx.message else discord.utils.utcnow()
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="💵 Wallet", value=f"`${wallet:,}`", inline=True)
        embed.add_field(name="🏦 Bank", value=f"`${bank:,}`", inline=True)
        embed.add_field(name="📊 Total", value=f"`${wallet + bank:,}`", inline=False)
        
        embed.set_footer(text="M4-Core Economy System")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Balance(bot))