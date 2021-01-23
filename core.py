import discord
from discord.ext import commands

intents: discord.Intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='%', intents=intents)

server_emoji = dict()
server_msg = dict()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    user_now = client.get_user(payload.user_id)

    if user_now == client.user:
        return

    member = payload.member
    emoji = str(payload.emoji)

    if emoji not in server_emoji.keys():
        print('Not Found Emoji')
        return
    else:
        print('Found')
        await member.add_roles(server_emoji[emoji][0])


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    user_now: discord.User = client.get_user(payload.user_id)

    if user_now == client.user:
        return

    guild: discord.Guild = client.get_guild(payload.guild_id)
    member: discord.Member = guild.get_member(payload.user_id)
    emoji = str(payload.emoji)

    if emoji not in server_emoji.keys():
        return
    elif member:
        await member.remove_roles(server_emoji[emoji][0])
    else:
        print('Not found user in guild')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    print(f'Message {message.content} from {message.author}')
    await client.process_commands(message)

@client.command(pass_context=True)
async def add(ctx: commands.Context, emoji: str, role: str, *, reason: str):
    print(emoji, role)
    try:
        if emoji in server_emoji.keys():
            await ctx.send('**Error: This emoji has been used**')
        else:
            is_valid = False
            role_added = None
            guild_id = ctx.guild.id
            for guild_role in ctx.guild.roles:
                print(guild_role.name, role)
                if guild_role.name == role:
                    role_added = guild_role
                    is_valid = True
                    break

            if is_valid:
                server_emoji[emoji] = (role_added, reason)
                print(emoji, role_added, reason)
                print('find ' + str(guild_id))

                if guild_id in server_msg.keys():   
                    msg = server_msg[guild_id]
                    embed = discord.Embed(color=0xbc3838)
                        
                    print('Add Process')

                    for emoji, role in server_emoji.items():
                        embed.add_field(name=f'กด \\{emoji} เพื่อ{role[1]}', value='** **', inline=False)
                        
                    await msg.edit(embed=embed)
                    await msg.add_reaction(emoji)

                await ctx.send('**Add emoji role successfully**')
            else:
                await ctx.send('**Error: Not found this role in this server**')
    except Exception as e:
        await ctx.send('**Unknown error occurred**')


@client.command(pass_context=True)
async def remove(ctx: commands.Context, emoji_del: str):
    try:
        # First check that emoji present in database or not
        if emoji_del not in server_emoji.keys():
            await ctx.send('**Error: Not found this role in database**')
        else:
            # then delete that emoji
            guild_id = ctx.guild.id
            del server_emoji[emoji_del]

            # edit message if we already display message
            if guild_id in server_msg.keys():
                msg = server_msg[guild_id]
                embed = discord.Embed(color=0xbc3838)
                    
                print('Remove Process', emoji_del)

                for emoji, role in server_emoji.items():
                    embed.add_field(name=f'กด \\{emoji} เพื่อ{role[1]}', value='** **', inline=False)
                    
                await msg.edit(embed=embed)
                await msg.clear_reaction(emoji_del)
            await ctx.send('**Deleted Role Successfully**')
    except Exception as e:
        print(e)
        await ctx.send('**Unknown error occurred**')


@client.command(pass_context=True)
async def display(ctx: commands.Context, channel: str):
    dest_channel = None
    guild = ctx.guild
    dest_channel = discord.utils.get(client.get_all_channels(), guild=guild, name=channel)

    print(channel, dest_channel)

    if dest_channel == None or guild.id in server_msg:
        return

    embed = discord.Embed(color=0xbc3838)
    for emoji, role in server_emoji.items():
        embed.add_field(name=f'กด \\{emoji} เพื่อ{role[1]}', value='** **', inline=False)

    msg = await dest_channel.send(embed=embed)

    for emoji in server_emoji.keys():
        await msg.add_reaction(emoji)

    server_msg[guild.id] = msg
    print('has ' + str(guild.id))