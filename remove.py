import discord
from discord.ext import commands

token = "PASTE_YOUR_DISCORD_TOKEN_HERE"

SERVERS = [1510207817217474661, 1510208070347653172, 1510208881769320518, 1510209273827950652]
SELECTED_INDEX = 0
NAME_PREFIX = "arrow_"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    target_id = SERVERS[SELECTED_INDEX]
    guild = bot.get_guild(target_id)
    if not guild:
        print(f"Guild {target_id} not found or bot is not in it.")
        await bot.close()
        return

    print(f"Removing {NAME_PREFIX}* emojis from {guild.name} ({target_id})...")

    removed = 0
    for emoji in list(guild.emojis):
        if not emoji.name.startswith(NAME_PREFIX):
            continue
        try:
            await emoji.delete()
            removed += 1
        except Exception as e:
            print(f"Failed to delete {emoji.name}: {e}")

    print(f"Removed {removed} emojis from {guild.name}")
    await bot.close()


if __name__ == '__main__':
    if token:
        bot.run(token)
    else:
        print("Error: Please set the token at the top of remove.py.")
