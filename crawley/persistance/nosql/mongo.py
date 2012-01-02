from pymongo.connection import Connection
from base import BaseNosqlSession, NosqlEntity

mongo_objects = []

class MongoEntity(NosqlEntity):

    collection = mongo_objects


class Session(BaseNosqlSession):

    def set_up(self, settings, storage_name):

        BaseNosqlSession.set_up(self, settings, storage_name)

        self.connection = Connection(self.db_host)
        self.db = getattr(self.connection, self.settings.MONGO_DB_NAME)

    def commit(self):

        for entity, obj in mongo_objects:

            if self.settings.SHOW_DEBUG_INFO:
                print obj

            doc = getattr(self.db, entity)
            doc.save(obj)

    def close(self):
        pass


mongo_session = Session()
