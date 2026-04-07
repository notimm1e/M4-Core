import discord
import random
import asyncio
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def deal_card(self):
        return random.randint(2, 11)

    @commands.command(name="blackjack", aliases=["bj"])
    async def blackjack(self, ctx, amount: int):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        if amount > data[user_id]["wallet"] or amount <= 0:
            return await ctx.send("⊘ insufficient cores.")

        player_hand = [self.deal_card(), self.deal_card()]
        dealer_hand = [self.deal_card(), self.deal_card()]

        async def get_embed():
            p_total = sum(player_hand)
            d_visible = dealer_hand[0]
            embed = discord.Embed(title="╼ blackjack ╾", color=0x2b2d31)
            embed.add_field(name="◈ your hand", value=f"cards: {player_hand}\ntotal: `{p_total}`")
            embed.add_field(name="◈ dealer", value=f"showing: `{d_visible}`")
            embed.set_footer(text="➕ hit  |  🛑 stand")
            return embed

        msg = await ctx.send(embed=await get_embed())
        await msg.add_reaction("➕")
        await msg.add_reaction("🛑")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["➕", "🛑"] and reaction.message.id == msg.id

        while sum(player_hand) < 21:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                if str(reaction.emoji) == "➕":
                    player_hand.append(self.deal_card())
                    await msg.edit(embed=await get_embed())
                    await msg.remove_reaction(reaction, user)
                else:
                    break
            except asyncio.TimeoutError:
                break

        p_total = sum(player_hand)
        while sum(dealer_hand) < 17:
            dealer_hand.append(self.deal_card())
        d_total = sum(dealer_hand)

        result_embed = discord.Embed(title="╼ blackjack results ╾", color=0x2b2d31)
        result_embed.add_field(name="◈ you", value=f"`{p_total}`")
        result_embed.add_field(name="◈ dealer", value=f"`{d_total}`")

        if p_total > 21:
            msg_text = "⊘ bust. you lost."
            data[user_id]["wallet"] -= amount
        elif d_total > 21 or p_total > d_total:
            msg_text = f"◈ winner. earned **⌬ {amount}**."
            data[user_id]["wallet"] += amount
        elif p_total == d_total:
            msg_text = "◈ push. cores returned."
        else:
            msg_text = "⊘ dealer wins."
            data[user_id]["wallet"] -= amount

        result_embed.description = msg_text
        save_bank(data)
        await msg.edit(embed=result_embed)
        await msg.clear_reactions()

async def setup(bot):
    await bot.add_cog(Blackjack(bot))
