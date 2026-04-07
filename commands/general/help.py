import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h", "commands"])
    async def help(self, ctx):
        embed = discord.Embed(
            title="m4-core · commands",
            description="prefix: `!`",
            color=discord.Color.blue()
        )

        embed.add_field(name="── general ──", value=(
            "`!ping` · check bot latency\n"
            "`!uptime` · how long the bot has been running\n"
            "`!say <message>` · make the bot say something ⌠auth⌡\n"
            "`!help` · show this menu"
        ), inline=False)

        embed.add_field(name="── utility ──", value=(
            "`!avatar [@member]` · show a user's avatar\n"
            "`!userinfo [@member]` · detailed user info\n"
            "`!serverinfo` · detailed server info\n"
            "`!roleinfo <role>` · info about a role\n"
            "`!calculator <expr>` · evaluate a math expression\n"
            "`!poll <question>` · create a yes/no poll\n"
            "`!password [length]` · generate a secure password\n"
            "`!dice [sides]` · roll a die"
        ), inline=False)

        embed.add_field(name="── moderation ──", value=(
            "`!purge <amount>` · delete messages ⌠manage messages⌡\n"
            "`!warn <@member> [reason]` · warn a user ⌠moderate members⌡\n"
            "`!warnings <@member>` · view warnings ⌠moderate members⌡\n"
            "`!rmwarn <@member> <index>` · remove a warning ⌠moderate members⌡\n"
            "`!kick <@member> [reason]` · kick a user ⌠kick members⌡\n"
            "`!ban <@member> [reason]` · ban a user ⌠ban members⌡\n"
            "`!unban <user_id> [reason]` · unban a user ⌠ban members⌡"
        ), inline=False)

        embed.add_field(name="── fun ──", value=(
            "`!ship @user1 @user2` · compatibility check\n"
            "`!8ball <question>` · ask the magic 8ball\n"
            "`!roast [@member]` · roast someone\n"
            "`!rps <rock/paper/scissors>` · play against the bot\n"
            "`!hack @member` · totally real hacking\n"
            "`!deathdate [@member]` · predict someone's demise"
        ), inline=False)

        embed.add_field(name="── events ──", value=(
            "`!setwelcome <#channel>` · set welcome channel ⌠manage guild⌡"
        ), inline=False)

        embed.add_field(name="── maintenance ──", value=(
            "`!pull [branch]` · pull from github & reload cogs ⌠auth⌡\n"
            "`!restart` · restart the bot process ⌠auth⌡"
        ), inline=False)

        embed.set_footer(text="⌠perm⌡ = requires permission · ⌠auth⌡ = authorized users only")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))
