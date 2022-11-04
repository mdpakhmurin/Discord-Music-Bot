from typing import List

from discord.ext import commands
import wavelink

from MusicBot.model.Queue.RedisQueStorage import RedisQueStorage
from MusicBot.model.Queue.IQue import IQue


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.que_storage = RedisQueStorage()

    @commands.Cog.listener()
    async def on_ready(self):
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='0.0.0.0',
            port=2333,
            password='secretpaassword')

        print("\n\n\nBot started!")

    @commands.command()
    async def play(self, ctx, *, music_query):
        server_id = self._get_server_id(ctx)

        voice_client = await self.force_connect_to_author_voice(ctx)
        if not voice_client:
            await ctx.reply("You are not in voice channel")
            return

        tracks = [await wavelink.YouTubeTrack.search(query=music_query, return_first=True)]
        que = self.que_storage.get_que(server_id)
        for track in tracks:
            que.push_back(track)

        if not voice_client.is_playing():
            await voice_client.play(que.pop_front())

        if len(tracks) == 0:
            await ctx.reply("I cant load your music")
        else:
            await ctx.reply(self.track_que_to_str())

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()

    @commands.command()
    async def list(self, ctx):
        server_id = self._get_server_id(ctx)

        que = self.que_storage.get_que(server_id)
        await ctx.reply(self.track_que_to_str(que))

    @commands.command()
    async def clear(self, ctx):
        server_id = self._get_server_id(ctx)

        self.que_storage.get_que(server_id).clear()
        await ctx.reply("Music list cleared")

        voice_client = self._get_voice_client(ctx)
        await voice_client.stop()

    @commands.command()
    async def skip(self, ctx):
        server_id = self._get_server_id(ctx)
        voice_client = self._get_voice_client(ctx)

        que = self.que_storage.get_que(server_id)
        track = que.pop_front()

        await ctx.reply(self.track_que_to_str(que))
        await voice_client.play(track)

    def _get_server_id(self, ctx):
        return ctx.message.guild.id

    def _get_author_voice(self, ctx):
        return ctx.message.author.voice

    def _get_voice_client(self, ctx):
        return ctx.voice_client

    def _get_author_voice_channel(self, ctx):
        return ctx.message.author.voice.channel

    def track_list_to_str(self, track_list: List[str]):
        s = ''
        for i, music in enumerate(track_list):
            s += f'{i+1}. {music.author}: {music.title}\n'
        return s

    def track_que_to_str(self, music_que: IQue):
        track_list = music_que.get_all()

        if len(track_list) == 0:
            return "Music queue is empty"
        else:
            return self.track_list_to_str(track_list)

    async def force_connect_to_author_voice(self, ctx):
        author_voice = self._get_author_voice(ctx)
        if not author_voice:
            return None

        voice_client = self._get_voice_client(ctx)
        voice_channel = self._get_author_voice_channel(ctx)
        if voice_client is None:
            voice_client = await voice_channel.connect(cls=wavelink.Player)
        await voice_client.move_to(voice_channel)

        return voice_client

    # def get_track_full_info(self, track):
        # return ""


async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
