import discord
from discord.ext import commands

# If you don't have simpleeval, you can use a basic eval with 
# strict limitations, but for now, we'll use a clean setup.

@commands.command(name="calculator", aliases=["calc"])
async def calculator(ctx, *, expression: str):
    # 1. Standardize the input (handle x, X, and ×)
    clean_expression = expression.replace('x', '*').replace('X', '*').replace('×', '*')
    
    try:
        # 2. Calculate the result
        # Note: Using eval() is generally risky with user input. 
        # For a production bot, consider the 'simpleeval' library.
        # This basic version allows standard math: +, -, *, /, **
        result = eval(clean_expression, {"__builtins__": None}, {})
        
        # 3. Create the Blue Embed
        embed = discord.Embed(
            title="Calculation Result",
            description=f"**Input:** `{expression}`\n**Answer:** `{result}`",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    except Exception as e:
        # Handle errors (like dividing by zero or typing words)
        error_embed = discord.Embed(
            title="Error",
            description="Invalid expression. Please use numbers and operators (e.g., 4x2, 10/2).",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
