if __name__ == '__main__':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
import MusicBot.bot.config as config
import discord
from discord.ext import commands

import wavelink

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

lavalink_nodes = []

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

@bot.event
async def on_command_error(ctx, err):
    print(err)

async def run():
    bot.remove_command('help') 
    await bot.load_extension("MusicBot.bot.cogs.MusicCommands")

    await bot.start(config.bot_token)

asyncio.run(run())