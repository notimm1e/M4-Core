import discord
from discord.ext import commands
from deep_translator import GoogleTranslator, exceptions

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="translate", aliases=["tr"], description="translate text to english (auto-detects source language)")
    async def translate(self, ctx, *, text: str):
        try:
            result = GoogleTranslator(source="auto", target="en").translate(text)

            embed = discord.Embed(color=0x2b2d31)
            embed.add_field(name="◈ input", value=text, inline=False)
            embed.add_field(name="◈ translation", value=result, inline=False)
            embed.set_footer(text="m4-core · auto-detected source")

            await ctx.send(embed=embed)

        except exceptions.LanguageNotSupportedException:
            await ctx.send(embed=discord.Embed(
                description="✖ couldn't detect the language.",
                color=0xff4500
            ))
        except Exception as e:
            await ctx.send(embed=discord.Embed(
                description=f"✖ translation failed: {e}",
                color=0xff4500
            ))

async def setup(bot):
    await bot.add_cog(Translate(bot))
