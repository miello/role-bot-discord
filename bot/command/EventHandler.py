import discord
from discord.ext import commands
from bot.setting import server_emoji

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        user_now = self.bot.get_user(payload.user_id)

        if user_now == self.bot.user:
            return

        member = payload.member
        emoji = str(payload.emoji)

        if emoji not in server_emoji.keys():
            print('Not Found Emoji')
            return
        else:
            print('Found')
            await member.add_roles(server_emoji[emoji][0])


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        user_now: discord.User = self.bot.get_user(payload.user_id)

        if user_now == self.bot.user:
            return

        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        member: discord.Member = guild.get_member(payload.user_id)
        emoji = str(payload.emoji)

        if emoji not in server_emoji.keys():
            print('Not Found')
            return
        elif member:
            print('Remove role')
            await member.remove_roles(server_emoji[emoji][0])
        else:
            print('Not found user in guild')


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        print(f'Message {message.content} from {message.author}')


    @commands.command(pass_context=True)
    async def about(ctx: commands.Context):
        await ctx.send('Role Adding System By Using Emoji Reaction [RASBUER]\n**(Currently in WIP)**')


def setup(bot):
    bot.add_cog(EventHandler(bot))