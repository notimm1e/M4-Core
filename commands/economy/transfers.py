import discord
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Transfers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = 50000

    @commands.hybrid_command(name="deposit", aliases=["dep"], description="move cores to your bank")
    async def deposit(self, ctx, amount: str):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)
        
        wallet = data[user_id]["wallet"]
        if amount.lower() == "all": amount = wallet
        else: amount = int(amount)

        if amount > wallet or amount <= 0:
            return await ctx.send(embed=discord.Embed(description="⊘ insufficient wallet cores.", color=0xff4500))

        data[user_id]["wallet"] -= amount
        data[user_id]["bank"] += amount
        save_bank(data)
        await ctx.send(embed=discord.Embed(description=f"◈ deposited **⌬ {amount:,}** cores.", color=0x2b2d31))

    @commands.hybrid_command(name="withdraw", aliases=["with"], description="move cores to your wallet")
    async def withdraw(self, ctx, amount: str):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)
        
        bank = data[user_id]["bank"]
        if amount.lower() == "all": amount = bank
        else: amount = int(amount)

        if amount > bank or amount <= 0:
            return await ctx.send(embed=discord.Embed(description="⊘ insufficient bank cores.", color=0xff4500))

        data[user_id]["bank"] -= amount
        data[user_id]["wallet"] += amount
        save_bank(data)
        await ctx.send(embed=discord.Embed(description=f"◈ withdrew **⌬ {amount:,}** cores.", color=0x2b2d31))

    @commands.hybrid_command(name="pay", description="transfer cores to another user")
    async def pay(self, ctx, member: discord.Member, amount: int):
        if member.id == ctx.author.id:
            return await ctx.send("⊘ you cannot pay yourself.")
        
        if amount > self.limit:
            return await ctx.send(embed=discord.Embed(description=f"⊘ transfer limit is **⌬ {self.limit:,}**.", color=0xff4500))

        data = load_bank()
        data = open_account(ctx.author.id, data)
        data = open_account(member.id, data)
        
        sender_id = str(ctx.author.id)
        rec_id = str(member.id)

        if amount > data[sender_id]["wallet"] or amount <= 0:
            return await ctx.send(embed=discord.Embed(description="⊘ insufficient cores in wallet.", color=0xff4500))

        data[sender_id]["wallet"] -= amount
        data[rec_id]["wallet"] += amount
        save_bank(data)

        embed = discord.Embed(
            description=f"╼ **transfer complete** ╾\n\nsent **⌬ {amount:,}** to {member.display_name.lower()}.",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Transfers(bot))
