import zope.interface

from MusicBot.model.Queue.IQue import IQue


class IQueStorage(zope.interface.Interface):
    def get_que(id: str) -> IQue:
        pass
