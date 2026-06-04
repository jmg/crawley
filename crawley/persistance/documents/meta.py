"""Shared infrastructure for document storages."""

from crawley.config import CRAWLEY_ROOT_DIR

documents_entities = []


class BaseDocument:
    """Base class registering user document classes.

    Document classes declared inside the ``crawley`` package itself (the
    abstract bases) are not registered.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        module = getattr(cls, "__module__", "") or ""
        if not module.startswith(CRAWLEY_ROOT_DIR):
            documents_entities.append(cls)


class BaseDocumentSession:
    """Base class for the document "sessions" (file writers)."""

    file_name = None

    def set_up(self, settings, storage_name):
        self.settings = settings
        self.file_name = getattr(settings, storage_name)

    def commit(self):  # pragma: no cover - interface only
        raise NotImplementedError

    def close(self):
        pass
