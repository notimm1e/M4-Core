import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        excluded_modules = {
            "commands.economy.economy_base",
            "commands.admins_config",
            "commands.blacklist_config"
        }
        
        for root, dirs, files in os.walk("./commands"):
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    relative_path = os.path.relpath(os.path.join(root, filename), ".")
                    module_path = relative_path.replace(os.sep, ".").removesuffix(".py")
                    
                    if module_path in excluded_modules:
                        print(f"⊘ skipped: {module_path}")
                        continue
                    
                    try:
                        await self.load_extension(module_path)
                        print(f"√ loaded: {module_path}")
                    except Exception as e:
                        print(f"✖ failed to load {module_path}: {e}")

    async def on_ready(self):
        print(f'logged in as {self.user} (id: {self.user.id})')
        print(f'm4-core is now active.')
        print('------')

    async def on_command_error(self, ctx, error):
        if hasattr(error, 'handled'):
            return
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=discord.Embed(
                title="✖ unknown command",
                description="that command does not exist (yet).",
                color=discord.Color.red()
            ))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title="✖ missing permissions",
                description="you don't have the required permissions to use this.",
                color=discord.Color.red()
            ))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title="✖ missing argument",
                description=f"`{error.param.name}` is required but was not provided.",
                color=discord.Color.red()
            ))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(
                title="✖ bad argument",
                description="one or more arguments are invalid.",
                color=discord.Color.red()
            ))
        else:
            print(f"unhandled error in {ctx.command}: {error}")

bot = MyBot()
bot.run(TOKEN)
