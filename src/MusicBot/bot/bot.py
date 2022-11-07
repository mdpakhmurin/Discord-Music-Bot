import asyncio
from distutils.command.config import config
import discord
from discord.ext import commands

import wavelink

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


# @commands.Cog.listener()
@bot.event
async def on_ready():
    await wavelink.NodePool.create_node(
        bot=bot,
        host='0.0.0.0',
        port=2333,
        password='secretpaassword')

    print("\n*3")
    print("Bot started!")


async def run(token: str):
    await bot.load_extension("MusicBot.bot.cogs.MusicCommands")
    await bot.start(token)
