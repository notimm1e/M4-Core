import discord
import random
import pyfiglet
from discord.ext import commands

class TextTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mock", description="mOcK tExT lIkE tHiS")
    async def mock(self, ctx, *, text: str):
        result = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
        embed = discord.Embed(description=result, color=0x2b2d31)
        await ctx.send(embed=embed)

    @commands.command(name="reverse", aliases=["rev"], description="reverse a string")
    async def reverse(self, ctx, *, text: str):
        result = text[::-1]
        embed = discord.Embed(description=result, color=0x2b2d31)
        await ctx.send(embed=embed)

    @commands.command(name="ascii", description="convert text to ascii art")
    async def ascii(self, ctx, *, text: str):
        if len(text) > 20:
            return await ctx.send(embed=discord.Embed(
                description="✖ max 20 characters for ascii art.",
                color=0xff4500
            ))
        result = pyfiglet.figlet_format(text, font="standard")
        if len(result) > 1900:
            result = result[:1900]
        await ctx.send(f"```\n{result}\n```")

async def setup(bot):
    await bot.add_cog(TextTools(bot))
