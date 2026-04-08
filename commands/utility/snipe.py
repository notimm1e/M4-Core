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
        self.sniped[message.channel.id] = {
            "content": message.content,
            "author": message.author,
            "avatar": message.author.display_avatar.url,
            "at": datetime.utcnow()
        }

    @commands.command(name="snipe", aliases=["s"])
    async def snipe(self, ctx):
        data = self.sniped.get(ctx.channel.id)
        if not data:
            return await ctx.send(embed=discord.Embed(
                title="✖ nothing to snipe",
                description="no recently deleted messages in this channel.",
                color=discord.Color.red()
            ))

        embed = discord.Embed(
            title="⌖ sniped",
            description=data["content"] or "*[no text content]*",
            color=discord.Color.blue()
        )
        embed.set_author(name=data["author"].display_name, icon_url=data["avatar"])
        embed.set_footer(text=f"deleted at {data['at'].strftime('%b %d, %Y %H:%M')} UTC")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(snipe(bot))
