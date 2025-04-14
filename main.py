import discord
from discord.ext import commands, tasks
import asyncio
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

MAP_POOL = [
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

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.command()
async def startmapban(ctx):
    await ctx.send("🎮 Map elimination is starting!")

    # Get two users mentioned
    def check_author(m):
        return m.author != bot.user and m.channel == ctx.channel

    await ctx.send("Please mention **two players** who will be banning maps (e.g. @Player1 @Player2):")
    try:
        msg = await bot.wait_for('message', check=check_author, timeout=60.0)
        mentions = msg.mentions
        if len(mentions) != 2:
            await ctx.send("❌ You must mention exactly two players.")
            return
        player_a, player_b = mentions
    except asyncio.TimeoutError:
        await ctx.send("⏰ Time's up. Try starting again.")
        return

    players = [player_a, player_b]
    random.shuffle(players)
    current_index = 0
    current_player = players[current_index]

    await ctx.send(f"🔀 Random draw complete! {current_player.mention} will start the elimination.")

    remaining_maps = sorted(MAP_POOL)

    while len(remaining_maps) > 1:
        await ctx.send(f"""{current_player.mention}, please eliminate a map.

Remaining maps:
```
{chr(10).join(remaining_maps)}
```
⏳ You have 30 seconds.""")

        try:
            def elimination_check(m):
                return m.author == current_player and m.channel == ctx.channel and m.content.strip() in remaining_maps

            reminder = asyncio.create_task(reminder_message(ctx, current_player))
            msg = await bot.wait_for('message', check=elimination_check, timeout=30.0)
            reminder.cancel()
            eliminated = msg.content.strip()
            remaining_maps.remove(eliminated)
            await ctx.send(f"❌ {eliminated} eliminated by {current_player.mention}.")
        except asyncio.TimeoutError:
            reminder.cancel()
            eliminated = remaining_maps[0]
            remaining_maps.remove(eliminated)
            await ctx.send(f"⏰ Time's up! Automatically eliminating **{eliminated}**.")

        current_index = (current_index + 1) % 2
        current_player = players[current_index]

    await ctx.send(f"✅ Final map selected: **{remaining_maps[0]}**")

def setup(bot):
    bot.add_command(startmapban)

async def reminder_message(ctx, player):
    await asyncio.sleep(20)
    await ctx.send(f"⏳ {player.mention}, 10 seconds left to eliminate a map!")

# Replace this with your bot token
bot.run("YOUR_DISCORD_BOT_TOKEN")
