import discord
import random
from discord.ext import commands
from datetime import datetime, timedelta

CAUSES = [
    "tripped over a single grape",
    "aggressively yeeted off a chair by a pigeon",
    "book fell on head at terminal velocity",
    "consumed 47 energy drinks in one sitting",
    "argued with a vending machine and lost",
    "sat on a lego at exactly the wrong angle",
    "attacked by a very opinionated goose",
    "spontaneously combusted during a yawn",
    "choked on the concept of a monday",
    "brained by a rogue frisbee thrown in 1987",
    "disagreed with gravity one too many times",
    "opened too many chrome tabs simultaneously",
    "challenged a raccoon to a staring contest",
    "hit by a forgotten shopping cart in a parking lot",
    "made eye contact with the microwave for too long",
    "fell into a void while looking for their keys",
    "stepped on wet floor sign instead of avoiding it",
    "overloaded brain by reading terms and conditions",
]

class deathdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deathdate", aliases=["death", "rip"])
    async def deathdate(self, ctx, member: discord.Member = None):
        target = member or ctx.author

        future = datetime.now() + timedelta(days=random.randint(1, 365 * 60))
        date_str = future.strftime("%B %d, %Y")
        age = future.year - datetime.now().year
        cause = random.choice(CAUSES)
        last_words = random.choice([
            "\"wait, what?\"",
            "\"i probably should've seen this coming.\"",
            "\"hold on let me google this.\"",
            "\"that's fine.\"",
            "\"can we reschedule?\"",
            "\"technically i'm fine.\"",
            "\"no wait—\"",
        ])

        embed = discord.Embed(
            title=f"☠ death certificate · {target.display_name}",
            color=discord.Color.dark_gray()
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="date of passing", value=f"`{date_str}`", inline=True)
        embed.add_field(name="age", value=f"`{age}`", inline=True)
        embed.add_field(name="cause of death", value=cause, inline=False)
        embed.add_field(name="last words", value=last_words, inline=False)
        embed.set_footer(text="fictional. probably.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(deathdate(bot))
