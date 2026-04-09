import discord
import json
import os
from discord.ext import commands

SETTINGS_FILE = "server_settings.json"

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.load_settings()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    @commands.command(name="setwelcome")
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.data:
            self.data[guild_id] = {}

        self.data[guild_id]["welcome_channel"] = channel.id
        self.save_settings()
        await ctx.send(embed=discord.Embed(
            title="√ welcome channel set",
            description=f"welcome messages will now be sent to {channel.mention}.",
            color=discord.Color.green()
        ))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id not in self.data or "welcome_channel" not in self.data[guild_id]:
            return

        channel = self.bot.get_channel(self.data[guild_id]["welcome_channel"])
        if not channel:
            return

        embed = discord.Embed(
            title="welcome!",
            description=f"glad to have you here, {member.mention}.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"member #{member.guild.member_count}")
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(welcome(bot))