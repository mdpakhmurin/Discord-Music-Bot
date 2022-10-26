import zope.interface

class IMusic(zope.interface.Interface):
    def __init__(author: str, title: str, link: str):
        pass

    def get_author() -> str:
        pass
    
    def get_title() -> str:
        pass
    
    def get_link() -> str:
        pass