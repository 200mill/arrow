import os
import io
import discord
from discord.ext import commands
from PIL import Image

token = os.environ.get("DISCORD_TOKEN", "")

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
                # 디스코드가 애니메이션 슬롯으로 인식하려면 '진짜' 다중 프레임 GIF여야 한다.
                # 프레임 2장이 완전히 동일하면 PIL이 하나로 합쳐 단일 프레임 GIF가 되고,
                # 그러면 디스코드가 정적(static) 이모지로 취급해 50칸 한도에 걸린다.
                # 그래서 두 번째 프레임의 픽셀 1개 alpha를 살짝 바꿔 두 프레임을 강제로 구분한다.
                with Image.open(path) as img:
                    f1 = img.convert("RGBA")
                    f2 = f1.copy()
                    px = f2.load()
                    r, g, bl, a = px[0, 0]
                    px[0, 0] = (r, g, bl, a - 1 if a > 0 else 1)

                    b = io.BytesIO()
                    f1.save(
                        b,
                        format="GIF",
                        save_all=True,
                        append_images=[f2],
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
