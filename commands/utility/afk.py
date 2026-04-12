import discord
from discord.ext import commands
from datetime import datetime

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    @commands.command(name="afk")
    async def afk(self, ctx, *, reason: str = "afk"):
        self.afk_users[ctx.author.id] = {
            "reason": reason,
            "at": datetime.utcnow()
        }
        await ctx.send(embed=discord.Embed(
            title="√ afk set",
            description=f"{ctx.author.mention} is now afk · **{reason}**",
            color=discord.Color.blue()
        ))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]
            await message.channel.send(embed=discord.Embed(
                title="√ welcome back",
                description=f"{message.author.mention} your afk has been removed.",
                color=discord.Color.green()
            ))

        if message.mentions:
            for member in message.mentions:
                if member.id in self.afk_users:
                    data = self.afk_users[member.id]
                    delta = datetime.utcnow() - data["at"]
                    mins = int(delta.total_seconds() // 60)
                    time_str = f"`{mins}m ago`" if mins > 0 else "`just now`"
                    await message.channel.send(embed=discord.Embed(
                        title="⌖ user is afk",
                        description=f"{member.mention} is afk · **{data['reason']}** · {time_str}",
                        color=discord.Color.yellow()
                    ))

async def setup(bot):
    await bot.add_cog(afk(bot))
