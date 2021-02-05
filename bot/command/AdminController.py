from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions

class Controller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_guild_permissions(manage_channels=True)
    @commands.group(pass_context=True)
    @commands.guild_only()
    async def admin(self, ctx: commands.Context):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if hasattr(ctx.command, 'on_err'):
            return 
        
        await ctx.send('Admin command have gotten error')

    @admin.command(pass_context=True, no_pm=True)
    async def enableExt(self, ctx: commands.Context, type: str, ext: str):
        try:
            self.bot.load_extension(f'bot.{type}.{ext}')
            await ctx.send('Enable extension successfully')
        except Exception as e:
            print(e)
            await ctx.send(str(e))

    @admin.command(pass_context=True, no_pm=True)
    async def disableExt(self, ctx: commands.context, type: str, ext: str):
        try:
            self.bot.unload_extension(f'bot.{type}.{ext}')
            await ctx.send('Disable extension successfully')
        except Exception as e:
            print(e)
            await ctx.send(str(e))            

    @admin.command(pass_context=True, no_pm=True)
    async def reloadExt(self, ctx: commands.context, type: str, ext: str):
        try:
            self.bot.unload_extension(f'bot.{type}.{ext}')
            self.bot.load_extension(f'bot.{type}.{ext}')
            await ctx.send('Reload extension successfully')
        except Exception as e:
            print(e)
            await ctx.send(str(e))

def setup(bot):
    bot.add_cog(Controller(bot))