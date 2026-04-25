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
            "`!avatar [@user]` · show profile picture\n"
            "`!roleinfo <role>` · information about a role\n"
            "`!help` · show this menu"
        ), inline=False)

        embed.add_field(name="◈ utility", value=(
            "`!userinfo [@user]` · detailed member data\n"
            "`!serverinfo` · detailed guild stats\n"
            "`!calc <expr>` · evaluate math expressions\n"
            "`!poll <query>` · create a yes/no poll\n"
            "`!password [len]` · generate secure string\n"
            "`!dice [sides]` · roll a random die\n"
            "`!snipe` · last deleted message\n"
            "`!timer <sec> [label]` · countdown timer\n"
            "`!remind <dur> <msg>` · set a reminder\n"
            "`!afk [reason]` · set afk status\n"
            "`!translate <text>` · auto-detect & translate to english\n"
            "`!qr <text>` · generate a qr code\n"
            "`!dict <term>` · urban dictionary lookup\n"
            "`!weather <city>` · current weather\n"
            "`!b64 encode/decode <text>` · base64 encode or decode\n"
            "`!color <hex>` · color swatch & info\n"
            "`!mock <text>` · mOcK tExT\n"
            "`!reverse <text>` · reverse a string\n"
            "`!ascii <text>` · ascii art text"
        ), inline=False)

        embed.add_field(name="◈ moderation", value=(
            "`!purge <amt>` · clear messages ⌠perm⌡\n"
            "`!warn <@user> [reason]` · issue strike ⌠perm⌡\n"
            "`!warnings <@user>` · view strikes ⌠perm⌡\n"
            "`!rmwarn <@user> <idx>` · remove strike ⌠perm⌡\n"
            "`!kick <@user> [reason]` · eject member ⌠perm⌡\n"
            "`!ban <@user> [reason]` · blacklist user ⌠perm⌡\n"
            "`!unban <id> [reason]` · lift blacklist ⌠perm⌡\n"
            "`!blacklist <@user>` · block from commands ⌠perm⌡\n"
            "`!rmblacklist <@user>` · unblock user ⌠perm⌡\n"
            "`!timeout <@user> <dur> [reason]` · mute member ⌠perm⌡\n"
            "`!untimeout <@user>` · remove timeout ⌠perm⌡\n"
            "`!slowmode <sec>` · set channel slowmode ⌠perm⌡\n"
            "`!lock` · lock current channel ⌠perm⌡\n"
            "`!unlock` · unlock current channel ⌠perm⌡"
        ), inline=False)

        embed.add_field(name="◈ economy", value=(
            "`!bal [@user]` · check cores\n"
            "`!dep <amt>` · deposit to bank\n"
            "`!with <amt>` · withdraw from bank\n"
            "`!pay <@user> <amt>` · transfer cores\n"
            "`!work` · labor shift ⧖\n"
            "`!beg` · request cores ⧖\n"
            "`!daily` · 24h reward ⧖\n"
            "`!rob <@user>` · attempt theft ⧖\n"
            "`!crime` · commit a crime ⧖\n"
            "`!coinflip <h/t> <amt>` · flip a coin\n"
            "`!blackjack <amt>` · play blackjack\n"
            "`!plinko <amt>` · drop the ball\n"
            "`!redeem <code>` · redeem a code\n"
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
            "`!wyr` · would you rather\n"
            "`!confess <msg>` · anonymous message (dms only)"
        ), inline=False)

        embed.add_field(name="◈ maintenance ⌠auth⌡", value=(
            "`!eval <code>` · run code remotely\n"
            "`!pull [branch]` · github sync\n"
            "`!reload` · reload all cogs\n"
            "`!restart` · reboot bot process\n"
            "`!say <msg>` · send as bot\n"
            "`!admin @user` · add admin\n"
            "`!rmadmin @user` · remove admin\n"
            "`!adminlist` · list admins\n"
            "`!env [name] [value]` · manage env vars\n"
            "`!issuecode <code> <amt> [uses]` · create redeem code\n"
            "`!revokecode <code>` · delete redeem code\n"
            "`!brainwash` · wipe slug's chat history\n"
            "`!setwelcome <#ch>` · set welcome channel\n"
            "`!setconfessions <#ch>` · set confessions channel\n"
            "`!sethof <#ch>` · set hall of fame channel\n"
            "`!setaichat <#ch>` · set ai chat channel\n"
            "`!setdictionary <#ch>` · set dictionary channel"
        ), inline=False)

        embed.set_footer(text="⧖ = cooldown · ⌬ = cores · ⌠perm⌡ = requires permission · ⌠auth⌡ = authorized only")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))