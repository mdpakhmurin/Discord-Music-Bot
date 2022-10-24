from typing import List
import zope.interface

from IMusic import IMusic


class IMusicBase(zope.interface.Interface):
    def searchable(text: str) -> bool:
        pass

    def search(text: str) -> List[IMusic]:
        pass
