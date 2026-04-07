import discord
import asyncio
from discord.ext import commands

class timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="timer", aliases=["t", "countdown"])
    async def timer(self, ctx, duration: int, *, label: str = "timer"):
        if duration < 1:
            return await ctx.send(embed=discord.Embed(title="✖ invalid duration", description="duration must be at least `1` second.", color=discord.Color.red()))
        if duration > 86400:
            return await ctx.send(embed=discord.Embed(title="✖ too long", description="maximum duration is `86400` seconds (24h).", color=discord.Color.red()))

        def fmt(s):
            h, r = divmod(s, 3600)
            m, s = divmod(r, 60)
            parts = []
            if h: parts.append(f"`{h}h`")
            if m: parts.append(f"`{m}m`")
            parts.append(f"`{s}s`")
            return " ".join(parts)

        embed = discord.Embed(
            title=f"⟳ {label}",
            description=f"time remaining: {fmt(duration)}",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"started by {ctx.author.display_name}")
        msg = await ctx.send(embed=embed)

        elapsed = 0
        update_interval = 5 if duration > 30 else 1

        while elapsed < duration:
            await asyncio.sleep(update_interval)
            elapsed += update_interval
            remaining = max(0, duration - elapsed)

            embed.description = f"time remaining: {fmt(remaining)}"
            await msg.edit(embed=embed)

        done_embed = discord.Embed(
            title=f"√ {label}",
            description=f"{ctx.author.mention} your timer is up!",
            color=discord.Color.green()
        )
        done_embed.set_footer(text=f"started by {ctx.author.display_name}")
        await msg.edit(embed=done_embed)

        await ctx.send(f"{ctx.author.mention} ⏱ **{label}** is done!")

        try:
            await ctx.author.send(embed=discord.Embed(
                title=f"⏱ timer done · {label}",
                description=f"your timer in **{ctx.guild.name}** · #{ctx.channel.name} has ended.",
                color=discord.Color.green()
            ))
        except discord.Forbidden:
            pass

    @timer.error
    async def timer_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="✖ missing duration", description="usage: `!timer <seconds> [label]`", color=discord.Color.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="✖ invalid duration", description="duration must be a number in seconds.", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(timer(bot))
