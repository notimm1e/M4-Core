import discord
import random
import asyncio
import json
from discord.ext import commands
from groq import Groq
from helpers.economy_base import load_bank, save_bank, open_account, apply_loss, apply_earnings, debt_prompt

# --- AI Integration Helpers ---
def get_ai_commentary(bet_amount, multiplier, profit):
    try:
        with open("groq.json", "r") as f:
            config = json.load(f)
        client = Groq(api_key=config["api_key"])
        
        # Construct the context for the AI
        status = "win" if profit > 0 else "loss"
        user_input = f"user {status} {abs(profit)} credits. bet was {bet_amount} with {multiplier}x multiplier."

        system_prompt = (
            "you are m4 core commenting on results. lowercase only. minimal emojis. "
            "if they win: be a hype man, high energy slang. "
            "if they lose small: tell them to touch grass or aw shucks. "
            "if they lose 1000+: tell them to take a break, it's a bad habit, and link ncpgambling.org. "
            "be creative, don't repeat yourself."
        )

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8,
        )
        return completion.choices[0].message.content.lower()
    except Exception as e:
        print(f"AI Error: {e}")
        return None

# --- Existing Plinko Logic Constants ---
ROWS = 6
SLOTS = ["▼", "◈", "❖", "▲", "✦"]
TOTAL_COLS = len(SLOTS) * 2 - 1

RISK_MODES = {
    "low": {"multipliers": [0.5, 0.8, 1.0, 1.2, 1.5], "weights": [10, 25, 30, 25, 10]},
    "medium": {"multipliers": [0.2, 0.5, 1.2, 1.5, 3.0], "weights": [25, 35, 20, 15, 5]},
    "high": {"multipliers": [0.0, 0.2, 1.5, 3.0, 5.0], "weights": [35, 30, 20, 10, 5]}
}

RISK_EMOJIS = {"🟢": "low", "🟡": "medium", "🔴": "high"}

def build_board(path_taken, current_col, row):
    lines = []
    for r in range(ROWS):
        pegs = []
        for c in range(TOTAL_COLS):
            if r < row:
                if c == path_taken[r]:
                    if r > 0:
                        prev = path_taken[r - 1]
                        pegs.append("╲" if prev < c else "╱" if prev > c else "│")
                    else:
                        pegs.append("│")
                else:
                    pegs.append("·")
            elif r == row:
                pegs.append("⬤" if c == current_col else "·")
            else:
                pegs.append("·")
        lines.append("  ".join(pegs))
    
    width = TOTAL_COLS * 3 - 2
    lines.append("═" * width)
    gap = (width - len(SLOTS)) // (len(SLOTS) - 1)
    slot_line = (" " * gap).join(SLOTS)
    lines.append(slot_line)
    return "\n".join(lines)

class Plinko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="plinko")
    async def plinko(self, ctx, amount: int):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        data = await debt_prompt(ctx, self.bot, data, ctx.author.id)

        if amount <= 0:
            return await ctx.send("amount must be greater than zero.")

        if amount > data[user_id]["wallet"]:
            return await ctx.send(embed=discord.Embed(description="⊘ insufficient cores.", color=0xff4500))

        embed = discord.Embed(
            title="╼ plinko ╾",
            description=f"select risk mode\n\nbet: {amount}\nwallet: {data[user_id]['wallet']} cores",
            color=0x2b2d31
        )

        message = await ctx.send(embed=embed)
        for emoji in RISK_EMOJIS:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in RISK_EMOJIS

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await message.edit(embed=discord.Embed(description="⌛ timed out selecting risk.", color=0xed4245))

        risk = RISK_EMOJIS[str(reaction.emoji)]
        mode = RISK_MODES[risk]
        multiplier = random.choices(mode["multipliers"], weights=mode["weights"])[0]
        slot_index = mode["multipliers"].index(multiplier)
        final_board_col = int(slot_index * (TOTAL_COLS - 1) / (len(SLOTS) - 1))

        await message.clear_reactions()

        current_col = TOTAL_COLS // 2
        path = []
        for r in range(ROWS):
            path.append(current_col)
            if r < ROWS - 1:
                if current_col < final_board_col:
                    current_col += random.choices([1, 0], weights=[75, 25])[0]
                elif current_col > final_board_col:
                    current_col -= random.choices([1, 0], weights=[75, 25])[0]
                else:
                    current_col += random.choices([-1, 0, 1], weights=[20, 60, 20])[0]
                current_col = max(0, min(TOTAL_COLS - 1, current_col))

        for r in range(ROWS):
            board = build_board(path, path[r], r)
            embed.description = f"```\n{board}\n```"
            await message.edit(embed=embed)
            await asyncio.sleep(0.4)

        winnings = int(amount * multiplier)
        profit = winnings - amount
        apply_loss(user_id, data, amount)
        debt_paid, to_wallet = apply_earnings(user_id, data, winnings) if winnings > 0 else (0, 0)
        save_bank(data)

        # --- Generate AI Commentary ---
        ai_msg = get_ai_commentary(amount, multiplier, profit)

        result_text = (
            f"bet: {amount}\n"
            f"multiplier: {multiplier}x\n"
            f"winnings: {winnings}\n"
            f"{'profit' if profit >= 0 else 'loss'}: {abs(profit)}"
        )
        
        if debt_paid: result_text += f"\n⌬ {debt_paid:,} went toward your debt."
        
        # Update Embed
        embed.color = 0x57f287 if multiplier > 1 else 0xfee75c if multiplier == 1 else 0xed4245
        embed.description = f"```\n{build_board(path, path[-1], ROWS - 1)}\n```\n{result_text}"
        
        # Add AI commentary as a field if successful
        if ai_msg:
            embed.add_field(name="m4 core", value=ai_msg, inline=False)
            
        await message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Plinko(bot))
