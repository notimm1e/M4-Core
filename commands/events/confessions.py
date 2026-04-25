import discord
import os
import yaml
from discord.ext import commands

def _load_cfg():
    path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.yaml"))
    with open(path) as f:
        return yaml.safe_load(f)

_cfg = _load_cfg()
CONFESSION_CHANNEL_ID = _cfg["channels"]["confession"]

class Confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="confess", description="send an anonymous confession")
    async def confess(self, ctx, *, message: str):
        if ctx.guild is not None:
            return await ctx.send(embed=discord.Embed(description="⊘ use this command in dms.", color=0x2b2d31))
        channel = self.bot.get_channel(CONFESSION_CHANNEL_ID)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(CONFESSION_CHANNEL_ID)
            except:
                return await ctx.send(embed=discord.Embed(description="⊘ confession channel not found.", color=0x2b2d31))
        embed = discord.Embed(title="╼ anonymous confession ╾", description=message.lower(), color=0x2b2d31)
        embed.set_footer(text="use !confess in dms to share")
        await channel.send(embed=embed)
        try:
            await ctx.author.send(embed=discord.Embed(description="◈ confession sent successfully.", color=0x2b2d31), delete_after=5)
        except:
            pass

    @commands.command(name="setconfessions")
    @commands.has_permissions(manage_guild=True)
    async def set_confessions(self, ctx, channel: discord.TextChannel):
        global CONFESSION_CHANNEL_ID
        cfg_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.yaml"))
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f)
        cfg["channels"]["confession"] = channel.id
        with open(cfg_path, "w") as f:
            yaml.dump(cfg, f)
        CONFESSION_CHANNEL_ID = channel.id
        await ctx.send(embed=discord.Embed(
            description=f"√ confessions channel set to {channel.mention}.",
            color=0x57f287
        ))

async def setup(bot):
    await bot.add_cog(Confessions(bot))
