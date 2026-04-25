import discord
import random
from discord.ext import commands

CHOICES = ["rock", "paper", "scissors"]
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
ICONS = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

class rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rps")
    async def rps(self, ctx, choice: str):
        choice = choice.lower()
        if choice not in CHOICES:
            return await ctx.send(embed=discord.Embed(title="✖ invalid choice", description="choose `rock`, `paper`, or `scissors`.", color=discord.Color.red()))

        bot_choice = random.choice(CHOICES)

        if choice == bot_choice:
            result, color = "tie", discord.Color.yellow()
        elif BEATS[choice] == bot_choice:
            result, color = "you win!", discord.Color.green()
        else:
            result, color = "you lose..", discord.Color.red()

        embed = discord.Embed(title="rock paper scissors", color=color)
        embed.add_field(name="you", value=f"{ICONS[choice]} {choice}", inline=True)
        embed.add_field(name="bot", value=f"{ICONS[bot_choice]} {bot_choice}", inline=True)
        embed.add_field(name="result", value=result, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(rps(bot))
