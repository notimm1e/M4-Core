import discord
from discord.ext import commands
from datetime import datetime

class snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped = {}
        self.editsniped = {}
        self.redacted_image = "https://assetcdn.patchednexus.win/money.png"

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        # Check for "!confess " to ensure it's the actual command
        is_confession = message.content.lower().startswith("!confess ")

        if is_confession:
            self.sniped[message.channel.id] = {
                "content": message.content,
                "author_name": "[REDACTED]",
                "avatar": self.redacted_image,
                "at": datetime.utcnow()
            }
        else:
            self.sniped[message.channel.id] = {
                "content": message.content,
                "author_name": message.author.display_name.lower(),
                "avatar": message.author.display_avatar.url,
                "at": datetime.utcnow()
            }

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        is_confession = before.content.lower().startswith("!confess ")

        if is_confession:
            self.editsniped[before.channel.id] = {
                "old_content": before.content,
                "new_content": after.content,
                "author_name": "[REDACTED]",
                "avatar": self.redacted_image,
                "at": datetime.utcnow()
            }
        else:
            self.editsniped[before.channel.id] = {
                "old_content": before.content,
                "new_content": after.content,
                "author_name": before.author.display_name.lower(),
                "avatar": before.author.display_avatar.url,
                "at": datetime.utcnow()
            }

    @commands.hybrid_command(name="snipe", aliases=["s"], description="retrieve the last deleted message")
    async def snipe(self, ctx):
        data = self.sniped.get(ctx.channel.id)
        if not data:
            return await ctx.send(embed=discord.Embed(
                description="⊘ no deleted data found for this channel.",
                color=0xff4500
            ))

        embed = discord.Embed(description=data["content"] or "*[no data]*", color=0x2b2d31)
        embed.set_author(name=f"╼ {data['author_name']} ╾", icon_url=data["avatar"])
        embed.set_footer(text=f"⌬ captured at {data['at'].strftime('%H:%M:%S')} UTC")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="editsnipe", aliases=["es"], description="retrieve the last edited message")
    async def editsnipe(self, ctx):
        data = self.editsniped.get(ctx.channel.id)
        if not data:
            return await ctx.send(embed=discord.Embed(
                description="⊘ no edit data found for this channel.",
                color=0xff4500
            ))

        embed = discord.Embed(color=0x2b2d31)
        embed.set_author(name=f"╼ {data['author_name']} ╾", icon_url=data["avatar"])
        embed.add_field(name="◈ before", value=data["old_content"] or "*[empty]*", inline=False)
        embed.add_field(name="◈ after", value=data["new_content"] or "*[empty]*", inline=False)
        embed.set_footer(text=f"⌬ edited at {data['at'].strftime('%H:%M:%S')} UTC")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(snipe(bot))
