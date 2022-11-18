import asyncio

import discord
from discord.ext import commands
from MusicBot.bot import config

import wavelink

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    for node in config.lavalink_nodes:
        await wavelink.NodePool.create_node(
            bot=bot,
            host=node['host'],
            port=node['port'],
            password=node['password']
        )

    print("\n"*3)
    print("Bot started!")


async def run(token: str):
    bot.remove_command('help') 
    await bot.load_extension("MusicBot.bot.cogs.MusicCommands")
    await bot.start(token)

@bot.event
async def on_command_error(ctx, err):
    print(err)

asyncio.run(run(config.bot_token))