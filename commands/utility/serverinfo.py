import discord
from discord.ext import commands

class serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo", aliases=["si", "server"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        created_at = guild.created_at.strftime("%b %d, %Y")

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        roles = len(guild.roles) - 1

        bots = sum(1 for m in guild.members if m.bot)
        humans = guild.member_count - bots

        boost_level = guild.premium_tier
        boosts = guild.premium_subscription_count

        embed = discord.Embed(
            title="✦", guild.name,
            description=guild.description or "no description set.",
            color=discord.Color.blue()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.add_field(name="owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="id", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="created", value=created_at, inline=True)

        embed.add_field(name="members", value=f"total `{guild.member_count}` · humans `{humans}` · bots `{bots}`", inline=False)
        embed.add_field(name="channels", value=f"text `{text_channels}` · voice `{voice_channels}` · categories `{categories}`", inline=False)
        embed.add_field(name="roles", value=f"`{roles}`", inline=True)
        embed.add_field(name="boosts", value=f"level `{boost_level}` · `{boosts}` boosts", inline=True)

        embed.set_footer(text=f"requested by {ctx.author.name}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(serverinfo(bot))