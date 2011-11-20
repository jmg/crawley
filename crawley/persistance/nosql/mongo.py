from pymongo.connection import Connection

mongo_objects = []

class MongoEntity(object):

    def __init__(self, **kwargs):

        mongo_objects.append((self.__class__.__name__, kwargs))


class Session(object):

    def set_up(self, settings):

        self.settings = settings
        self.connection = Connection(settings.MONGO_DB_HOST)

    def commit(self):

        db = getattr(self.connection, self.settings.MONGO_DB_NAME)

        for entity, obj in mongo_objects:

            if self.settings.SHOW_DEBUG_INFO:
                print obj

            doc = getattr(db, entity)
            doc.save(obj)

    def close(self):
        pass


mongo_session = Session()
