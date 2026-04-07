import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll", aliases=["vote", "question"])
    async def poll(self, ctx, *, question: str):
        """Creates a simple Yes/No poll."""
        
        # Creating a clean embed for the poll
        embed = discord.Embed(
            title="📊 Survey / Poll",
            description=question,
            color=discord.Color.blurple()
        )
        
        embed.set_footer(text=f"Poll started by {ctx.author.name}")
        
        # Send the poll message
        poll_msg = await ctx.send(embed=embed)
        
        # Add the reactions
        await poll_msg.add_reaction("✅")
        await poll_msg.add_reaction("❌")
        
        # Delete the original command message to keep the channel clean
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Please provide a question for the poll. (Example: `!poll Should we have a movie night?`)")

async def setup(bot):
    await bot.add_cog(Poll(bot))