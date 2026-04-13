import discord
import json
import os
from discord.ext import commands

CONFIG_FILE = "confessions_config.json"

class Confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def save_config(self, guild_id, channel_id):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {}
        data[str(guild_id)] = channel_id
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def get_config(self, guild_id):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get(str(guild_id))
        return None

    @commands.command(name="setconfessions", description="set the channel for anonymous confessions")
    @commands.has_permissions(manage_guild=True)
    async def setconfessions(self, ctx, channel: discord.TextChannel):
        self.save_config(ctx.guild.id, channel.id)
        embed = discord.Embed(description=f"◈ confessions channel set to {channel.mention}", color=0x2b2d31)
        await ctx.send(embed=embed)

    @commands.command(name="confess", description="send an anonymous confession")
    async def confess(self, ctx, *, message: str):
        channel_id = self.get_config(ctx.guild.id)
        if not channel_id:
            return await ctx.send("⊘ confessions are not configured for this server.")

        channel = self.bot.get_channel(channel_id)
        if channel:
            await ctx.message.delete()
            embed = discord.Embed(
                title="╼ anonymous confession ╾",
                description=message.lower(),
                color=0x2b2d31
            )
            embed.set_footer(text="use !confess <message> to share")
            await channel.send(embed=embed)
            await ctx.author.send("◈ confession sent successfully.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Confessions(bot))
