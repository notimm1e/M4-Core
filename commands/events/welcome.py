import discord
import json
import os
from discord.ext import commands

# File to store server-specific settings
SETTINGS_FILE = "server_settings.json"

class Welcome(commands.Cog):
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
        """Sets the welcome channel for this server."""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.data:
            self.data[guild_id] = {}
        
        self.data[guild_id]["welcome_channel"] = channel.id
        self.save_settings()
        await ctx.send(f"✅ Welcome messages will now be sent to {channel.mention}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Triggers when a member joins a server."""
        guild_id = str(member.guild.id)
        
        # Check if this specific server has a welcome channel set
        if guild_id in self.data and "welcome_channel" in self.data[guild_id]:
            channel_id = self.data[guild_id]["welcome_channel"]
            channel = self.bot.get_channel(channel_id)
            
            if channel:
                embed = discord.Embed(
                    title="Welcome!",
                    description=f"Happy to have you here, {member.mention}!",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f"Member Count: {member.guild.member_count}")
                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))