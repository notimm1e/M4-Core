import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True  
intents.members = True # Required for the welcome feature

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        for root, dirs, files in os.walk("./commands"):
            for filename in files:
                if filename.endswith(".py"):
                    relative_path = os.path.relpath(os.path.join(root, filename), ".")
                    module_path = relative_path.replace(os.sep, ".").removesuffix(".py")
                    
                    try:
                        await self.load_extension(module_path)
                        print(f"✅ Loaded: {module_path}")
                    except Exception as e:
                        print(f"❌ Failed to load {module_path}: {e}")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'M4-Core is now active.')
        print('------')

    # 2. Global Error Handler
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ That command does not exist (yet).")
        elif isinstance(error, commands.MissingPermissions):
            # This catches permission errors globally so you don't have to code them in every file
            await ctx.send("❌ You don't have the required permissions to use this.")
        else:
            # Logs other errors to your terminal so you can fix them
            print(f"Logged Error: {error}")

bot = MyBot()
bot.run(TOKEN)