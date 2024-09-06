import discord
from discord.ext import commands
from model import recycle
from yolo import detect_objects  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url

            try:
                await attachment.save(f"./images/{attachment.filename}")
                objects_detected = detect_objects(f"images/{attachment.filename}")
                if not objects_detected:
                    await ctx.send("Извините, я не уверен, что на этой картинке.")
                    return

                name = recycle(f"images/{attachment.filename}")
                await ctx.send(f"Я думаю, что это: {name}")
            except Exception as e:
                await ctx.send("Произошла ошибка при обработке изображения. Попробуйте снова.")
                print(f"Ошибка: {e}")
    else:
        await ctx.send("Вы забыли загрузить файлы :(")

bot.run("токен")