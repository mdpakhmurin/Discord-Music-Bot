import asyncio
from distutils.command.config import config
import discord
from discord.ext import commands

import wavelink

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


async def run(token: str):
    await bot.load_extension("MusicBot.bot.cogs.MusicCommands")
    await bot.start(token)
    