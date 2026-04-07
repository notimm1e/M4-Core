import discord
from discord.ext import commands
from datetime import datetime

class snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        # Check if the message is a confession
        # We check for "!confess " to ensure it's the actual command
        is_confession = message.content.lower().startswith("!confess ")

        if is_confession:
            # Redact information for confessions
            self.sniped[message.channel.id] = {
                "content": message.content,
                "author_name": "[REDACTED]",
                "avatar": "https://i.imgur.com/839I7sH.png", # Transparent/Empty placeholder
                "at": datetime.utcnow(),
                "is_anonymous": True
            }
        else:
            # Store normal message data
            self.sniped[message.channel.id] = {
                "content": message.content,
                "author_name": message.author.display_name.lower(),
                "avatar": message.author.display_avatar.url,
                "at": datetime.utcnow(),
                "is_anonymous": False
            }

    @commands.hybrid_command(name="snipe", aliases=["s"], description="retrieve the last deleted message")
    async def snipe(self, ctx):
        data = self.sniped.get(ctx.channel.id)
        
        if not data:
            return await ctx.send(embed=discord.Embed(
                description="⊘ no data found in the buffer for this channel.",
                color=0xff4500
            ))

        embed = discord.Embed(
            description=data["content"] or "*[no data]*",
            color=0x2b2d31
        )
        
        # Set the author based on whether it was redacted or not
        embed.set_author(name=f"╼ {data['author_name']} ╾", icon_url=data["avatar"])
        
        timestamp = data['at'].strftime('%H:%M:%S')
        embed.set_footer(text=f"⌬ captured at {timestamp} UTC")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(snipe(bot))
