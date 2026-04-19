import discord
from discord.ext import commands
from datetime import timezone

LOG_CHANNEL = 1495397971783712839

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, guild, embed):
        ch = guild.get_channel(LOG_CHANNEL)
        if ch:
            await ch.send(embed=embed)

    # ── messages ──────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return
        embed = discord.Embed(
            title="🗑 message deleted",
            color=0xff4500,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="author", value=f"{message.author.mention} (`{message.author.id}`)", inline=True)
        embed.add_field(name="channel", value=message.channel.mention, inline=True)
        if message.content:
            embed.add_field(name="content", value=message.content[:1024], inline=False)
        if message.attachments:
            embed.add_field(name="attachments", value="\n".join(a.url for a in message.attachments), inline=False)
        embed.set_footer(text=f"message id: {message.id}")
        await self.log(message.guild, embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild or before.content == after.content:
            return
        embed = discord.Embed(
            title="✏ message edited",
            color=0xf1c40f,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="author", value=f"{before.author.mention} (`{before.author.id}`)", inline=True)
        embed.add_field(name="channel", value=before.channel.mention, inline=True)
        embed.add_field(name="before", value=before.content[:512] or "*(empty)*", inline=False)
        embed.add_field(name="after", value=after.content[:512] or "*(empty)*", inline=False)
        embed.add_field(name="jump", value=f"[view]({after.jump_url})", inline=True)
        embed.set_footer(text=f"message id: {before.id}")
        await self.log(before.guild, embed)

    # ── members ───────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="📥 member joined",
            color=0x57f287,
            timestamp=discord.utils.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="user", value=f"{member.mention} (`{member.id}`)", inline=True)
        embed.add_field(name="account created", value=discord.utils.format_dt(member.created_at, "R"), inline=True)
        embed.set_footer(text=f"member count: {member.guild.member_count}")
        await self.log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="📤 member left",
            color=0xff4500,
            timestamp=discord.utils.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="user", value=f"{member.mention} (`{member.id}`)", inline=True)
        roles = [r.mention for r in member.roles if r != member.guild.default_role]
        if roles:
            embed.add_field(name="roles", value=" ".join(roles)[:1024], inline=False)
        embed.set_footer(text=f"member count: {member.guild.member_count}")
        await self.log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles and before.nick == after.nick:
            return

        embed = discord.Embed(
            title="👤 member updated",
            color=0x5865f2,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="user", value=f"{after.mention} (`{after.id}`)", inline=False)

        if before.nick != after.nick:
            embed.add_field(name="nickname", value=f"`{before.nick}` → `{after.nick}`", inline=False)

        added = [r for r in after.roles if r not in before.roles]
        removed = [r for r in before.roles if r not in after.roles]
        if added:
            embed.add_field(name="roles added", value=" ".join(r.mention for r in added), inline=False)
        if removed:
            embed.add_field(name="roles removed", value=" ".join(r.mention for r in removed), inline=False)

        await self.log(after.guild, embed)

    # ── moderation (audit log) ────────────────────────────────

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        guild = entry.guild
        action = entry.action
        user = entry.user
        target = entry.target

        embed = None

        if action == discord.AuditLogAction.ban:
            embed = discord.Embed(title="🔨 member banned", color=0xff4500, timestamp=discord.utils.utcnow())
            embed.add_field(name="user", value=f"{target.mention} (`{target.id}`)", inline=True)
            embed.add_field(name="by", value=f"{user.mention}", inline=True)
            embed.add_field(name="reason", value=entry.reason or "no reason provided", inline=False)

        elif action == discord.AuditLogAction.unban:
            embed = discord.Embed(title="✅ member unbanned", color=0x57f287, timestamp=discord.utils.utcnow())
            embed.add_field(name="user", value=f"{target.mention} (`{target.id}`)", inline=True)
            embed.add_field(name="by", value=f"{user.mention}", inline=True)

        elif action == discord.AuditLogAction.kick:
            embed = discord.Embed(title="👢 member kicked", color=0xf1c40f, timestamp=discord.utils.utcnow())
            embed.add_field(name="user", value=f"{target.mention} (`{target.id}`)", inline=True)
            embed.add_field(name="by", value=f"{user.mention}", inline=True)
            embed.add_field(name="reason", value=entry.reason or "no reason provided", inline=False)

        elif action == discord.AuditLogAction.member_update:
            if hasattr(entry.changes, "timed_out_until"):
                timed_out = entry.changes.after.timed_out_until
                if timed_out:
                    embed = discord.Embed(title="⏱ member timed out", color=0xf1c40f, timestamp=discord.utils.utcnow())
                    embed.add_field(name="user", value=f"{target.mention} (`{target.id}`)", inline=True)
                    embed.add_field(name="by", value=f"{user.mention}", inline=True)
                    embed.add_field(name="until", value=discord.utils.format_dt(timed_out, "F"), inline=False)
                    embed.add_field(name="reason", value=entry.reason or "no reason provided", inline=False)
                else:
                    embed = discord.Embed(title="✅ timeout removed", color=0x57f287, timestamp=discord.utils.utcnow())
                    embed.add_field(name="user", value=f"{target.mention} (`{target.id}`)", inline=True)
                    embed.add_field(name="by", value=f"{user.mention}", inline=True)

        elif action == discord.AuditLogAction.channel_update:
            embed = discord.Embed(title="📝 channel updated", color=0x5865f2, timestamp=discord.utils.utcnow())
            embed.add_field(name="channel", value=getattr(target, "mention", str(target)), inline=True)
            embed.add_field(name="by", value=f"{user.mention}", inline=True)

        if embed:
            embed.set_footer(text=f"by {user} ({user.id})")
            await self.log(guild, embed)

    # ── channels ──────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title="➕ channel created", color=0x57f287, timestamp=discord.utils.utcnow())
        embed.add_field(name="name", value=channel.mention, inline=True)
        embed.add_field(name="type", value=str(channel.type), inline=True)
        await self.log(channel.guild, embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title="➖ channel deleted", color=0xff4500, timestamp=discord.utils.utcnow())
        embed.add_field(name="name", value=f"`#{channel.name}`", inline=True)
        embed.add_field(name="type", value=str(channel.type), inline=True)
        await self.log(channel.guild, embed)

async def setup(bot):
    await bot.add_cog(Logger(bot))