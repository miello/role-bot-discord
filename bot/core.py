import discord
from discord.ext import commands
from bot.setting import TOKEN_ID

intents: discord.Intents = discord.Intents.default()
intents.members = True

extensions = ['bot.command.EventHandler', 'bot.command.Controller', 'bot.command.RoleCommand']

client = commands.Bot(command_prefix='%', intents=intents)

for extension in extensions:
    try:
        client.load_extension(extension)
        print('Success')
    except Exception as e:
        print(e)

client.run(TOKEN_ID)
