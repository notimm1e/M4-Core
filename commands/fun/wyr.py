import discord
import random
from discord.ext import commands

DILEMMAS = [
    ("never use the internet again", "never watch TV or movies again"),
    ("be able to fly", "be invisible"),
    ("always be 10 minutes late", "always be 20 minutes early"),
    ("have unlimited money but no friends", "have unlimited friends but no money"),
    ("know how you'll die", "know when you'll die"),
    ("be famous but hated", "be unknown but loved"),
    ("eat only sweet food forever", "eat only savory food forever"),
    ("be able to speak every language", "be able to play every instrument"),
    ("live in extreme heat", "live in extreme cold"),
    ("have no phone for a year", "have no music for a year"),
    ("always tell the truth", "always lie"),
    ("be able to read minds", "be able to see the future"),
    ("never sleep again", "never dream again"),
    ("fight 100 duck-sized horses", "fight 1 horse-sized duck"),
    ("have fingers as toes", "have toes as fingers"),
    ("only whisper forever", "only shout forever"),
    ("lose all your memories from birth to 18", "lose all your memories from the last 5 years"),
    ("always itch but never scratch", "always feel like sneezing but never sneeze"),
    ("be able to teleport", "be able to time travel"),
    ("never be able to use social media", "never be able to watch youtube"),
]

class WouldYouRather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wyr", aliases=["wouldyourather"], description="get a random would you rather question")
    async def wyr(self, ctx):
        a, b = random.choice(DILEMMAS)
        embed = discord.Embed(
            title="◈ would you rather...",
            color=0x5865f2
        )
        embed.add_field(name="🅐", value=a, inline=True)
        embed.add_field(name="🅑", value=b, inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🅐")
        await msg.add_reaction("🅑")

async def setup(bot):
    await bot.add_cog(WouldYouRather(bot))
