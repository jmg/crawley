"""Base classes for the NoSQL storages."""


class NosqlEntity:
    """Base for NoSQL entities (Mongo / Couch).

    ``collection`` is a shared list of ``(entity_name, data)`` tuples and must
    be overridden by subclasses.
    """

    collection = None

    def __init__(self, **kwargs):
        self.collection.append((self.__class__.__name__, kwargs))


class BaseNosqlSession:
    def set_up(self, settings, storage_name):
        self.settings = settings
        self.db_host = getattr(settings, storage_name)

    def commit(self):  # pragma: no cover - interface only
        raise NotImplementedError

    def close(self):
        pass
