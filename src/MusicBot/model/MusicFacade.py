from typing import List
from MusicBot.model.IMusic import IMusic
from MusicBot.model.IMusic import IMusic

from MusicBot.model.Music import Music
from MusicBot.model.Queue.IQue import IQue
from MusicBot.model.Queue.IQueStorage import IQueStorage
from MusicBot.model.Queue.RedisQueStorage import RedisQueStorage

from MusicBot.model.MusicSearcher.IMusicSearcher import IMusicSearcher
from MusicBot.model.MusicSearcher.YTMusicSearcher import YTMusicSearcher

DEFAULT_MUSIC_SEARCHER = YTMusicSearcher()
DEFAULT_QUE_STORAGE = RedisQueStorage()


class MusicFacade:
    def __init__(self, music_searcher: IMusicSearcher = DEFAULT_MUSIC_SEARCHER, que_storage: IQueStorage = DEFAULT_QUE_STORAGE) -> None:
        self._searcher: IMusicSearcher = None
        self._que_storage: IQueStorage = None

        self.set_music_searcher(music_searcher)
        self.set_que_storage(que_storage)

    def set_que_storage(self, storage: IQueStorage) -> None:
        self._que_storage = storage

    def set_music_searcher(self, searcher: IMusicSearcher) -> None:
        self._searcher = searcher

    def add_to_que(self, server_id: str, music: str) -> None:
        que = self._que_storage.get_que(server_id)
        music_list = self.search_music(music)
        for music in music_list:
            que.push_back(music)

    def peek_que_first(self, server_id: str) -> IMusic:
        que = self._que_storage.get_que(server_id)
        return que.peek_front()

    def pop_que_first(self, server_id: str) -> IMusic:
        que = self._que_storage.get_que(server_id)
        return que.pop_front()

    def get_que_size(self, server_id: str) -> int:
        que = self._que_storage.get_que(server_id)
        return que.get_size()

    def clear_que(self, server_id: str) -> None:
        que = self._que_storage.get_que(server_id)
        que.clear()

    def search_music(self, music: str) -> List[IMusic]:
        return self._searcher.search(music)