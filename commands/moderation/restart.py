@commands.command(name="restart")
async def restart(self, ctx):
    if ctx.author.id not in AUTHORIZED:
        return

    await ctx.send(embed=discord.Embed(
        title="⟳ restarting",
        description="restarting bot process...",
        color=discord.Color.blue()
    ))

    await self.bot.close()
    os.execv(sys.executable, [sys.executable, "main.py"])
