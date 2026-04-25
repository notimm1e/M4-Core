import discord
import os
import yaml
from discord.ext import commands

def _load_cfg():
    path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.yaml"))
    with open(path) as f:
        return yaml.safe_load(f)

def _save_cfg(cfg):
    path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.yaml"))
    with open(path, "w") as f:
        yaml.dump(cfg, f)

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = _load_cfg()["channels"].get("welcome")

    @commands.command(name="setwelcome")
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel):
        cfg = _load_cfg()
        cfg["channels"]["welcome"] = channel.id
        _save_cfg(cfg)
        self.channel_id = channel.id
        await ctx.send(embed=discord.Embed(
            title="√ welcome channel set",
            description=f"welcome messages will now be sent to {channel.mention}",
            color=discord.Color.green()
        ))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.channel_id:
            return
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            return
        embed = discord.Embed(
            title="welcome!",
            description=f"glad to have you here, {member.mention}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"member #{member.guild.member_count}")
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(welcome(bot))
