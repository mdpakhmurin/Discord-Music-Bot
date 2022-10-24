import zope.interface


class IQue(zope.interface.Interface):
    def push_back(element: object) -> None:
        pass

    def peek_front() -> object:
        pass

    def pop_front() -> object:
        pass

    def clear():
        pass

    def size() -> int:
        pass
