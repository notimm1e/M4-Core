import discord
from discord.ext import commands
from collections import defaultdict, deque

LOG_CHANNEL = 1495397971783712839
CONSOLE_CHANNEL = 1495411242859364474
GUILD_ID = 1483246510337425483

class Logger(commands.Cog):
    # List of all permission names (keeps the code compatible across discord.py versions)
    PERMISSION_NAMES = [
        "create_instant_invite",
        "kick_members",
        "ban_members",
        "administrator",
        "manage_channels",
        "manage_guild",
        "add_reactions",
        "view_audit_log",
        "priority_speaker",
        "stream",
        "view_channel",
        "send_messages",
        "send_tts_messages",
        "manage_messages",
        "embed_links",
        "attach_files",
        "read_message_history",
        "mention_everyone",
        "use_external_emojis",
        "view_guild_insights",
        "connect",
        "speak",
        "mute_members",
        "deafen_members",
        "move_members",
        "use_vad",
        "change_nickname",
        "manage_nicknames",
        "manage_roles",
        "manage_webhooks",
        "manage_emojis_and_stickers",
        "use_application_commands",
        "request_to_speak",
        "manage_events",
        "manage_threads",
        "create_public_threads",
        "create_private_threads",
        "use_external_stickers",
        "send_messages_in_threads",
        "use_embedded_activities",
        "moderate_members",
        "send_voice_messages",
    ]

    def __init__(self, bot):
        self.bot = bot
        self.cmd_usage = defaultdict(int)
        self.user_usage = defaultdict(int)
        self.deleted_cache = deque(maxlen=100)

    async def log(self, guild, embed):
        if not guild or guild.id != GUILD_ID:
            return
        ch = guild.get_channel(LOG_CHANNEL)
        if ch:
            await ch.send(embed=embed)

    # ──────────────────────────────────────────────────────────────
    # Helper: Role permission diff (simple + / - like before)
    # ──────────────────────────────────────────────────────────────
    def _get_permission_diff(self, before: discord.Role, after: discord.Role) -> list[str]:
        changes = []
        for perm in self.PERMISSION_NAMES:
            try:
                b_val = getattr(before.permissions, perm)
                a_val = getattr(after.permissions, perm)
                if b_val != a_val:
                    sign = "+" if a_val else "-"
                    changes.append(f"{sign} {perm.replace('_', ' ')}")
            except AttributeError:
                continue
        return changes

    # ──────────────────────────────────────────────────────────────
    # Helper: Channel permission overwrite diff (simple + / - / reset)
    # ──────────────────────────────────────────────────────────────
    def _get_overwrite_diff(self, before_ow: discord.PermissionOverwrite, after_ow: discord.PermissionOverwrite) -> list[str]:
        changes = []
        for perm in self.PERMISSION_NAMES:
            try:
                b_val = getattr(before_ow, perm, None)
                a_val = getattr(after_ow, perm, None)
                if b_val != a_val:
                    if a_val is True:
                        changes.append(f"+ {perm.replace('_', ' ')}")
                    elif a_val is False:
                        changes.append(f"- {perm.replace('_', ' ')}")
                    elif a_val is None and b_val is not None:
                        changes.append(f"↩ {perm.replace('_', ' ')} (reset to @everyone)")
            except AttributeError:
                continue
        return changes

    # ──────────────────────────────────────────────────────────────
    # Existing listeners (only message edit reverted to simple before/after)
    # ──────────────────────────────────────────────────────────────
    @commands.Cog.listener()
    async def on_command(self, ctx):
        if not ctx.guild or ctx.guild.id != GUILD_ID:
            return
        if ctx.command:
            self.cmd_usage[ctx.command.name] += 1
            self.user_usage[ctx.author.id] += 1

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if not ctx.guild or ctx.guild.id != GUILD_ID:
            return
        if ctx.command and ctx.command.name == "eval":
            raw = ctx.message.content
            parts = raw.split(" ", 1)
            code = parts[1] if len(parts) > 1 else "*no code*"
            embed = discord.Embed(
                title="⚙ eval used",
                color=0x5865f2,
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="user", value=ctx.author.mention)
            embed.add_field(name="channel", value=ctx.channel.mention)
            embed.add_field(name="input", value=f"```\n{code[:1000]}\n```", inline=False)
            await self.log(ctx.guild, embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        if message.guild.id != GUILD_ID:
            return
        if message.channel.id == CONSOLE_CHANNEL:
            embed = discord.Embed(
                title="🖥 console input",
                color=0x2b2d31,
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="user", value=message.author.mention)
            embed.add_field(name="input", value=f"```\n{message.content[:1000]}\n```", inline=False)
            await self.log(message.guild, embed)

    @commands.command()
    async def stats(self, ctx):
        if ctx.guild.id != GUILD_ID:
            return
        top_cmds = sorted(self.cmd_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        top_users = sorted(self.user_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        embed = discord.Embed(color=0x5865f2)
        embed.add_field(name="◈ top commands", value="\n".join(f"{k}: {v}" for k, v in top_cmds) or "none", inline=False)
        embed.add_field(name="◈ top users", value="\n".join(f"<@{k}>: {v}" for k, v in top_users) or "none", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def restore(self, ctx):
        if ctx.guild.id != GUILD_ID:
            return
        if not self.deleted_cache:
            return await ctx.send("nothing to restore")
        msg = self.deleted_cache[-1]
        content = msg["content"] or "*no content*"
        files = [await a.to_file() for a in msg["attachments"]]
        await ctx.send(content=content, files=files)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.guild.id != GUILD_ID or message.author.bot:
            return
        self.deleted_cache.append({
            "content": message.content,
            "attachments": message.attachments
        })
        embed = discord.Embed(title="🗑 message deleted", color=0xff4500, timestamp=discord.utils.utcnow())
        embed.add_field(name="user", value=message.author.mention)
        embed.add_field(name="channel", value=message.channel.mention)
        if message.content:
            embed.add_field(name="content", value=message.content[:1000], inline=False)
        if message.attachments:
            embed.add_field(name="attachments", value="\n".join(a.url for a in message.attachments), inline=False)
        await self.log(message.guild, embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if not messages or messages[0].guild.id != GUILD_ID:
            return
        embed = discord.Embed(title="🧹 bulk delete", color=0xff4500, timestamp=discord.utils.utcnow())
        embed.add_field(name="count", value=str(len(messages)))
        embed.add_field(name="channel", value=messages[0].channel.mention)
        await self.log(messages[0].guild, embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild or before.guild.id != GUILD_ID or before.author.bot:
            return
        if before.content == after.content:
            return
        embed = discord.Embed(title="✏ message edited", color=0xf1c40f, timestamp=discord.utils.utcnow())
        embed.add_field(name="user", value=before.author.mention)
        embed.add_field(name="channel", value=before.channel.mention)
        # Reverted to simple before/after (git-style diff removed as requested)
        embed.add_field(name="before", value=before.content[:1000] or "*empty*", inline=False)
        embed.add_field(name="after", value=after.content[:1000] or "*empty*", inline=False)
        await self.log(before.guild, embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if guild.id != GUILD_ID:
            return
        embed = discord.Embed(title="🔨 user banned", color=0xff0000)
        embed.add_field(name="user", value=str(user))
        await self.log(guild, embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if guild.id != GUILD_ID:
            return
        embed = discord.Embed(title="🔓 user unbanned", color=0x57f287)
        embed.add_field(name="user", value=str(user))
        await self.log(guild, embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = discord.Embed(title="➕ role created", color=0x57f287)
        embed.add_field(name="role", value=role.mention)
        await self.log(role.guild, embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = discord.Embed(title="➖ role deleted", color=0xff4500)
        embed.add_field(name="role", value=role.name)
        await self.log(role.guild, embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        embed = discord.Embed(title="✏ role updated", color=0xf1c40f, timestamp=discord.utils.utcnow())
        changed = False

        if before.name != after.name:
            embed.add_field(name="name", value=f"{before.name} → {after.name}", inline=False)
            changed = True

        perm_changes = self._get_permission_diff(before, after)
        if perm_changes:
            embed.add_field(name="permissions", value="\n".join(perm_changes[:25]), inline=False)
            changed = True

        if changed:
            await self.log(after.guild, embed)

    # ──────────────────────────────────────────────────────────────
    # NEW: Channel permission logging (overwrites + name change)
    # ──────────────────────────────────────────────────────────────
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        if before.guild.id != GUILD_ID:
            return

        embed = discord.Embed(title="📡 channel updated", color=0xf1c40f, timestamp=discord.utils.utcnow())
        embed.add_field(name="channel", value=after.mention, inline=False)
        changed = False

        # Name change
        if before.name != after.name:
            embed.add_field(name="name", value=f"{before.name} → {after.name}", inline=False)
            changed = True

        # Permission overwrite changes
        before_overwrites = {k: v for k, v in before.overwrites.items()}
        after_overwrites = {k: v for k, v in after.overwrites.items()}

        # New / changed overwrites
        for target, after_perm in after_overwrites.items():
            target_str = target.mention if hasattr(target, "mention") else target.name

            if target not in before_overwrites:
                # Brand new overwrite
                embed.add_field(
                    name=f"➕ new permissions for {target_str}",
                    value="overridden (check audit log for full list)",
                    inline=False
                )
                changed = True
            else:
                before_perm = before_overwrites[target]
                perm_changes = self._get_overwrite_diff(before_perm, after_perm)
                if perm_changes:
                    embed.add_field(
                        name=f"✏ permissions updated for {target_str}",
                        value="\n".join(perm_changes[:20]),
                        inline=False
                    )
                    changed = True

        # Removed overwrites
        for target in list(before_overwrites.keys()):
            if target not in after_overwrites:
                target_str = target.mention if hasattr(target, "mention") else target.name
                embed.add_field(
                    name=f"➖ permissions removed for {target_str}",
                    value="reset to @everyone",
                    inline=False
                )
                changed = True

        if changed:
            await self.log(after.guild, embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id != GUILD_ID or before.channel == after.channel:
            return
        embed = discord.Embed(color=0x5865f2)
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

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        embed = discord.Embed(title="🧵 thread created", color=0x57f287)
        embed.add_field(name="thread", value=thread.mention)
        await self.log(thread.guild, embed)

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        embed = discord.Embed(title="🧵 thread deleted", color=0xff4500)
        embed.add_field(name="name", value=thread.name)
        await self.log(thread.guild, embed)

    # ──────────────────────────────────────────────────────────────
    # Additional sensible logging (unchanged)
    # ──────────────────────────────────────────────────────────────
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != GUILD_ID:
            return
        embed = discord.Embed(title="👋 member joined", color=0x57f287, timestamp=discord.utils.utcnow())
        embed.add_field(name="user", value=member.mention)
        await self.log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != GUILD_ID:
            return
        embed = discord.Embed(title="🚪 member left", color=0xff4500, timestamp=discord.utils.utcnow())
        embed.add_field(name="user", value=str(member))
        await self.log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id != GUILD_ID:
            return
        embed = discord.Embed(title="✏ member updated", color=0xf1c40f, timestamp=discord.utils.utcnow())
        embed.add_field(name="user", value=before.mention)
        changed = False

        if before.nick != after.nick:
            embed.add_field(
                name="nickname",
                value=f"{before.nick or '*none*'} → {after.nick or '*none*'}",
                inline=False
            )
            changed = True

        if before.roles != after.roles:
            added = [r.mention for r in after.roles if r not in before.roles and not r.is_default()]
            removed = [r.mention for r in before.roles if r not in after.roles and not r.is_default()]
            if added:
                embed.add_field(name="roles added", value=", ".join(added) or "none", inline=False)
                changed = True
            if removed:
                embed.add_field(name="roles removed", value=", ".join(removed) or "none", inline=False)
                changed = True

        if changed:
            await self.log(before.guild, embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.id != GUILD_ID:
            return
        embed = discord.Embed(title="🏠 guild updated", color=0xf1c40f, timestamp=discord.utils.utcnow())
        changed = False

        if before.name != after.name:
            embed.add_field(name="name", value=f"{before.name} → {after.name}", inline=False)
            changed = True

        if before.icon != after.icon:
            embed.add_field(name="icon", value="changed" if after.icon else "removed", inline=False)
            changed = True

        if changed:
            await self.log(after, embed)

async def setup(bot):
    await bot.add_cog(Logger(bot))