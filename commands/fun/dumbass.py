import discord
import msgpack
import os
import random
from discord.ext import commands
from datetime import datetime

REASONS = [
    "microwaved a fork",
    "googled 'google'",
    "sent a text to the wrong person and didn't realize it",
    "tried to reply to a voicemail",
    "locked themselves out of their own house twice in one day",
    "asked what time 12pm is",
    "tried to use a computer without a mouse",
    "argued with autocorrect and lost",
    "put the milk in the cupboard",
    "sent a screenshot of a text instead of forwarding it",
    "spent 10 minutes looking for their phone while on a call",
    "clicked 'forgot password' three times in a row",
    "tried to zoom in on a physical piece of paper",
    "said 'you too' when a waiter said enjoy your meal, then said it again",
    "walked into a push door",
    "got into the passenger seat of their own car",
    "tripped over nothing and blamed the floor",
    "replied all on a company-wide email",
    "accidentally sent a meme in a professional chat",
    "used the wrong emoji in a message and didn't know how to react",
    "tried to unlock their phone with their face while wearing sunglasses",
    "forgot how to spell a common word and had to look it up",
    "laughed at a joke they didn't understand and then had to pretend they got it",
    "started a sentence and then forgot what they were going to say",
    "set two alarms 1 minute apart instead of snoozing",
]

RANKS = ["bronze", "silver", "gold", "platinum", "diamond", "legendary", "cosmic"]
SEALS = ["🔏 certified", "📜 notarized", "⚖ legally binding", "🏛 government approved", "👁 witnessed"]
TRACKER_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "dumbass.msgpack"))

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "rb") as f:
                data = msgpack.unpack(f, raw=False)
                return data if data else {}
        except (msgpack.UnpackException, OSError):
            pass
    return {}

def save_tracker(data):
    tmp = TRACKER_FILE + ".tmp"
    with open(tmp, "wb") as f:
        msgpack.pack(data, f, use_bin_type=True)
    os.replace(tmp, TRACKER_FILE)

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

async def setup(bot):
    await bot.add_cog(dumbass(bot))