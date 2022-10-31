from typing import List
import zope.interface

from MusicBot.model.IMusic import IMusic


class IMusicSearcher(zope.interface.Interface):
    def searchable(text: str) -> bool:
        pass

    def search(text: str) -> List[IMusic]:
        pass
