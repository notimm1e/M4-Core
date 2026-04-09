import discord
import random
import asyncio
from discord.ext import commands

ALWAYS_SUS = {"nyxgoober"}

VERDICTS_SUS = [
    "extremely suspicious. do not trust.",
    "something is very off here.",
    "the scan doesn't lie. very sus.",
    "anomalous readings detected.",
    "trust level: zero.",
]

VERDICTS_CLEAR = [
    "probably fine. probably.",
    "no anomalies detected.",
    "seems legit. for now.",
    "cleared. but stay alert.",
    "scan complete. nothing unusual.",
]

SCAN_STEPS = [
    "⟳ initializing biometric scan...",
    "⟳ cross-referencing identity matrix...",
    "⟳ analyzing behavioral patterns...",
    "⟳ checking timeline inconsistencies...",
    "⟳ running anomaly detection...",
    "⟳ finalizing report...",
]

class impostor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="impostor", aliases=["sus", "scan"])
    async def impostor(self, ctx, member: discord.Member = None):
        target = member or ctx.author

        embed = discord.Embed(
            title="⌖ scanning",
            description=SCAN_STEPS[0],
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        msg = await ctx.send(embed=embed)

        for step in SCAN_STEPS[1:]:
            await asyncio.sleep(1.1)
            embed.description = step
            await msg.edit(embed=embed)

        await asyncio.sleep(1)

        is_sus = target.name.lower() in ALWAYS_SUS or random.random() < 0.4
        sus_score = random.randint(85, 99) if is_sus else random.randint(3, 35)
        verdict = random.choice(VERDICTS_SUS if is_sus else VERDICTS_CLEAR)
        bar_filled = sus_score // 10
        bar = "█" * bar_filled + "░" * (10 - bar_filled)

        result_embed = discord.Embed(
            title=f"{'⚠ impostor detected' if is_sus else '√ scan complete'}",
            color=discord.Color.red() if is_sus else discord.Color.green()
        )
        result_embed.set_thumbnail(url=target.display_avatar.url)
        result_embed.add_field(name="subject", value=target.mention, inline=True)
        result_embed.add_field(name="sus level", value=f"`{bar}` {sus_score}%", inline=False)
        result_embed.add_field(name="verdict", value=verdict, inline=False)
        result_embed.set_footer(text="scan powered by m4-core anomaly engine")
        await msg.edit(embed=result_embed)

    @impostor.error
    async def impostor_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="✖ member not found", description="that member doesn't exist.", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(impostor(bot))
