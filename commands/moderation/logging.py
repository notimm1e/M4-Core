import discord
from discord.ext import commands

LOG_CHANNEL = 1495397971783712839

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, guild, embed):
        ch = guild.get_channel(LOG_CHANNEL)
        if ch:
            await ch.send(embed=embed)

    # ── bulk delete ─────────────────────────────

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if not messages:
            return
        embed = discord.Embed(title="🧹 bulk delete", color=0xff4500, timestamp=discord.utils.utcnow())
        embed.add_field(name="count", value=str(len(messages)))
        embed.add_field(name="channel", value=messages[0].channel.mention)
        await self.log(messages[0].guild, embed)

    # ── roles ───────────────────────────────────

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = discord.Embed(title="➕ role created", color=0x57f287, timestamp=discord.utils.utcnow())
        embed.add_field(name="role", value=role.mention)
        await self.log(role.guild, embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = discord.Embed(title="➖ role deleted", color=0xff4500, timestamp=discord.utils.utcnow())
        embed.add_field(name="role", value=role.name)
        await self.log(role.guild, embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        embed = discord.Embed(title="✏ role updated", color=0xf1c40f, timestamp=discord.utils.utcnow())
        if before.name != after.name:
            embed.add_field(name="name", value=f"{before.name} → {after.name}", inline=False)
        if before.permissions != after.permissions:
            embed.add_field(name="permissions changed", value="yes", inline=False)
        await self.log(after.guild, embed)

    # ── voice ───────────────────────────────────

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return

        embed = discord.Embed(color=0x5865f2, timestamp=discord.utils.utcnow())
        embed.add_field(name="user", value=member.mention)

        if before.channel is None:
            embed.title = "🔊 joined voice"
            embed.add_field(name="channel", value=after.channel.mention)
        elif after.channel is None:
            embed.title = "🔇 left voice"
            embed.add_field(name="channel", value=before.channel.mention)
        else:
            embed.title = "🔁 moved voice"
            embed.add_field(name="from", value=before.channel.mention)
            embed.add_field(name="to", value=after.channel.mention)

        await self.log(member.guild, embed)

    # ── avatar change ───────────────────────────

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_avatar != after.display_avatar:
            embed = discord.Embed(title="🖼 avatar changed", color=0x5865f2, timestamp=discord.utils.utcnow())
            embed.add_field(name="user", value=after.mention)
            embed.set_thumbnail(url=after.display_avatar.url)
            await self.log(after.guild, embed)

    # ── permissions ─────────────────────────────

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.overwrites != after.overwrites:
            embed = discord.Embed(title="🔐 permissions updated", color=0xf1c40f, timestamp=discord.utils.utcnow())
            embed.add_field(name="channel", value=after.mention)
            await self.log(after.guild, embed)

    # ── pins ────────────────────────────────────

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        embed = discord.Embed(title="📌 pins updated", color=0x5865f2, timestamp=discord.utils.utcnow())
        embed.add_field(name="channel", value=channel.mention)
        await self.log(channel.guild, embed)

    # ── emojis / stickers ───────────────────────

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        embed = discord.Embed(
            title="emoji updated",
            color=0x5865f2,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="before", value=str(len(before)))
        embed.add_field(name="after", value=str(len(after)))
        await self.log(guild, embed)

    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild, before, after):
        embed = discord.Embed(title="sticker updated", color=0x5865f2, timestamp=discord.utils.utcnow())
        embed.add_field(name="count", value=f"{len(before)} → {len(after)}")
        await self.log(guild, embed)

    # ── threads ─────────────────────────────────

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        embed = discord.Embed(title="🧵 thread created", color=0x57f287, timestamp=discord.utils.utcnow())
        embed.add_field(name="thread", value=thread.mention)
        await self.log(thread.guild, embed)

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        embed = discord.Embed(title="🧵 thread deleted", color=0xff4500, timestamp=discord.utils.utcnow())
        embed.add_field(name="name", value=thread.name)
        await self.log(thread.guild, embed)

    # ── webhooks ────────────────────────────────

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        embed = discord.Embed(title="🪝 webhooks updated", color=0xf1c40f, timestamp=discord.utils.utcnow())
        embed.add_field(name="channel", value=channel.mention)
        await self.log(channel.guild, embed)

    # ── integrations ────────────────────────────

    @commands.Cog.listener()
    async def on_integration_create(self, integration):
        embed = discord.Embed(title="➕ integration added", color=0x57f287)
        await self.log(integration.guild, embed)

    @commands.Cog.listener()
    async def on_integration_delete(self, integration):
        embed = discord.Embed(title="➖ integration removed", color=0xff4500)
        await self.log(integration.guild, embed)

    # ── stage instances ─────────────────────────

    @commands.Cog.listener()
    async def on_stage_instance_create(self, stage):
        embed = discord.Embed(title="🎤 stage started", color=0x57f287)
        await self.log(stage.guild, embed)

    @commands.Cog.listener()
    async def on_stage_instance_delete(self, stage):
        embed = discord.Embed(title="🎤 stage ended", color=0xff4500)
        await self.log(stage.guild, embed)

    # ── invites ─────────────────────────────────

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        embed = discord.Embed(title="➕ invite created", color=0x57f287)
        embed.add_field(name="code", value=invite.code)
        await self.log(invite.guild, embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        embed = discord.Embed(title="➖ invite deleted", color=0xff4500)
        embed.add_field(name="code", value=invite.code)
        await self.log(invite.guild, embed)

async def setup(bot):
    await bot.add_cog(Logger(bot))