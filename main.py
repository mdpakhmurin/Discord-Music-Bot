# import discord
# from discord import FFmpegPCMAudio
# from discord.ext import commands

# from YTMusicBase import YTMusicBase
# music_base = YTMusicBase()

# intents = discord.Intents().all()
# client = discord.Client(intents=intents)
# bot = commands.Bot(command_prefix='!',intents=intents)


# FFMPEG_OPTIONS = {}
# @bot.command()
# async def play(ctx, title):
#     channel = ctx.message.author.voice.channel
#     vc = await channel.connect()
#     music_link = music_base.search(title)[0].link()
#     source = FFmpegPCMAudio(music_link, **FFMPEG_OPTIONS)
#     vc.play(source)

# DISCORD_TOKEN = "NO IT IS VERY SECRET INFO"
# bot.run(DISCORD_TOKEN)
