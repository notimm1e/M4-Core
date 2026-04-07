import discord
import asyncio
import os
from datetime import datetime
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Deletes messages silently and logs them to a local file."""
        if amount < 1:
            return await ctx.send("❌ Specify a number greater than 0.")

        try:
            # 1. Fetch history for the log before deleting
            retrieved_messages = []
            async for message in ctx.channel.history(limit=amount + 1):
                retrieved_messages.append(message)

            if not retrieved_messages:
                return

            # 2. Silently log to local file
            self.log_to_file(ctx.guild.name, ctx.channel.name, retrieved_messages)

            # 3. Perform the deletion
            deleted = await ctx.channel.delete_messages(retrieved_messages)
            
            # 4. Standard public confirmation (No mention of logs)
            count = len(deleted) - 1
            confirm = await ctx.send(f"✅ Cleaned {max(0, count)} messages.")
            await asyncio.sleep(3)
            await confirm.delete()

        except Exception as e:
            # Errors only print to your Terminal, never to Discord
            print(f"Internal Error: {e}")

    def log_to_file(self, guild_name, channel_name, messages):
        """Writes data to the local /logs folder."""
        if not os.path.exists("logs"):
            os.makedirs("logs")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/purge_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- INTERNAL PURGE LOG ---\n")
            f.write(f"Guild: {guild_name} | Channel: {channel_name}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("-" * 30 + "\n\n")

            for msg in reversed(messages):
                # We skip the command itself in the final log
                if msg.content.startswith(f"{self.bot.command_prefix}purge") or \
                   msg.content.startswith(f"{self.bot.command_prefix}clear"):
                    continue
                
                time = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{time}] {msg.author} ({msg.author.id}): {msg.content}\n")
                if msg.attachments:
                    f.write(f"   Files: {[a.url for a in msg.attachments]}\n")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Purge(bot))