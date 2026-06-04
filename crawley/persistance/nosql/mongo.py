"""MongoDB storage based on a modern ``pymongo``."""

import logging

from crawley.persistance.nosql.base import BaseNosqlSession, NosqlEntity

log = logging.getLogger("crawley.persistance.mongo")

mongo_objects = []


class MongoEntity(NosqlEntity):
    collection = mongo_objects


class Session(BaseNosqlSession):
    def set_up(self, settings, storage_name):
        super().set_up(settings, storage_name)

        from pymongo import MongoClient

        self.connection = MongoClient(self.db_host)
        self.db = self.connection[self.settings.MONGO_DB_NAME]

    def commit(self):
        for entity, obj in mongo_objects:
            if getattr(self.settings, "SHOW_DEBUG_INFO", False):
                log.debug("%s", obj)
            self.db[entity].insert_one(dict(obj))

    def close(self):
        if hasattr(self, "connection"):
            self.connection.close()


mongo_session = Session()
