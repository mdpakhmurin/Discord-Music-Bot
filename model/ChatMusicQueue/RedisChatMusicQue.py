import zope.interface

import redis
import pickle

from model.IChat import IChat
from model.ChatMusicQueue.IQue import IQue


@zope.interface.implementer(IChat, IQue)
class RedisChatMusicQue():
    def __init__(self, chat_id: str, host='localhost', port='6379'):
        self._bd = redis.Redis(host=host, port=port)
        self._chat_id = chat_id

    def chat_id(self) -> str:
        return self._chat_id

    def push_back(self, element: object) -> None:
        element = pickle.dumps(element)
        self._bd.rpush(self._chat_id, element)

    def peek_front(self) -> object:
        element = self._bd.lrange(self._chat_id, 0, 0)[0]
        element = pickle.loads(element) 
        return element

    def pop_front(self) -> object:
        element = self._bd.lpop(self._chat_id)
        element = pickle.loads(element) 
        return element

    def clear(self) -> None:
        self._bd.delete(self._chat_id)

    def size(self) -> int:
        return self._bd.llen(self._chat_id)