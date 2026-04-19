import discord
from discord.ext import commands
import base64 as b64

class Base64(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="b64", aliases=["base64"], description="encode or decode base64")
    async def b64_cmd(self, ctx, action: str, *, text: str):
        action = action.lower()
        if action not in ("encode", "decode"):
            return await ctx.send(embed=discord.Embed(
                description="✖ usage: `!b64 encode/decode <text>`",
                color=0xff4500
            ))

        try:
            if action == "encode":
                result = b64.b64encode(text.encode()).decode()
                label = "◈ encoded"
            else:
                result = b64.b64decode(text.encode()).decode()
                label = "◈ decoded"
        except Exception:
            return await ctx.send(embed=discord.Embed(
                description="✖ invalid input for decoding.",
                color=0xff4500
            ))

        if len(result) > 1900:
            result = result[:1900] + "..."

        embed = discord.Embed(color=0x2b2d31)
        embed.add_field(name="◈ input", value=f"`{text[:200]}`", inline=False)
        embed.add_field(name=label, value=f"`{result}`", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Base64(bot))
