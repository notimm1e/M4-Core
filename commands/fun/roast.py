import discord
import random
from discord.ext import commands

ROASTS = [
    "if brains were dynamite, you couldn't blow your hat off.",
    "you're the human equivalent of a participation trophy.",
    "i'd roast you harder but my mom said i'm not allowed to burn trash.",
    "you have the charisma of a wet sock.",
    "somewhere out there a tree is tirelessly producing oxygen for you. you owe it an apology.",
    "you're not stupid, you just have bad luck thinking.",
    "your wifi password is probably your only secret.",
    "you're like a cloud. when you disappear, it's a beautiful day.",
    "if you were a spice, you'd be flour.",
    "you have something on your chin. no, the third one.",
]

class roast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roast")
    async def roast(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        embed = discord.Embed(
            title=f"🔥 roasting {target.display_name}",
            description=random.choice(ROASTS),
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(roast(bot))
