
import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

maps = [
    "CTF-Cynosure][LE105",
    "CTF-Vaultcity-LE102",
    "CTF-Sub-ZeroLE104",
    "CTF-Vengeance-CE103",
    "CTF-Ranel-JoltEdition",
    "CTF-Gataka-SE105",
    "CTF-DeonizeLE111",
    "CTF-Ahunuii-LE101",
    "CTF-Infested-UGL-LE203",
    "CTF-Cronomize-PE100",
    "CTF-NovemberCE127"
]

active_sessions = {}

@bot.command()
async def startmapban(ctx):
    if ctx.channel.id in active_sessions:
        await ctx.send("Map ban is already in progress in this channel.")
        return

    await ctx.send("Please mention two players who will be banning maps (e.g. @Player1 @Player2):")

    def check_players(m):
        return m.channel == ctx.channel and len(m.mentions) == 2

    try:
        msg = await bot.wait_for("message", timeout=60.0, check=check_players)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting for player mentions.")
        return

    player1, player2 = msg.mentions
    players = [player1, player2]
    random.shuffle(players)

    await ctx.send(f"Randomly selected: {players[0].mention} will start the map banning.")

    session = {
        "players": players,
        "current_turn": 0,
        "remaining_maps": sorted(maps)
    }

    active_sessions[ctx.channel.id] = session
    await next_ban_round(ctx)

async def next_ban_round(ctx):
    session = active_sessions[ctx.channel.id]
    remaining = session["remaining_maps"]

    if len(remaining) == 1:
        await ctx.send(f"Final map to play is: **{remaining[0]}**")
        del active_sessions[ctx.channel.id]
        return

    current_player = session["players"][session["current_turn"] % 2]
    await ctx.send(f"{current_player.mention}, please type the name of the map to remove from the list:
```\n" + "\n".join(remaining) + "\n``` (You have 30 seconds)")

    def check(m):
        return m.author == current_player and m.channel == ctx.channel

    try:
        reminder_task = asyncio.create_task(reminder(ctx, current_player))
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        reminder_task.cancel()
        selected_map = msg.content.strip()

        if selected_map in remaining:
            remaining.remove(selected_map)
            session["current_turn"] += 1
            await next_ban_round(ctx)
        else:
            await ctx.send("Invalid map name. Automatically removing the first map.")
            removed = remaining.pop(0)
            await ctx.send(f"Removed: {removed}")
            session["current_turn"] += 1
            await next_ban_round(ctx)

    except asyncio.TimeoutError:
        removed = remaining.pop(0)
        await ctx.send(f"{current_player.mention} took too long. Removed first map: {removed}")
        session["current_turn"] += 1
        await next_ban_round(ctx)

async def reminder(ctx, player):
    await asyncio.sleep(20)
    await ctx.send(f"{player.mention}, 10 seconds left to pick a map!")

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
