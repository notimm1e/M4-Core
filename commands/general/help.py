import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", aliases=["h", "commands"], description="show the system command menu")
    async def help(self, ctx):
        embed = discord.Embed(
            title="╼ m4-core systems ╾",
            description="prefix: `!` · currency: `cores`",
            color=0x2b2d31
        )

        embed.add_field(name="◈ general", value=(
            "`!about` · system info\n"
            "`!ping` · latency\n"
            "`!uptime` · runtime\n"
            "`!say <msg>` · repeat text ⌠auth⌡"
        ), inline=True)

        embed.add_field(name="◈ economy", value=(
            "`!bal` · check cores\n"
            "`!work` · earn cores ⧖\n"
            "`!beg` · request cores ⧖\n"
            "`!daily` · daily reward ⧖\n"
            "`!dep/!with` · bank mgmt\n"
            "`!pay <@user> <amt>` · transfer"
        ), inline=True)

        embed.add_field(name="◈ utility", value=(
            "`!avatar [@user]` · view pfp\n"
            "`!userinfo` · member data\n"
            "`!serverinfo` · guild data\n"
            "`!calc <expr>` · math engine\n"
            "`!poll` · create vote\n"
            "`!password` · gen string\n"
            "`!dice` · roll random"
        ), inline=False)

        embed.add_field(name="◈ moderation", value=(
            "`!purge <amt>` · clear logs\n"
            "`!warn/!rmwarn` · strikes\n"
            "`!warnings` · view strikes\n"
            "`!kick/!ban/!unban` · removal"
        ), inline=True)

        embed.add_field(name="◈ fun", value=(
            "`!impostor [@user]` · sus levels\n"
            "`!ship` · compatibility\n"
            "`!8ball` · void wisdom\n"
            "`!roast` · burn user\n"
            "`!rps` · play bot\n"
            "`!hack` · simulated breach\n"
            "`!deathdate` · predict end"
        ), inline=True)

        embed.add_field(name="◈ system", value=(
            "`!setwelcome` · config entry\n"
            "`!pull` · github sync ⌠auth⌡\n"
            "`!restart` · reboot bot ⌠auth⌡"
        ), inline=False)

        embed.set_footer(text="⧖ = cooldown · ⌬ = cores · ⌠auth⌡ = authorized only")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
