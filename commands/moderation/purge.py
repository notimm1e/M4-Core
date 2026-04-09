import discord
import asyncio
import os
from datetime import datetime
from discord.ext import commands

class purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount < 1:
            return await ctx.send(embed=discord.Embed(
                title="✖ invalid amount",
                description="specify a number greater than 0.",
                color=discord.Color.red()
            ))

        try:
            retrieved_messages = []
            async for message in ctx.channel.history(limit=amount + 1):
                retrieved_messages.append(message)

            if not retrieved_messages:
                return

            self.log_to_file(ctx.guild.name, ctx.channel.name, retrieved_messages)

            deleted = await ctx.channel.delete_messages(retrieved_messages)
            count = max(0, len(deleted) - 1)

            confirm = await ctx.send(embed=discord.Embed(
                title="√ purged",
                description=f"cleaned `{count}` messages.",
                color=discord.Color.green()
            ))
            await asyncio.sleep(3)
            await confirm.delete()

        except Exception as e:
            print(f"internal error: {e}")

    def log_to_file(self, guild_name, channel_name, messages):
        if not os.path.exists("logs"):
            os.makedirs("logs")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/purge_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- purge log ---\n")
            f.write(f"guild: {guild_name} | channel: {channel_name}\n")
            f.write(f"timestamp: {timestamp}\n")
            f.write("-" * 30 + "\n\n")

            for msg in reversed(messages):
                if msg.content.startswith(f"{self.bot.command_prefix}purge") or \
                   msg.content.startswith(f"{self.bot.command_prefix}clear"):
                    continue

                time = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{time}] {msg.author} ({msg.author.id}): {msg.content}\n")
                if msg.attachments:
                    f.write(f"   files: {[a.url for a in msg.attachments]}\n")

async def setup(bot):
    await bot.add_cog(purge(bot))
