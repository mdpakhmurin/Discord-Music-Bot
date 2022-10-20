import imp
import string
import zope.interface

from IChat import IChat
from IQue import IQue


@ zope.interface.implementer(IChat, IQue)
class ChatMusicQue():
    def __init__(self, chat_id: str):
        pass

    def chat_id(self):
        pass

    def push_back(self, element: object) -> None:
        pass

    def peek_front(self) -> object:
        pass

    def pop_front(self) -> object:
        pass

    def clear(self) -> None:
        pass

    def size(self) -> int:
        pass
