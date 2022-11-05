from typing import List

from bs4 import BeautifulSoup
import aiohttp
import re
import zope.interface

from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


@zope.interface.implementer(IUrl2MusicInfo)
class PlayListUrl2MusicInfo():
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

    async def _try_parse_asc(self, url: str) -> List[MusicInfo]:
        tracks = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')

                tracks_wrappers_html = soup.find_all('div', class_='d-track__overflowable-wrapper')
                for track_wrapper_html in tracks_wrappers_html:
                    track_title_html = track_wrapper_html.find('div', class_='d-track__name')
                    track_title = track_title_html.text.strip()

                    track_authors_html = track_wrapper_html.find('span', class_='d-track__artists')
                    track_authors_html = track_authors_html.find_all('a')
                    track_authors = [track.text.strip() for track in track_authors_html]

                    tracks.append(MusicInfo(track_title, track_authors))
        
        return tracks

    def _check_url_pattern(self, url: str) -> bool:
        url_pattern = re.compile('https:\/\/music.yandex.ru\/users\/.*\/playlists\/\d*\/?$')
        return bool(url_pattern.match(url))

    def parse(self, url: str) -> List[MusicInfo]:
        raise NotImplementedError()
