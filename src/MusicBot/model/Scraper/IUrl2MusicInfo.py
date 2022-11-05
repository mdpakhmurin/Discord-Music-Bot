from typing import List

import zope.interface

from MusicBot.model.Scraper.MusicInfo import MusicInfo


class IUrl2MusicInfo(zope.interface.Interface):
    async def parse_asc(url: str) -> List[MusicInfo]:
        pass

    def parse(url: str) -> List[MusicInfo]:
        pass
