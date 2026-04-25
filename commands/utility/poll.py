import discord
from discord.ext import commands

class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll", aliases=["vote", "question"])
    async def poll(self, ctx, *, question: str):
        embed = discord.Embed(
            title="⌯⌲ poll",
            description=question,
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"started by {ctx.author.name}")

        poll_msg = await ctx.send(embed=embed)
        await poll_msg.add_reaction("☑️")
        await poll_msg.add_reaction("❌")

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

async def setup(bot):
    await bot.add_cog(poll(bot))