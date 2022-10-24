from typing import List

import zope.interface
import youtube_dl

from IMusic import IMusic
from IMusicBase import IMusicBase
from Music import Music


@zope.interface.implementer(IMusicBase)
class YTMusicBase():
    def __init__(self):
        pass

    def searchable(self, text: str):
        return True

    def search(self, text: str) -> List[IMusic]:
        ydl_opts = {'format': 'bestaudio'}

        music = Music("", "", "")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch:{text}", download=False)
            first_music = search_result['entries'][0]
            url = first_music['formats'][0]['url']

            music = Music(first_music['channel'], first_music['title'], url)

        return [music]