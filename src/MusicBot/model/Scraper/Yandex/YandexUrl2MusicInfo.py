from typing import List

from bs4 import BeautifulSoup
import aiohttp
import asyncio
import zope.interface

from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo

from MusicBot.model.Scraper.Yandex.AlbomUrl2MusicInfo import AlbomUrl2MusicInfo
from MusicBot.model.Scraper.Yandex.ArtistUrl2MusicInfo import ArtistUrl2MusicInfo 
from MusicBot.model.Scraper.Yandex.PlayListUrl2MusicInfo import PlayListUrl2MusicInfo 
from MusicBot.model.Scraper.Yandex.SingleTrackUrl2MusicInfo import SingleTrackUrl2MusicInfo


@zope.interface.implementer(IUrl2MusicInfo)
class YandexUrl2MusicInfo():
    def __init__(self):
        self.parsers = [
            AlbomUrl2MusicInfo(),
            ArtistUrl2MusicInfo(),
            PlayListUrl2MusicInfo(),
            SingleTrackUrl2MusicInfo()
        ]
        

    async def parse_asc(self, url: str) -> List[MusicInfo]:
        for parser in self.parsers:
            parse_result = await parser.parse_asc(url)
            if len(parse_result) > 0:
                return parse_result
        return []

    def parse(self, url: str) -> List[MusicInfo]:
        raise NotImplementedError()
