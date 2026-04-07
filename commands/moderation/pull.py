import discord
from discord.ext import commands
import asyncio
import os

AUTHORIZED = {779653730978103306, 500683600614785025}

class GitManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def reload_all_extensions(self):
        results = []
        for root, _, files in os.walk("./commands"):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    module_path = rel_path.replace(os.sep, ".").removesuffix(".py")
                    try:
                        await self.bot.reload_extension(module_path)
                        results.append(f"√ `{module_path}`")
                    except commands.ExtensionNotLoaded:
                        try:
                            await self.bot.load_extension(module_path)
                            results.append(f"√ `{module_path}` (new)")
                        except Exception as e:
                            results.append(f"✖ `{module_path}`: {e}")
                    except Exception as e:
                        results.append(f"✖ `{module_path}`: {e}")
        return results

    @commands.command(name="pull")
    async def pull(self, ctx, branch: str = "canary"):
        if ctx.author.id not in AUTHORIZED:
            return

        branch = branch.lower()
        if branch not in ["canary", "main"]:
            return await ctx.send("✖ use `!pull canary` or `!pull main`.")

        status_msg = await ctx.send(embed=discord.Embed(
            title="⟳ pulling",
            description=f"pulling and updating bot internals from **{branch}**...",
            color=discord.Color.blue()
        ))

        try:
            process = await asyncio.create_subprocess_shell(
                f"git fetch origin && git reset --hard origin/{branch}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(stderr.decode())

            reload_logs = await self.reload_all_extensions()

            git_log = stdout.decode().strip()
            if len(git_log) > 500:
                git_log = "..." + git_log[-497:]
            if not git_log:
                git_log = "already up to date."

            log_chunk = "\n".join(reload_logs)
            if len(log_chunk) > 1024:
                log_chunk = log_chunk[:1020] + "..."

            embed = discord.Embed(
                title="√ pulled!",
                description=f"pulled and updated bot internals from `{branch}`.",
                color=discord.Color.green()
            )
            embed.add_field(name="git output", value=f"```\n{git_log}\n```", inline=False)
            embed.add_field(name="bot logs", value=log_chunk or "no cogs found.", inline=False)
            await status_msg.edit(embed=embed)

        except Exception as e:
            err = str(e)
            if len(err) > 1000:
                err = err[:1000] + "..."
            embed = discord.Embed(
                title="✖ pull failed",
                description=f"```\n{err}\n```",
                color=discord.Color.red()
            )
            embed.add_field(
                name="common causes",
                value="• invalid branch name\n• git not in venv path\n• network issue",
                inline=False
            )
            await status_msg.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(GitManager(bot))
