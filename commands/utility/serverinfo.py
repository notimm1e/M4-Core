import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo", aliases=["si", "server"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        
        # Gathering server data
        name = guild.name
        member_count = guild.member_count
        owner = guild.owner
        id = guild.id
        # Formatting the creation date (Month Day, Year)
        created_at = guild.created_at.strftime("%B %d, %Y")
        
        # Creating the Embed
        embed = discord.Embed(
            title=f"Server Information",
            description=f"Details for **{name}**",
            color=discord.Color.blue()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=f"`{id}`", inline=True)
        embed.add_field(name="Member Count", value=member_count, inline=True)
        embed.add_field(name="Created On", value=created_at, inline=False)
        
        embed.set_footer(text=f"ID: {ctx.author.id}")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))