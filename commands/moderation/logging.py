import discord
from discord.ext import commands
from collections import defaultdict, deque

LOG_CHANNEL = 1495397971783712839
GUILD_ID = 1483246510337425483

class Logger(commands.Cog):
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
            embed = discord.Embed(
                title="⚙ eval used",
                color=0x5865f2,
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="user", value=ctx.author.mention)
            embed.add_field(name="channel", value=ctx.channel.mention)

            content = ctx.message.content[:1000] if ctx.message.content else "*no content*"
            embed.add_field(name="input", value=f"```\n{content}\n```", inline=False)

            await self.log(ctx.guild, embed)

    @commands.command()
    async def stats(self, ctx):
        if ctx.guild.id != GUILD_ID:
            return
        top_cmds = sorted(self.cmd_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        top_users = sorted(self.user_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        embed = discord.Embed(color=0x5865f2)
        embed.add_field(name="◈ top commands", value="\n".join(f"{k}: {v}" for k,v in top_cmds) or "none", inline=False)
        embed.add_field(name="◈ top users", value="\n".join(f"<@{k}>: {v}" for k,v in top_users) or "none", inline=False)
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
        embed = discord.Embed(title="✏ role updated", color=0xf1c40f)
        if before.name != after.name:
            embed.add_field(name="name", value=f"{before.name} → {after.name}", inline=False)
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

async def setup(bot):
    await bot.add_cog(Logger(bot))