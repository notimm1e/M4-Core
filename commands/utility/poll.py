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

    @poll.error
    async def poll_error(self, ctx, error):
        error.handled = True
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title="✖ missing question",
                description="provide a question. (e.g. `!poll should we have a movie night?`)",
                color=discord.Color.red()
            ))

async def setup(bot):
    await bot.add_cog(poll(bot))