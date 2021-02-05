import discord
from discord.ext import commands
from bot.setting import TOKEN_ID, extensions

intents: discord.Intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='%', intents=intents)

for extension in extensions:
    try:
        client.load_extension(extension)
        print('Success')
    except Exception as e:
        print(e)

client.run(TOKEN_ID)
