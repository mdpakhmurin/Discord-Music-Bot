from typing import List

import zope.interface
import youtube_dl

from model.IMusic import IMusic
from model.Music import Music
from model.MusicBase.IMusicBase import IMusicBase


@zope.interface.implementer(IMusicBase)
class YTMusicBase():
    def __init__(self):
        pass

    def searchable(self, text: str):
        return True

    def search(self, text: str) -> List[IMusic]:
        ydl_opts = {'format': 'bestaudio'}

        musics = []
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch:{text}", download=False)['entries']
            if len(search_result) > 0:
                first_music = search_result[0]

                author = first_music['channel']
                title = first_music['title']
                url = first_music['formats'][0]['url']
                musics.append(Music(author, title, url))

        return musics