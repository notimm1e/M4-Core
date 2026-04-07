import discord
from discord.ext import commands
import re

class calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calculator", aliases=["calc"])
    async def calculator(self, ctx, *, expression: str):
        clean = expression.replace('x', '*').replace('X', '*').replace('×', '*')
        clean = re.sub(r'[^0-9+\-*/(). ]', '', clean)

        try:
            result = eval(clean, {"__builtins__": None}, {})

            embed = discord.Embed(title="calculator", color=discord.Color.blue())
            embed.add_field(name="input", value=f"```\n{expression}\n```", inline=False)
            embed.add_field(name="result", value=f"```\n{result}\n```", inline=False)
            await ctx.send(embed=embed)

        except Exception:
            await ctx.send(embed=discord.Embed(
                title="✖ invalid expression",
                description="use numbers and operators only. (e.g. `4x2`, `10/2`)",
                color=discord.Color.red()
            ))

async def setup(bot):
    await bot.add_cog(calculator(bot))