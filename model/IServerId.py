import zope.interface


class IServerId(zope.interface.Interface):
    def get_server_id() -> str:
        pass
