import zope.interface

from IMusic import IMusic

@zope.interface.implementer(IMusic)
class Music():
    def __init__(self, author: str, title: str, link: str):
        self._author = str(author)
        self._title = str(title)
        self._link = str(link)

    def author(self) -> str:
        return self._author
    
    def title(self) -> str:
        return self._title
    
    def link(self) -> str:
        return self._link

    def __repr__(self) -> str:
        return f'Music(author: "{self._author}", title: "{self._title}", link: "{self._link}")'