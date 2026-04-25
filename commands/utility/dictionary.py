import discord
import os
import yaml
import aiohttp
from discord.ext import commands

def _load_cfg():
    path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.yaml"))
    with open(path) as f:
        return yaml.safe_load(f)

_cfg = _load_cfg()
ALLOWED_CHANNEL = _cfg["channels"]["dictionary"]

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dict", aliases=["dictionary"], description="look up a term on urban dictionary")
    async def dict(self, ctx, *, term: str):
        if ctx.channel.id != ALLOWED_CHANNEL:
            return await ctx.send(embed=discord.Embed(
                description="⊘ you can only use this in a designated dictionary channel to prevent inappropriate words.",
                color=0xff4500
            ), delete_after=5)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.urbandictionary.com/v0/define", params={"term": term}) as resp:
                if resp.status != 200:
                    return await ctx.send(embed=discord.Embed(description="✖ couldn't reach urban dictionary.", color=0xff4500))
                data = await resp.json()
        results = data.get("list", [])
        if not results:
            return await ctx.send(embed=discord.Embed(description=f"✖ no results for **{term}**.", color=0xff4500))
        top = results[0]
        definition = top["definition"].replace("[", "").replace("]", "")
        example = top["example"].replace("[", "").replace("]", "")
        if len(definition) > 1024:
            definition = definition[:1021] + "..."
        if len(example) > 512:
            example = example[:509] + "..."
        embed = discord.Embed(title=top["word"], url=top["permalink"], color=0x2b2d31)
        embed.add_field(name="◈ definition", value=definition, inline=False)
        if example.strip():
            embed.add_field(name="◈ example", value=f"*{example}*", inline=False)
        embed.set_footer(text=f"👍 {top['thumbs_up']:,}  👎 {top['thumbs_down']:,} · urban dictionary")
        await ctx.send(embed=embed)

    @commands.command(name="setdictionary")
    @commands.has_permissions(manage_guild=True)
    async def set_dictionary(self, ctx, channel: discord.TextChannel):
        global ALLOWED_CHANNEL
        cfg_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.yaml"))
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f)
        cfg["channels"]["dictionary"] = channel.id
        with open(cfg_path, "w") as f:
            yaml.dump(cfg, f)
        ALLOWED_CHANNEL = channel.id
        await ctx.send(embed=discord.Embed(
            description=f"√ dictionary channel set to {channel.mention}.",
            color=0x57f287
        ))

async def setup(bot):
    await bot.add_cog(Dictionary(bot))
