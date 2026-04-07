import discord
from discord.ext import commands
from datetime import datetime

class snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped = {}
        self.edit_sniped = {}

    def get_redacted_data(self, message):
        """Helper to create redacted or normal data dictionary."""
        is_confession = message.content.lower().startswith("!confess ")
        
        if is_confession:
            return {
                "content": message.content,
                "author_name": "[REDACTED]",
                "avatar": "https://i.imgur.com/839I7sH.png", # Empty/Transparent placeholder
                "at": datetime.utcnow()
            }
        else:
            return {
                "content": message.content,
                "author_name": message.author.display_name.lower(),
                "avatar": message.author.display_avatar.url,
                "at": datetime.utcnow()
            }

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        self.sniped[message.channel.id] = self.get_redacted_data(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        self.edit_sniped[before.channel.id] = self.get_redacted_data(before)

    @commands.hybrid_command(name="snipe", aliases=["s"], description="retrieve the last deleted message")
    async def snipe(self, ctx):
        data = self.sniped.get(ctx.channel.id)
        if not data:
            return await ctx.send(embed=discord.Embed(description="⊘ no deleted data found.", color=0xff4500))

        embed = discord.Embed(description=data["content"] or "*[no text]*", color=0x2b2d31)
        embed.set_author(name=f"╼ {data['author_name']} ╾", icon_url=data["avatar"])
        embed.set_footer(text=f"⌬ deleted at {data['at'].strftime('%H:%M:%S')} UTC")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="editsnipe", aliases=["es"], description="retrieve the last edited message")
    async def editsnipe(self, ctx):
        data = self.edit_sniped.get(ctx.channel.id)
        if not data:
            return await ctx.send(embed=discord.Embed(description="⊘ no edited data found.", color=0xff4500))

        embed = discord.Embed(description=data["content"] or "*[no text]*", color=0x2b2d31)
        embed.set_author(name=f"╼ {data['author_name']} ╾", icon_url=data["avatar"])
        embed.set_footer(text=f"⌬ edited at {data['at'].strftime('%H:%M:%S')} UTC")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(snipe(bot))
