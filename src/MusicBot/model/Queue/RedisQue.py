from typing import List
import zope.interface

import redis
import pickle

from MusicBot.model.Queue.IQue import IQue


@zope.interface.implementer(IQue)
class RedisQue():
    def __init__(self, id: str, host='localhost', port='6379'):
        self._bd = redis.Redis(host=host, port=port)
        self._id = id

        if not self._bd.ping():
            raise ConnectionError(f"Cannot connect to Redis database ({host, port})")

    def get_id(self) -> str:
        return self._id

    def push_back(self, element: object) -> None:
        element = pickle.dumps(element)
        self._bd.rpush(self._id, element)

    def peek_front(self) -> object:
        if self.get_size() == 0:
            return None

        element = self._bd.lrange(self._id, 0, 0)[0]
        element = pickle.loads(element) 
        return element

    def pop_front(self) -> object:
        if self.get_size() == 0:
            return None

        element = self._bd.lpop(self._id)
        element = pickle.loads(element) 
        return element

    def clear(self) -> None:
        self._bd.delete(self._id)

    def get_size(self) -> int:
        return self._bd.llen(self._id)

    def get_all(self) -> List[object]:
        elems = self._bd.lrange(self._id, 0, -1)
        elems = [pickle.loads(x) for x in elems]
        return elems