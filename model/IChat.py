import zope.interface


class IChat(zope.interface.Interface):
    def chat_id() -> str:
        pass
