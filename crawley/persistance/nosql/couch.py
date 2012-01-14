import couchdb
from base import BaseNosqlSession, NosqlEntity

couch_objects = []

class CouchEntity(NosqlEntity):

    collection = couch_objects


class Session(BaseNosqlSession):

    def set_up(self, settings, storage_name):

        BaseNosqlSession.set_up(self, settings, storage_name)
        server = couchdb.Server(self.db_host)

        try:
            self.db = server[settings.COUCH_DB_NAME]
        except:
            self.db = server.create(settings.COUCH_DB_NAME)

    def commit(self):

        for entity, obj in couch_objects:

            if self.settings.SHOW_DEBUG_INFO:
                print obj

            self.db.save(obj)

    def close(self):
        pass


couch_session = Session()


