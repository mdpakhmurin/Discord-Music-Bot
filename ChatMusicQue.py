import imp
import zope.interface

from IChat import IChat
from IQue import IQue


@ zope.interface.implementer(IChat, IQue)
class ChatMusicQue():
    def get_chat_id():
        pass

    def push_back(elemnt: object) -> None:
        pass

    def peek_front() -> object:
        pass

    def pop_front() -> object:
        pass

    def clear():
        pass

    def size() -> int:
        pass
