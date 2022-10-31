from discord.ext import commands
from MusicBot.model.MusicFacade import MusicFacade

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.musicFacade = MusicFacade()

    @commands.command()
    async def play(self, ctx, *, music_id):
        print(ctx)

    @commands.command()
    async def pause(self, ctx):
        print(ctx)

    @commands.command()
    async def resume(self, ctx):
        print(ctx)

    @commands.command()
    async def list(self, ctx):
        print(ctx)

    @commands.command()
    async def skip(self, ctx):
        print(ctx)

async def setup(bot):
    await bot.add_cog(MusicCommands(bot))