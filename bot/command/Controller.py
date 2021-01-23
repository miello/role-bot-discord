from discord.ext import commands

class Controller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def enableExt(self, ctx: commands.Context, ext: str):
        try:
            self.bot.load_extension(ext)
            await ctx.send('Enable extension successfully')
        except Exception as e:
            print(e)

    @commands.command(pass_context=True)
    async def disableExt(self, ctx: commands.context, ext: str):
        try:
            self.bot.unload_extension(ext)
            await ctx.send('Disable extension successfully')
        except Exception as e:
            print(e)
            

    @commands.command(pass_context=True)
    async def reloadExt(self, ctx: commands.context, ext: str):
        try:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
            await ctx.send('Reload extension successfully')
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Controller(bot))