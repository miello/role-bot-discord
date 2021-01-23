import discord
from discord.ext import commands
from bot.setting import server_emoji, server_msg

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def add(self, ctx: commands.Context, emoji: str, role: str, *, reason: str):
        print(emoji, role)
        try:
            if emoji in server_emoji.keys():
                await ctx.send('**Error: This emoji has been used**')
            else:
                is_valid = False
                role_added = None
                guild_id = ctx.guild.id
                for guild_role in ctx.guild.roles:
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


    @commands.command(pass_context=True)
    async def remove(self, ctx: commands.Context, emoji_del: str):
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


    @commands.command(pass_context=True)
    async def display(self, ctx: commands.Context, channel: str):
        dest_channel = None
        guild = ctx.guild
        dest_channel = discord.utils.get(self.bot.get_all_channels(), guild=guild, name=channel)

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


def setup(bot):
    bot.add_cog(Role(bot))