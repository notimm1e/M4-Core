import os
import discord
from discord.ext import commands
from helpers.admins_config import load_admins, save_admins

class Emergency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.passphrase = os.getenv("EMERGENCY_PASSPHRASE")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not isinstance(message.channel, discord.DMChannel):
            return

        if not self.passphrase:
            return

        if message.content.strip() == self.passphrase:
            admins = load_admins()

            if message.author.id in admins:
                return await message.channel.send(embed=discord.Embed(
                    description="⊘ you already have admin powers",
                    color=0xff4500
                ))

            admins.add(message.author.id)
            save_admins(admins)

            await message.channel.send(embed=discord.Embed(
                description="√ emergency admin access granted",
                color=0x57f287
            ))

async def setup(bot):
    await bot.add_cog(Emergency(bot))