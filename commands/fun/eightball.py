import discord
import random
from discord.ext import commands

RESPONSES = [
    "it is certain.", "without a doubt.", "yes, definitely.",
    "you may rely on it.", "most likely.", "outlook good.",
    "signs point to yes.", "reply hazy, try again.", "ask again later.",
    "cannot predict now.", "don't count on it.", "my sources say no.",
    "outlook not so good.", "very doubtful.", "absolutely not."
]

class eightball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball", aliases=["ask"])
    async def eightball(self, ctx, *, question: str):
        embed = discord.Embed(title="⊙ 8ball", color=discord.Color.purple())
        embed.add_field(name="question", value=question, inline=False)
        embed.add_field(name="answer", value=random.choice(RESPONSES), inline=False)
        await ctx.send(embed=embed)

    @eightball.error
    async def eightball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="✖ missing question", description="usage: `!8ball <question>`", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(eightball(bot))
