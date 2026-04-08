import discord
import random
import asyncio
import time
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account, apply_loss, apply_earnings, debt_prompt

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_card(self):
        return random.randint(2, 11)

    @commands.hybrid_command(name="blackjack", aliases=["bj"], description="play blackjack against the house")
    async def blackjack(self, ctx, amount: int):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        data = await debt_prompt(ctx, self.bot, data, ctx.author.id)

        if amount > data[user_id]["wallet"] or amount <= 0:
            return await ctx.send("⊘ insufficient cores in wallet.")

        player_hand = [self.get_card(), self.get_card()]
        dealer_hand = [self.get_card(), self.get_card()]

        def create_embed(show_dealer=False):
            p_score = sum(player_hand)
            d_score = sum(dealer_hand) if show_dealer else f"{dealer_hand[0]} + ?"
            embed = discord.Embed(title="╼ blackjack ╾", color=0x2b2d31)
            embed.add_field(name="◈ your hand", value=f"cards: `{player_hand}`\ntotal: `{p_score}`")
            embed.add_field(name="◈ dealer hand", value=f"total: `{d_score}`")
            if not show_dealer:
                embed.set_footer(text="➕ hit  |  🛑 stand")
            return embed

        msg = await ctx.send(embed=create_embed())
        await msg.add_reaction("➕")
        await msg.add_reaction("🛑")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["➕", "🛑"] and reaction.message.id == msg.id

        while sum(player_hand) < 21:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                if str(reaction.emoji) == "➕":
                    player_hand.append(self.get_card())
                    await msg.edit(embed=create_embed())
                    try:
                        await msg.remove_reaction(reaction, user)
                    except: pass
                    if sum(player_hand) >= 21:
                        break
                elif str(reaction.emoji) == "🛑":
                    break
            except asyncio.TimeoutError:
                break

        p_total = sum(player_hand)
        if p_total <= 21:
            while sum(dealer_hand) < 17:
                dealer_hand.append(self.get_card())

        d_total = sum(dealer_hand)

        if p_total > 21:
            apply_loss(user_id, data, amount)
            debt = data[user_id]["debt"]
            result = f"⊘ bust. you lost **⌬ {amount}** cores."
            if debt > 0:
                result += f"\n⌬ {debt:,} now in debt."
        elif d_total > 21:
            debt_paid, to_wallet = apply_earnings(user_id, data, amount)
            result = f"◈ dealer bust. you won **⌬ {amount}** cores."
            if debt_paid:
                result += f"\n⌬ {debt_paid:,} went toward your debt."
        elif p_total > d_total:
            debt_paid, to_wallet = apply_earnings(user_id, data, amount)
            result = f"◈ winner. you won **⌬ {amount}** cores."
            if debt_paid:
                result += f"\n⌬ {debt_paid:,} went toward your debt."
        elif p_total < d_total:
            apply_loss(user_id, data, amount)
            debt = data[user_id]["debt"]
            result = f"⊘ dealer wins. you lost **⌬ {amount}** cores."
            if debt > 0:
                result += f"\n⌬ {debt:,} now in debt."
        else:
            result = "◈ push. your cores were returned."

        save_bank(data)
        final_embed = create_embed(show_dealer=True)
        final_embed.description = result
        await msg.edit(embed=final_embed)
        try:
            await msg.clear_reactions()
        except: pass

async def setup(bot):
    await bot.add_cog(Blackjack(bot))
