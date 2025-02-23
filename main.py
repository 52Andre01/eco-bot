import discord
from discord.ext import commands
from model import get_class
import os, random
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''The duck command returns the photo of the duck'''
    print('hello')
    image_url = get_duck_image_url()
    await ctx.send(image_url)


@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = "img/temp." + attachment.filename.split('.')[-1]
            await attachment.save(f"./{file_name}")
            class_name, score = get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=f"./{file_name}")
            await ctx.send(f'Io penso che sia **{class_name[:-1]}** e sono sicuro al **{(score * 100) // 1}%**')
    else:
        await ctx.send("You forgot to upload the image :(")

with open ("token.txt", "r") as fin:
    token = fin.read()
bot.run(token)