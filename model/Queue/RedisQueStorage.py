import zope.interface
from model.Queue.IQue import IQue

from model.Queue.IQueStorage import IQueStorage
from model.Queue.RedisQue import RedisQue

@zope.interface.implementer(IQueStorage)
class RedisQueStorage():
    def __init__(self, host='localhost', port='6379') -> None:
        self._host = host
        self._port = port

    def get_que(self, id: str) -> IQue:
        return RedisQue(id=str(id), host=self._host, port=self._port)