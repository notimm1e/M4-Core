import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", aliases=["h", "commands"], description="view the full system command list")
    async def help(self, ctx):
        embed = discord.Embed(
            title="╼ m4-core systems ╾",
            description="prefix: `!` · currency: `cores`",
            color=0x5865f2
        )

        embed.add_field(name="◈ general", value=(
            "`!ping` · check latency\n"
            "`!uptime` · runtime duration\n"
            "`!about` · bot information\n"
            "`!say <msg>` · broadcast ⌠auth⌡\n"
            "`!help` · show this menu"
        ), inline=False)

        embed.add_field(name="◈ utility", value=(
            "`!avatar [@user]` · show profile picture\n"
            "`!userinfo [@user]` · detailed member data\n"
            "`!serverinfo` · detailed guild stats\n"
            "`!roleinfo <role>` · information about a role\n"
            "`!calc <expr>` · evaluate math expressions\n"
            "`!poll <query>` · create a yes/no poll\n"
            "`!password [len]` · generate secure string\n"
            "`!dice [sides]` · roll a random die\n"
            "`!snipe` · last deleted message\n"
            "`!editsnipe` · last edited message\n"
            "`!timer <sec> [label]` · countdown timer\n"
            "`!afk [reason]` · set afk status"
        ), inline=False)

        embed.add_field(name="◈ moderation", value=(
            "`!purge <amt>` · clear logs ⌠perm⌡\n"
            "`!warn <@user>` · issue strike ⌠perm⌡\n"
            "`!warnings <@user>` · view strikes\n"
            "`!rmwarn <@user> <idx>` · remove strike ⌠perm⌡\n"
            "`!kick <@user>` · eject member ⌠perm⌡\n"
            "`!ban <@user>` · blacklist user ⌠perm⌡\n"
            "`!unban <id>` · lift blacklist ⌠perm⌡"
        ), inline=False)

        embed.add_field(name="◈ economy", value=(
            "`!bal` · check cores\n"
            "`!dep/!with` · bank management\n"
            "`!pay <@user> <amt>` · transfer cores\n"
            "`!work` · labor shift ⧖\n"
            "`!beg` · request cores ⧖\n"
            "`!daily` · 24h reward ⧖\n"
            "`!rob <@user>` · attempt theft ⧖\n"
            "`!crime` · commit a crime ⧖\n"
            "`!blackjack <amt>` · play blackjack\n"
            "`!plinko <amt>` · drop the ball\n"
            "`!lb` · richest users"
        ), inline=False)

        embed.add_field(name="◈ fun", value=(
            "`!ship @u1 @u2` · compatibility check\n"
            "`!8ball <query>` · ask the magic ball\n"
            "`!roast [@user]` · burn a member\n"
            "`!rps <play>` · rock paper scissors\n"
            "`!hack @user` · simulated breach\n"
            "`!deathdate [@user]` · predict demise\n"
            "`!impostor [@user]` · sus level check\n"
            "`!dumbass [@user]` · issue certificate\n"
            "`!confess <msg>` · anonymous message"
        ), inline=False)

        embed.add_field(name="◈ maintenance & events", value=(
            "`!setwelcome <#ch>` · entry config ⌠perm⌡\n"
            "`!pull [branch]` · github sync ⌠auth⌡\n"
            "`!reload [cog]` · reload module ⌠auth⌡\n"
            "`!restart` · reboot bot process ⌠auth⌡"
        ), inline=False)

        embed.set_footer(text="⧖ = cooldown · ⌬ = cores · ⌠perm⌡ = requires permission · ⌠auth⌡ = authorized only")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))
