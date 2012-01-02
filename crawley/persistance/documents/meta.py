from crawley.config import CRAWLEY_ROOT_DIR

documents_entities = []

class DocumentMeta(type):
    """
        This metaclass adds the user's documents storages to a list
        used by the CLI commands.
        Abstract base documents storages won't be added.
    """

    def __init__(cls, name, bases, dct):

        if not hasattr(cls, '__module__' ) or not cls.__module__.startswith(CRAWLEY_ROOT_DIR):
            documents_entities.append(cls)
        super(DocumentMeta, cls).__init__(name, bases, dct)


class BaseDocumentSession(object):

    def set_up(self, settings, storage_name):

        self.settings = settings
        self.file_name = getattr(settings, storage_name)
