from typing import List

import discord
from discord.ext import commands
import wavelink
import datetime

from MusicBot.model.Queue.RedisQueStorage import RedisQueStorage
from MusicBot.model.Queue.IQue import IQue
from StringProgressBar import progressBar

from MusicBot.model.Scraper.Yandex.YandexUrl2MusicInfo import YandexUrl2MusicInfo


class ServerMusicStorage():
    def __init__(self) -> None:
        self.que_storage = RedisQueStorage()
        self.yandex_parser = YandexUrl2MusicInfo()

    async def search_add_tracks(self, server_id: str, search_query: str, max_number: int = 5) -> List[wavelink.Track]:
        que = self.que_storage.get_que(server_id)
        searched_tracks = await self.search_track(search_query, max_number=max_number)
        for track in searched_tracks:
            que.push_back(track)
        return searched_tracks

    async def search_track(self, query: str, max_number: int = 5) -> List[wavelink.Track]:
        tracks = []

        track_titles = []
        if 'music.yandex.ru' in query:
            tracks_info = await self.yandex_parser.parse_asc(query)
            track_titles = [f'{track_info.title} - {track_info.authors}' for track_info in tracks_info]
        else:
            track_titles = [query]

        track_titles = track_titles[:max_number]
        for track_title in track_titles:
            try:
                yt_search_result = await wavelink.YouTubeTrack.search(query=track_title, return_first=True)
                tracks.append(yt_search_result)
            except Exception as e:
                print(e)

        return tracks

    def pop_que(self, server_id: str) -> wavelink.Track:
        que = self.que_storage.get_que(server_id)
        return que.pop_front()

    def get_all_que(self, server_id: str) -> List[wavelink.Track]:
        que = self.que_storage.get_que(server_id)
        return que.get_all()

    def clear_que(self, server_id: str) -> None:
        que = self.que_storage.get_que(server_id)
        que.clear()


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage = ServerMusicStorage()

    @commands.command()
    async def play(self, ctx, *track_query):
        server_id = ctx.message.guild.id

        max_tracks = 5
        if len(track_query) > 1 and track_query[-1].isdigit():
            max_tracks = int(track_query[-1])
            track_query = ' '.join(track_query[:-1])
        else:
            track_query = ' '.join(track_query)

        await self.storage.search_add_tracks(server_id, track_query, max_number=max_tracks)

        voice_client = await self.voice_client_join_to_author(ctx)
        if not voice_client:
            await ctx.reply("I can't connect the player")
        elif voice_client.is_paused():
            await voice_client.play()
        elif not voice_client.is_playing():
            next_music = self.storage.pop_que(server_id)
            await voice_client.play(next_music)
        
        await ctx.reply(embed=self.gen_player_status_embed(voice_client))
        await ctx.send(embed=self.gen_track_list_embed(self.storage.get_all_que(server_id)))

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track:  wavelink.Track, reason):
        if reason == "FINISHED":
            server_id = player.guild.id
            next_track = self.storage.pop_que(server_id)
            await player.play(next_track)

    @commands.command()
    async def pause(self, ctx):
        voice_client = await self.voice_client_join_to_author(ctx)
        await voice_client.pause()

    @commands.command()
    async def list(self, ctx):
        player = ctx.voice_client
        server_id = ctx.message.guild.id

        await ctx.reply(embed=self.gen_player_status_embed(player))
        await ctx.send(embed=self.gen_track_list_embed(self.storage.get_all_que(server_id)))

    @commands.command()
    async def clear(self, ctx):
        server_id = ctx.message.guild.id
        voice_client = await self.voice_client_join_to_author(ctx)

        self.storage.clear_que(server_id)
        await ctx.reply("Music list cleared")

        if voice_client:
            await voice_client.stop()

    @commands.command()
    async def skip(self, ctx):
        server_id = ctx.message.guild.id
        voice_client = await self.voice_client_join_to_author(ctx)
        if voice_client:
            await voice_client.stop()

            next_track = self.storage.pop_que(server_id)
            await voice_client.play(next_track)

            await ctx.reply(embed=self.gen_player_status_embed(voice_client))
            await ctx.send(embed=self.gen_track_list_embed(self.storage.get_all_que(server_id)))

    async def stop_voice(self, ctx):
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.stop()

    async def play_next(self, ctx):
        voice_client = ctx.voice_client
        if voice_client:
            next_track = self.storage.pop_que(ctx.message.guild.id)
            await voice_client.play(next_track)

    async def voice_client_join_to_author(self, ctx) -> wavelink.Player:
        voice_client = None

        author_voice = ctx.message.author.voice
        if author_voice:
            author_voice_channel = author_voice.channel

            voice_client = ctx.voice_client
            if voice_client is None:
                voice_client = await author_voice_channel.connect(cls=wavelink.Player)

            await voice_client.move_to(author_voice_channel)

        return voice_client

    def gen_player_status_embed(self, player: wavelink.Player) -> discord.Embed:
        if not player or not (player.is_paused() or player.is_playing()):
            embed = discord.Embed(title="List is not playing", color=0xdd0000)
        else:
            track = player.track

            passed_time = datetime.timedelta(seconds=int(player.position))
            all_time = datetime.timedelta(seconds=int(track.duration))

            pb = progressBar.splitBar(
                total=int(all_time.total_seconds()),
                current=int(passed_time.total_seconds()),
                size=15)
            pb_str = pb[0]

            embed = discord.Embed(
                title=track.title, color=0x00dd00, description=pb_str)
            embed.set_author(name=track.author)
            embed.set_footer(text=f'{str(passed_time)} / {str(all_time)}')

        return embed

    def gen_track_list_embed(self, track_list: List[wavelink.Track]) -> discord.Embed:
        if not track_list:
            embed = discord.Embed(title="Music list is empty", color=0xdd0000)
        else:
            track_list_str = ''
            for track_id, track in enumerate(track_list, start=1):
                track_id_formatted = str(track_id)[:2].rjust(2)
                author_formatted = track.author[:10].ljust(10)
                title_formatted = track.title[:30].ljust(30)
                duration = str(datetime.timedelta(seconds=int(track.duration)))

                track_list_str += f'{track_id_formatted}. {author_formatted}: {title_formatted} | {duration}\n'
                if track_id > 20:
                    track_list_str += '...'
                    break
            track_list_str = f'```{track_list_str}```'

            embed_title = f'Music list ({len(track_list)} tracks)'
            embed = discord.Embed(
                title=embed_title, color=0x3299cd, description=track_list_str)

        return embed


async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
