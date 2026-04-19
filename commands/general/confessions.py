import discord
from discord.ext import commands

CONFESSION_CHANNEL_ID = 1491085704829341747

class Confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="confess", description="send an anonymous confession")
    async def confess(self, ctx, *, message: str):
        if ctx.guild is not None:
            return await ctx.send(embed=discord.Embed(
                description="⊘ use this command in dms.",
                color=0x2b2d31
            ))

        channel = self.bot.get_channel(CONFESSION_CHANNEL_ID)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(CONFESSION_CHANNEL_ID)
            except:
                return await ctx.send(embed=discord.Embed(
                    description="⊘ confession channel not found.",
                    color=0x2b2d31
                ))

        embed = discord.Embed(
            title="╼ anonymous confession ╾",
            description=message.lower(),
            color=0x2b2d31
        )
        embed.set_footer(text="use !confess in dms to share")

        await channel.send(embed=embed)

        try:
            await ctx.author.send(embed=discord.Embed(
                description="◈ confession sent successfully.",
                color=0x2b2d31
            ), delete_after=5)
        except:
            pass

async def setup(bot):
    await bot.add_cog(Confessions(bot))