from MusicBot.bot.bot import run
import config

import asyncio

asyncio.run(run(config.bot_token))
