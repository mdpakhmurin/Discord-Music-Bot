from typing import List

from bs4 import BeautifulSoup
import aiohttp
import re
import zope.interface

from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


@zope.interface.implementer(IUrl2MusicInfo)
class ArtistUrl2MusicInfo():
    def __init__(self):
        pass

    async def parse_asc(self, url: str) -> List[MusicInfo]:
        result = []
        if self._check_url_pattern(url):
            try:
                result = await self._try_parse_asc(url)
            except:
                pass
        return result

    def _check_url_pattern(self, url: str) -> bool:
        url_pattern = re.compile('https:\/\/music.yandex.ru\/artist\/\d*(\/tracks\/?|\/)?$')
        return bool(url_pattern.match(url))

    async def _try_parse_asc(self, url: str) -> List[MusicInfo]:
        if not url.endswith('/tracks'):
            url += '/tracks'

        tracks = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')

                tracks_author = soup.find(
                    'h1', class_='page-artist__title').text
                tracks_author = tracks_author.strip()

                tracks_titles_html = soup.find_all(
                    'a', class_='d-track__title')
                for track_title_html in tracks_titles_html:
                    track_title = track_title_html.text
                    track_title = track_title.strip()

                    tracks.append(MusicInfo(track_title, [tracks_author]))

        return tracks

    def parse(self, url: str) -> List[MusicInfo]:
        raise NotImplementedError()
