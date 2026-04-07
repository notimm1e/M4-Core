import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", aliases=["h", "commands"], description="show the command menu")
    async def help(self, ctx):
        embed = discord.Embed(
            title="╼ m4-core systems ╾",
            description="prefix: `!` · currency: `cores`",
            color=0x2b2d31
        )

        embed.add_field(name="◈ general", value=(
            "`!about` · system information\n"
            "`!ping` · check latency\n"
            "`!uptime` · session duration\n"
            "`!help` · show this menu"
        ), inline=False)

        embed.add_field(name="◈ economy", value=(
            "`!bal` · check cores\n"
            "`!work` · earn cores ⧖\n"
            "`!beg` · request cores ⧖\n"
            "`!daily` · claim daily reward ⧖\n"
            "`!dep <amt>` · deposit to bank\n"
            "`!with <amt>` · withdraw to wallet\n"
            "`!pay <@user> <amt>` · transfer cores"
        ), inline=False)

        embed.add_field(name="◈ fun & utility", value=(
            "`!impostor [@user]` · check sus levels\n"
            "`!avatar [@user]` · view profile image\n"
            "`!calculator <expr>` · solve math\n"
            "`!8ball <query>` · consult the void"
        ), inline=False)

        embed.add_field(name="◈ moderation", value=(
            "`!purge <amt>` · delete logs\n"
            "`!warn <@user>` · issue strike\n"
            "`!kick/!ban` · remove entities"
        ), inline=False)

        embed.set_footer(text="⧖ = has cooldown · ⌬ = currency unit")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
