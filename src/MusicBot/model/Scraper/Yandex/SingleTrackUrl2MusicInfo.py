from typing import List

from bs4 import BeautifulSoup
import aiohttp
import re
import zope.interface

from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


@zope.interface.implementer(IUrl2MusicInfo)
class SingleTrackUrl2MusicInfo():
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
        url_pattern = re.compile('https:\/\/music.yandex.ru\/album\/\d*\/track\/\d*\/?$')
        return bool(url_pattern.match(url))

    async def _try_parse_asc(self, url: str) -> List[MusicInfo]:
        target_track_id = url.split('/')[-1]

        tracks = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')

                track_author_html = soup.find('span', class_='d-artists')
                track_authors_text = track_author_html.text.strip()
                track_authors = track_authors_text.split(',')

                tracks_titles_html = soup.find_all('a', class_='d-track__title')
                for track_title_html in tracks_titles_html:
                    current_track_id = track_title_html['href'].split('/')[-1]
                    if current_track_id == target_track_id:
                        track_title = track_title_html.text.strip()

                        tracks.append(MusicInfo(track_title, track_authors))
                        break

        return tracks

    def parse(self, url: str) -> List[MusicInfo]:
        raise NotImplementedError()
