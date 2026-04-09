import discord
from discord.ext import commands
import os
from commands.admins_config import is_admin

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reloadall", aliases=["ra"])
    async def reload_all(self, ctx):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(
                description="⊘ unauthorized.", color=0xff4500
            ))

        status_msg = await ctx.send(embed=discord.Embed(
            title="⟳ reloading",
            description="reloading all extensions...",
            color=0x2b2d31
        ))

        reloaded_logs = []
        for root, dirs, files in os.walk("./commands"):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    path = os.path.relpath(os.path.join(root, file), ".").replace(os.sep, ".").removesuffix(".py")
                    try:
                        await self.bot.reload_extension(path)
                        reloaded_logs.append(f"√ `{path}`")
                    except Exception as e:
                        reloaded_logs.append(f"✖ `{path}`: {e}")

        log_chunk = "\n".join(reloaded_logs) or "no cogs found."
        if len(log_chunk) > 4000:
            log_chunk = log_chunk[:3997] + "..."

        await status_msg.edit(embed=discord.Embed(
            title="√ reloaded",
            description=log_chunk,
            color=0x57f287
        ))

async def setup(bot):
    await bot.add_cog(Admin(bot))
