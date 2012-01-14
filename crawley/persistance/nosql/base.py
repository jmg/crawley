
class NosqlEntity(object):
    """
        Base of NosqlEntities like MongoEntity or CouchEntity

        Collection is a list of nosql objects and it must be overrrided
        in the base classes.
    """
    def __init__(self, **kwargs):

        self.collection.append((self.__class__.__name__, kwargs))


class BaseNosqlSession(object):

    def set_up(self, settings, storage_name):

        self.settings = settings
        self.db_host = getattr(settings, storage_name)
