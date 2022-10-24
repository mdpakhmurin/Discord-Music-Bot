import zope.interface

class IMusic(zope.interface.Interface):
    def __init__(author: str, title: str, link: str):
        pass

    def author() -> str:
        pass
    
    def title() -> str:
        pass
    
    def link() -> str:
        pass