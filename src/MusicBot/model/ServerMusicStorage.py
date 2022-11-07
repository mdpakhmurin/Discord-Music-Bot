from typing import List
import wavelink

from MusicBot.model.Queue.RedisQueStorage import RedisQueStorage
from MusicBot.model.Scraper.Yandex.YandexUrl2MusicInfo import YandexUrl2MusicInfo 


class ServerMusicStorage():
    def __init__(self) -> None:
        self.que_storage = RedisQueStorage()
        self.parsers = [YandexUrl2MusicInfo()]

    async def search_add_tracks(self, server_id: str, search_query: str, max_number: int = 5) -> List[wavelink.Track]:
        que = self.que_storage.get_que(server_id)

        searched_tracks = await self.search_track(search_query, max_number=max_number)
        for track in searched_tracks:
            que.push_back(track)

        return searched_tracks

    async def search_track(self, query: str, max_number: int = 5) -> List[wavelink.Track]:
        track_titles = await self._query_to_track_titles(query)
        track_titles = track_titles[:max_number]

        tracks = await self._search_tracks_by_titles(track_titles)

        return tracks

    async def _search_tracks_by_titles(self, track_titles: List[str]) -> List[wavelink.Track]:
        tracks = []
        for track_title in track_titles:
            try:
                yt_search_result = await wavelink.YouTubeTrack.search(query=track_title, return_first=True)
                tracks.append(yt_search_result)
            except Exception as e:
                print(e)

        return tracks

    async def _query_to_track_titles(self, query: str) -> List[str]:
        track_titles = []
        if 'http' in query:
            tracks_info = await self._parse_query(query)
            track_titles = [f'{track_info.title} - {track_info.authors}' for track_info in tracks_info]
        else:
            track_titles = [query]
            
        return track_titles

    async def _parse_query(self, query: str) -> List[str]:
        for parser in self.parsers:
            tracks_info = await parser.parse_asc(query)
            if tracks_info:
                return tracks_info
        return []

    def pop_que(self, server_id: str) -> wavelink.Track:
        que = self.que_storage.get_que(server_id)
        return que.pop_front()

    def get_all_que(self, server_id: str) -> List[wavelink.Track]:
        que = self.que_storage.get_que(server_id)
        return que.get_all()

    def clear_que(self, server_id: str) -> None:
        que = self.que_storage.get_que(server_id)
        que.clear()