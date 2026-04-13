import discord
from discord.ext import commands
from commands.admins_config import is_admin

class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load")
    async def load_module(self, ctx, module: str):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(description="⊘ unauthorized.", color=0xff4500))

        try:
            await self.bot.load_extension(module)
            await ctx.send(embed=discord.Embed(
                description=f"√ loaded: `{module}`",
                color=0x57f287
            ))
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(embed=discord.Embed(description=f"⊘ `{module}` is already loaded.", color=0xff4500))
        except commands.ExtensionNotFound:
            await ctx.send(embed=discord.Embed(description=f"⊘ `{module}` not found.", color=0xff4500))
        except Exception as e:
            await ctx.send(embed=discord.Embed(
                title=f"✖ failed to load `{module}`",
                description=f"```{e}```",
                color=0xff4500
            ))

async def setup(bot):
    await bot.add_cog(Load(bot))