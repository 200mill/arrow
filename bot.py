import os
import io
import discord
from discord.ext import commands
from PIL import Image

token = "PASTE_YOUR_DISCORD_TOKEN_HERE"

# Set up intents (required to read message content in modern discord.py)
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    servers = [1510207817217474661, 1510208070347653172, 1510208881769320518, 1510209273827950652]
    for i in range(4):
        current = servers[i]
        guild = bot.get_guild(current)
        if not guild:
            print(f"Guild {current} not found or bot is not in it.")
            continue

        print(f"Uploading to {guild.name} ({current})...")
        
        # 각 서버당 90개씩 할당 (0~89, 90~179, ...)
        start_idx = i * 90
        
        # 50 -> static emoji upload
        for j in range(50):
            idx = start_idx + j
            path = f'./img/{idx}.png'
            if not os.path.exists(path): continue
            
            with open(path, 'rb') as f:
                img_bytes = f.read()
            
            try:
                await guild.create_custom_emoji(name=f"arrow_{idx}", image=img_bytes)
            except Exception as e:
                print(f"Failed to upload static arrow_{idx}: {e}")

        # 40 -> gif emoji upload
        for j in range(50, 90):
            idx = start_idx + j
            path = f'./img/{idx}.png'
            if not os.path.exists(path): continue
            
            try:
                # 디스코드가 애니메이션 슬롯으로 인식하려면 다중 프레임 GIF여야 하므로 같은 프레임 2장으로 저장
                with Image.open(path) as img:
                    b = io.BytesIO()
                    img.save(
                        b,
                        format="GIF",
                        save_all=True,
                        append_images=[img.copy()],
                        duration=100,
                        loop=0,
                        disposal=2,
                    )

                await guild.create_custom_emoji(name=f"arrow_{idx}", image=b.getvalue())
            except Exception as e:
                print(f"Failed to upload gif arrow_{idx}: {e}")
                
    print("Emoji upload complete!")



if __name__ == '__main__':
    if token:
        bot.run(token)
    else:
        print("Error: Please set the token at the top of bot.py.")
