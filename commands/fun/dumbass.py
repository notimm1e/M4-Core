import discord
import random
import json
import os
from discord.ext import commands
from datetime import datetime

REASONS = [
    "microwaved a fork",
    "googled 'google'",
    "tried to reply to a voicemail",
    "locked themselves out of their own house twice in one day",
    "asked what time 12pm is",
    "argued with autocorrect and lost",
    "put the milk in the cupboard",
    "sent a screenshot of a text instead of forwarding it",
    "spent 10 minutes looking for their phone while on a call",
    "clicked 'forgot password' three times in a row",
    "tried to zoom in on a physical piece of paper",
    "said 'you too' when a waiter said enjoy your meal, then said it again",
    "walked into a push door",
    "replied all on a company-wide email",
    "set two alarms 1 minute apart instead of snoozing",
]

RANKS = ["bronze", "silver", "gold", "platinum", "diamond", "legendary", "cosmic"]
SEALS = ["🔏 certified", "📜 notarized", "⚖ legally binding", "🏛 government approved", "👁 witnessed"]
TRACKER_FILE = "dumbass.json"

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tracker(data):
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_rank(count):
    index = min((count - 1) // 2, len(RANKS) - 1)
    return RANKS[index]

class dumbass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dumbass", aliases=["certified", "cert"])
    async def dumbass(self, ctx, member: discord.Member = None):
        target = member or ctx.author

        data = load_tracker()
        guild_id = str(ctx.guild.id)
        user_id = str(target.id)

        if guild_id not in data:
            data[guild_id] = {}
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = 0

        data[guild_id][user_id] += 1
        count = data[guild_id][user_id]
        save_tracker(data)

        rank = get_rank(count)
        reason = random.choice(REASONS)
        seal = random.choice(SEALS)
        number = random.randint(10000, 99999)
        date = datetime.utcnow().strftime("%B %d, %Y")

        embed = discord.Embed(
            title="certificate of dumbass",
            color=discord.Color.yellow()
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.description = (
            f"*this is to certify that*\n"
            f"## {target.display_name}\n"
            f"*has been officially recognized as a certified dumbass*"
        )
        embed.add_field(name="reason", value=reason, inline=False)
        embed.add_field(name="rank", value=f"`{rank} tier`", inline=True)
        embed.add_field(name="times certified", value=f"`{count}`", inline=True)
        embed.add_field(name="certificate no.", value=f"`#{number}`", inline=True)
        embed.add_field(name="issued", value=date, inline=True)
        embed.set_footer(text=f"{seal} · issued by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @dumbass.error
    async def dumbass_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="✖ member not found", description="that member doesn't exist.", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(dumbass(bot))
