import discord
from discord.ext import commands
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # The IDs you provided
        self.authorized_users = [779653730978103306, 500683600614785025]

    def is_authorized(self, user_id):
        return user_id in self.authorized_users

    @commands.command(name="reloadall", aliases=["ra"])
    async def reload_all(self, ctx):
        if not self.is_authorized(ctx.author.id):
            return await ctx.send("❌ You do not have permission to reload the bot.")

        reloaded_logs = []
        
        # Create the initial "Processing" embed
        embed = discord.Embed(
            title="Bot Reload",
            description="🔄 *Reloading all extensions...*",
            color=discord.Color.gold()
        )
        status_msg = await ctx.send(embed=embed)

        # This assumes your structure is commands/folder/file.py
        # It loops through your folders to find all cogs
        for root, dirs, files in os.walk("./commands"):
            for file in files:
                if file.endswith(".py"):
                    # Convert file path to python dot notation
                    path = os.path.join(root, file).replace("./", "").replace("/", ".").replace(".py", "")
                    try:
                        await self.bot.reload_extension(path)
                        reloaded_logs.append(f"✅ `{path}`")
                    except Exception as e:
                        reloaded_logs.append(f"❌ `{path}`: {e}")

        # Update the embed with the final logs
        final_embed = discord.Embed(
            title="Bot Reload Complete",
            description="\n".join(reloaded_logs) if reloaded_logs else "No extensions found.",
            color=discord.Color.green()
        )
        final_embed.set_footer(text=f"Triggered by {ctx.author}")
        
        await status_msg.edit(embed=final_embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))

