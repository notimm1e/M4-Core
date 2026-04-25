import discord
import random
import string
from discord.ext import commands

class generators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="password", aliases=["pw", "genpass"])
    async def password(self, ctx, length: int = 16):
        if length < 8:
            return await ctx.send(embed=discord.Embed(title="✖ too short", description="minimum length is `8`.", color=discord.Color.red()))
        if length > 64:
            return await ctx.send(embed=discord.Embed(title="✖ too long", description="maximum length is `64`.", color=discord.Color.red()))

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pw = "".join(random.choices(chars, k=length))

        try:
            await ctx.author.send(embed=discord.Embed(
                title="√ generated password",
                description=f"```\n{pw}\n```",
                color=discord.Color.green()
            ).set_footer(text="sent via dms"))
            await ctx.send(embed=discord.Embed(title="√ password sent", description="check your dms", color=discord.Color.green()))
        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(title="✖ dms closed", description="i can't dm you, open your dms and try again", color=discord.Color.red()))

    @commands.command(name="dice", aliases=["roll"])
    async def dice(self, ctx, sides: int = 6):
        if sides < 2:
            return await ctx.send(embed=discord.Embed(title="✖ invalid sides", description="minimum is `2` sides", color=discord.Color.red()))
        if sides > 1000:
            return await ctx.send(embed=discord.Embed(title="✖ too many sides", description="maximum is `1000` sides", color=discord.Color.red()))

        result = random.randint(1, sides)
        await ctx.send(embed=discord.Embed(
            title=f"⚄ d{sides}",
            description=f"rolled **{result}**",
            color=discord.Color.blue()
        ))

async def setup(bot):
    await bot.add_cog(generators(bot))
