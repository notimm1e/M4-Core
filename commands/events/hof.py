import discord
from discord.ext import commands

HOF_CHANNEL = 1491359053274939503

class HallOfFame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hof", description="add a replied message to the hall of fame")
    @commands.has_permissions(manage_messages=True)
    async def hof(self, ctx):
        if not ctx.message.reference:
            return await ctx.send(embed=discord.Embed(
                description="✖ you must reply to a message to hof it.",
                color=0xff4500
            ), delete_after=5)

        try:
            ref_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except discord.NotFound:
            return await ctx.send(embed=discord.Embed(
                description="✖ could not find the referenced message.",
                color=0xff4500
            ), delete_after=5)

        hof_channel = ctx.guild.get_channel(HOF_CHANNEL)
        if not hof_channel:
            return await ctx.send(embed=discord.Embed(
                description="✖ hall of fame channel not found.",
                color=0xff4500
            ))

        author = ref_msg.author
        embed = discord.Embed(
            description=ref_msg.content or None,
            color=0xf1c40f,
            timestamp=ref_msg.created_at
        )
        embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
        embed.add_field(name="source", value=f"[jump to message]({ref_msg.jump_url})", inline=True)
        embed.add_field(name="channel", value=ref_msg.channel.mention, inline=True)
        embed.set_footer(text=f"inducted by {ctx.author.display_name}")

        files = []
        if ref_msg.attachments:
            first = ref_msg.attachments[0]
            if first.content_type and first.content_type.startswith("image"):
                embed.set_image(url=first.url)
            else:
                embed.add_field(
                    name="attachment",
                    value=f"[{first.filename}]({first.url})",
                    inline=False
                )

        await hof_channel.send(embed=embed)
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(
            description=f"√ added to {hof_channel.mention}.",
            color=0x57f287
        ), delete_after=5)

async def setup(bot):
    await bot.add_cog(HallOfFame(bot))