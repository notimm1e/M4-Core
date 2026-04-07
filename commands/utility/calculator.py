import discord
from discord.ext import commands
import re

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calculator", aliases=["calc"])
    async def calculator(self, ctx, *, expression: str):
        # 1. Clean the input: Replace 'x', 'X', and '×' with '*'
        # We also strip out anything that isn't a number or a math operator for safety
        clean_expression = expression.replace('x', '*').replace('X', '*').replace('×', '*')
        
        # Remove any characters that aren't math-related to prevent exploit attempts
        clean_expression = re.sub(r'[^0-9+\-*/(). ]', '', clean_expression)

        try:
            # 2. Calculate using a restricted eval
            # We pass empty dicts for globals/locals to block access to bot internals
            result = eval(clean_expression, {"__builtins__": None}, {})
            
            # 3. Create the Blue Embed
            embed = discord.Embed(
                title="Calculation Result",
                color=discord.Color.blue()
            )
            embed.add_field(name="Input", value=f"```\n{expression}\n```", inline=False)
            embed.add_field(name="Answer", value=f"```\n{result}\n```", inline=False)
            
            await ctx.send(embed=embed)

        except Exception:
            # Handle math errors (like 4/0) or syntax errors
            error_embed = discord.Embed(
                title="Error",
                description="Invalid expression. Please use numbers and operators (e.g., 4x2, 10/2).",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)

# This is the "handshake" function that fixes the "no setup function" error
async def setup(bot):
    await bot.add_cog(Calculator(bot))

